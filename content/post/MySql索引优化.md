---
title: "MySql索引优化"
date: 2022-06-08T11:04:01+08:00
lastmod: 2022-06-08T11:04:01+08:00
author: ["Reid"]
categories: 
- Storage
tags: 
- MySql
- 索引
- 优化
- 面试
keyword:
- Storage
- 面试
- 索引覆盖
description: ""
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: ""
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

数据库表结构：

```mysql
create table user (
    id int primary key,
    name varchar(20),
    sex varchar(5),
    index(name)
)engine=innodb;

select id,name where name='shenjian'
select id,name,sex where name='shenjian'
```

**多查询了一个属性，为何检索过程完全不同？**

**什么是回表查询？**

**什么是索引覆盖？**

**如何实现索引覆盖？**

**哪些场景，可以利用索引覆盖来优化SQL？**

### **一、什么是回表查询？**

这先要从InnoDB的索引实现说起，InnoDB有两大类索引：

- 聚集索引(clustered index)
- 普通索引(secondary index)

**InnoDB聚集索引和普通索引有什么差异？

**

InnoDB**聚集索引**的叶子节点存储行记录，因此， InnoDB必须要有，且只有一个聚集索引：

（1）如果表定义了PK，则PK就是聚集索引；

（2）如果表没有定义PK，则第一个not NULL unique列是聚集索引；

（3）否则，InnoDB会创建一个隐藏的row-id作为聚集索引；

*画外音：所以PK查询非常快，直接定位行记录。*

InnoDB**普通索引**的叶子节点存储主键值。

*画外音：注意，不是存储行记录头指针，MyISAM的索引叶子节点存储记录指针。*



举个栗子，不妨设有表：

　　*t(id PK, name KEY, sex, flag);*

*画外音：id是聚集索引，name是普通索引。*

表中有四条记录：

　　*1, shenjian, m, A*

　　*3, zhangsan, m, A*

　　*5, lisi, m, A*

　　*9, wangwu, f, B*

![img](https://img2018.cnblogs.com/blog/885859/201907/885859-20190729184808306-758660222.png)

两个B+树索引分别如上图：

　　（1）id为PK，聚集索引，叶子节点存储行记录；

　　（2）name为KEY，普通索引，叶子节点存储PK值，即id；

既然从普通索引无法直接定位行记录，那**普通索引的查询过程是怎么样的呢？**

通常情况下，需要扫描两遍索引树。

例如：

``` mysql
select` `* ``from` `t ``where` `name``=``'lisi'``;　
```

**是如何执行的呢？**

![img](https://img2018.cnblogs.com/blog/885859/201907/885859-20190729184911699-676257427.png)

如**粉红色**路径，需要扫码两遍索引树：

（1）先通过普通索引定位到主键值id=5；

（2）在通过聚集索引定位到行记录；

这就是所谓的**回表查询**，先定位主键值，再定位行记录，它的性能较扫一遍索引树更低。

### 二、什么是索引覆盖Covering index)？

MySQL官网，类似的说法出现在explain查询计划优化章节，即explain的输出结果Extra字段为**Using index**时，能够触发索引覆盖。

不管是SQL-Server官网，还是MySQL官网，都表达了：**只需要在一棵索引树上就能获取SQL所需的所有列数据，无需回表，速度更快。**

### **三、如何实现索引覆盖？**

常见的方法是：将被查询的字段，**建立到联合索引**里去。

仍是之前中的例子：

```mysql
create table user (
    id int primary key,
    name varchar(20),
    sex varchar(5),
    index(name)
)engine=innodb;
```

第一个SQL语句:

![image](https://raw.githubusercontent.com/Reid00/image-host/main/20220608/image.6ig5jbwgngk0.webp)

```mysql
select id, name from user where name='shenjian'
```

能够命中name索引，索引叶子节点存储了主键id，通过name的索引树即可获取id和name，无需回表，符合索引覆盖，效率较高。

*画外音，Extra：**Using index**。*

第二个SQL语句：

![image](https://raw.githubusercontent.com/Reid00/image-host/main/20220608/image.1ptp2ulckau8.webp)

```mysql
select id, name from user where name='shenjian'
```

能够命中name索引，索引叶子节点存储了主键id，但sex字段必须回表查询才能获取到，不符合索引覆盖，需要再次通过id值扫码聚集索引获取sex字段，效率会降低。

*画外音，Extra：**Using index condition**。*



如果把(name)单列索引升级为**联合索引(name, sex)**就不同了。

```mysql
create table user (
    id int primary key,
    name varchar(20),
    sex varchar(5),
    index(name, sex)
)engine=innodb;
```

![image](https://raw.githubusercontent.com/Reid00/image-host/main/20220608/image.4vkps30mzim0.webp)

可以看到：

```mysql
select id,name ... where name='shenjian';

select id,name,sex ... where name='shenjian';
```

都能够命中索引覆盖，无需回表。

*画外音，Extra：**Using index**。*

### **四、哪些场景可以利用索引覆盖来优化SQL？**

#### **场景1：全表count查询优化**

![image](https://raw.githubusercontent.com/Reid00/image-host/main/20220608/image.22a77fpqfxj4.webp)

原表为：

*user(PK id, name, sex)；*

```mysql
select count(name) from user;
```

不能利用索引覆盖。

添加索引：

```mysql
alter table user add key(name);
```

就能够利用索引覆盖提效。

**count(1)、count(*) 与 count(列名) 的区别？**

- count(*)包括了所有的列，相当于行数，在统计结果的时候，不会忽略列值为NULL
- count(1)包括了忽略所有列，用1代表代码行，在统计结果的时候，不会忽略列值为NULL
- count(列名)只包括列名那一列，在统计结果的时候，会忽略列值为空（这里的空不是只空字符串或者0，而是表示null）的计数，即某个字段值为NULL时，不统计。



#### **场景2：列查询回表优化**

```mysql
select id,name,sex ... where name='shenjian';
```

这个例子不再赘述，将单列索引(name)升级为联合索引(name, sex)，即可避免回表。

#### **场景3：分页查询**

```mysql
select id,name,sex ... order by name limit 500,100;
```

将单列索引(name)升级为联合索引(name, sex)，也可以避免回表。

---
参考: https://mp.weixin.qq.com/s/T7LnqldlD9sCH37gWUHVfQ