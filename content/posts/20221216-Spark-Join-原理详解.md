---
title: "Spark Join 原理详解"
date: 2022-12-16T11:04:27+08:00
lastmod: 2022-12-16T11:04:27+08:00
author: ["Reid"]
categories: 
- Spark
tags: 
- Spark
- Join
keyword:
- Spark
- Join
description: ""
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Spark-Join-原理详解
draft: false # 是否为草稿
comments: true
showToc: true # 显示目录
TocOpen: false # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
disableShare: true # 底部不显示分享栏
showbreadcrumbs: true #顶部显示当前路径
cover:
    image: ""
    caption: ""
    alt: ""
    relative: false
---

## 介绍
Join大致包括三个要素：Join方式、Join条件以及过滤条件。其中过滤条件也可以通过AND语句放在Join条件中。
![join](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.3auv97qmulk0.webp)
Spark支持的Join 包括:
- inner join
- left outer join
- right outer join
- full outer join
- left semi join
- left anti join

## Join 的基本流程
总体上来说，Join的基本实现流程如下图所示，Spark将参与Join的两张表抽象为流式遍历表(streamIter)和查找表(buildIter)，通常streamIter为大表，buildIter为小表，我们不用担心哪个表为streamIter，哪个表为buildIter，这个spark会根据join语句自动帮我们完成。
![流程](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.4hvszw2v3nc0.webp)

在实际计算时，spark会`基于streamIter`来遍历，每次取出streamIter中的一条记录rowA，根据Join条件计算keyA，然后根据该keyA去buildIter中查找所有满足Join条件(keyB==keyA)的记录rowBs，并将rowBs中每条记录分别与rowAjoin得到join后的记录，最后根据过滤条件得到最终join的记录。

从上述计算过程中不难发现，对于每条来自streamIter的记录，都要去buildIter中查找匹配的记录，所以`buildIter一定要是查找性能较优的数据结构 如Hash Table`。spark提供了三种join实现：sort merge join、broadcast join以及hash join。

## Hash join实现
spark提供了hash join实现方式，在shuffle read阶段不对记录排序，反正来自两格表的具有相同key的记录会在同一个分区，只是在分区内不排序，将来自buildIter的记录放到hash表中，以便查找，如下图所示。

由于Spark是一个分布式的计算引擎，可以通过分区的形式将大批量的数据划分成n份较小的数据集进行并行计算。这种思想应用到Join上便是Shuffle Hash Join了。利用key相同必然分区相同的这个原理，SparkSQL将较大表的join分而治之，先将表划分成n个分区，在对buildlter查找表和streamlter表进行Hash Join。
![hasJoin](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.360e1g4bv760.webp)

### Shuffle Hash Join分为两步：
1. 对两张表分别按照join keys进行重分区，即shuffle，目的是为了让有相同join keys值的记录分到对应的分区中
2. 对 对应分区中的数据进行join，此处先将小表分区构造为一张hash表，然后根据大表分区中记录的join keys值拿出来进行匹配

不难发现，要将来自buildIter的记录放到hash表中，那么每个分区来自buildIter的记录不能太大，否则就存不下，默认情况下hash join的实现是关闭状态，如果要使用hash join，必须满足以下四个条件：
- buildIter总体估计大小超过spark.sql.autoBroadcastJoinThreshold设定的值，即不满足broadcast join条件
- 开启尝试使用hash join的开关，spark.sql.join.preferSortMergeJoin=false
- 每个分区的平均大小不超过spark.sql.autoBroadcastJoinThreshold设定的值，即shuffle read阶段每个分区来自buildIter的记录要能放到内存中
- streamIter的大小是buildIter三倍以上

## Sort Merge Join 实现
上面介绍的实现对于一定大小的表比较适用，但当两个表都非常大时，显然无论适用哪种都会对计算内存造成很大压力。这是因为join时两者采取的都是hash join，是将一侧的数据完全加载到内存中，使用hash code取join keys值相等的记录进行连接。

要让两条记录能join到一起，首先需要将具有相同key的记录在同一个分区，所以通常来说，需要做一次shuffle，map阶段根据join条件确定每条记录的key，基于该key做shuffle write，将可能join到一起的记录分到同一个分区中，这样在shuffle read阶段就可以将两个表中具有相同key的记录拉到同一个分区处理。前面我们也提到，对于buildIter一定要是查找性能较优的数据结构，通常我们能想到hash表，但是对于一张较大的表来说，不可能将所有记录全部放到hash表中，SparkSQL采用了一种全新的方案来对表进行Join，即Sort Merge Join。这种实现方式不用将一侧数据全部加载后再进行hash join，但需要在join前将数据排序，如下图所示：
![sortMerge](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.17azw5lad074.webp)

三个步骤:
**shuffle阶段**：或者说shuffle write 阶段，将两张大表根据join key进行重新分区，两张表数据会分布到整个集群，以便分布式并行处理
**sort阶段**：对单个分区节点的两表数据，分别进行排序
**merge阶段**：或者说shuffle read 阶段，对排好序的两张分区表数据执行join操作。join操作很简单，分别遍历两个有序序列，碰到相同join key就merge输出，否则取更小一边

在shuffle read阶段，分别对streamIter和buildIter进行merge sort，在遍历streamIter时，对于每条记录，都采用顺序查找的方式从buildIter查找对应的记录，由于两个表都是排序的，每次处理完streamIter的一条记录后，对于streamIter的下一条记录，只需从buildIter中上一次查找结束的位置开始查找，所以说每次在buildIter中查找不必重头开始，整体上来说，查找性能还是较优的。

仔细分析的话会发现，sort-merge join的代价并不比shuffle hash join小，反而是多了很多。那为什么SparkSQL还会在两张大表的场景下选择使用sort-merge join算法呢？这和Spark的shuffle实现有关，目前spark的shuffle实现都适用sort-based shuffle算法，因此在经过shuffle之后partition数据都是按照key排序的。因此理论上可以认为数据经过shuffle之后是不需要sort的，可以直接merge。

## Broadcast Join实现
为了能具有相同key的记录分到同一个分区，我们通常是做shuffle，而shuffle在Spark中是比较耗时的操作，我们应该尽可能的设计Spark应用使其避免大量的shuffle。。那么如果buildIter是一个非常小的表，那么其实就没有必要大动干戈做shuffle了，直接将buildIter广播到每个计算节点，然后将buildIter放到hash表中，如下图所示。
![broadcast](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.5v9djh5ouq80.webp)

在执行上，主要可以分为以下两步：
1. broadcast阶段：将小表广播分发到大表所在的所有主机。分发方式可以有driver分发，或者采用p2p方式。
2. hash join阶段：在每个executor上执行单机版hash join，小表映射，大表试探；

Broadcast Join的条件有以下几个：
1. 被广播的表需要小于spark.sql.autoBroadcastJoinThreshold所配置的值，默认是10M （或者加了broadcast join的hint）
2. 基表不能被广播，比如left outer join时，只能广播右表

## Hive Join
Hive中的Join可分为Common Join（Reduce阶段完成join）和Map Join（Map阶段完成join）。
### Hive Common Join
如果不指定MapJoin或者不符合MapJoin的条件，那么Hive解析器会默认把执行Common Join，即在Reduce阶段完成join。整个过程包含Map、Shuffle、Reduce阶段。

- Map阶段
读取源表的数据，Map输出时候以Join on条件中的列为key，如果Join有多个关联键，则以这些关联键的组合作为key；Map输出的value为join之后所关心的(select或者where中需要用到的)列，同时在value中还会包含表的Tag信息，用于标明此value对应哪个表。

- Shuffle阶段
根据key的值进行hash，并将key/value按照hash值推送至不同的reduce中，这样确保两个表中相同的key位于同一个reduce中。

- Reduce阶段
根据key的值完成join操作，期间通过Tag来识别不同表中的数据。

```sql
SELECT a.id,a.dept,b.age 
FROM a join b 
ON (a.id = b.id);
```
![Common Join](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.5rzbfv75s340.webp)

### Hive Map Join
MapJoin通常用于一个很小的表和一个大表进行join的场景，具体小表有多小，由参数hive.mapjoin.smalltable.filesize来决定，默认值为25M。满足条件的话Hive在执行时候会自动转化为MapJoin，或使用hint提示 /*+ mapjoin(table) */执行MapJoin。
![MapJoin](https://cdn.staticaly.com/gh/Reid00/image-host@main/20221216/image.4sz2rswtp9y0.webp)

如上图中的流程，首先Task A在客户端本地执行，负责扫描小表b的数据，将其转换成一个HashTable的数据结构，并写入本地的文件中，之后将该文件加载到DistributeCache中。
接下来的Task B任务是一个没有Reduce的MapReduce，启动MapTasks扫描大表a，在Map阶段，根据a的每一条记录去和DistributeCache中b表对应的HashTable关联，并直接输出结果，因为没有Reduce，所以有多少个Map Task，就有多少个结果文件。
注意：Map JOIN不适合FULL/RIGHT OUTER JOIN。