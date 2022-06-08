---
title: "集成学习之xgboost"
date: 2022-06-08T11:09:50+08:00
lastmod: 2022-06-08T11:09:50+08:00
author: ["Reid"]
categories: 
- Machine Learning
tags: 
- xgboost
- 集成学习
keyword:
- Machine Learning
- xgboost
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

### **一、XGBoost和GBDT**

xgboost是一种集成学习算法，属于3类常用的集成方法(bagging,boosting,stacking)中的boosting算法类别。它是一个加法模型，基模型一般选择树模型，但也可以选择其它类型的模型如逻辑回归等。



xgboost属于梯度提升树(GBDT)模型这个范畴，GBDT的基本想法是让新的基模型（GBDT以CART分类回归树为基模型）去拟合前面模型的偏差，从而不断将加法模型的偏差降低。

相比于经典的GBDT，xgboost做了一些改进，从而在效果和性能上有明显的提升（**划重点面试常考**）。

**第一，GBDT将目标函数泰勒展开到一阶，而xgboost将目标函数泰勒展开到了二阶**。保留了更多有关目标函数的信息，对提升效果有帮助。

**第二，GBDT是给新的基模型寻找新的拟合标签**（前面加法模型的负梯度），**而xgboost是给新的基模型寻找新的目标函数**（目标函数关于新的基模型的二阶泰勒展开）。

**第三，xgboost加入了和叶子权重的L2正则化项**，因而有利于模型获得更低的方差。

**第四，xgboost增加了自动处理缺失值特征的策略。**通过把带缺失值样本分别划分到左子树或者右子树，比较两种方案下目标函数的优劣，从而自动对有缺失值的样本进行划分，无需对缺失特征进行填充预处理。

**此外**，xgboost还支持候选分位点切割，特征并行等，可以提升性能。

### 二、XGBoost原理概述

面从假设空间，目标函数，优化算法3个角度对xgboost的原理进行概括性的介绍。

**1，假设空间**

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0Fe8QIBoZlJ1FOxl6hMHzqJdDW4qzvibqEs6yoPsLbma2nNkL7gsaNng/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0lwXWCdMDP5ibMK3D3t5ianLwCst5opXGRrthdnecPzKAF6VL5Yszuxww/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0fx2icma2wLZmppde5SJQbjORDVjEYTeJicpJtQGQnwib4oE0bFUwSplPg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



**2，目标函数**

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0mBrvmW8ha6bydPiaErK5FdyyNYbxiaU3GvdRkFSmf2wrb16wWC7DqdHQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0xt3jt0LKucp8j0ayMRcBchBOutibTP3uFKj62bEt5ZnSYq9ibhMibXAJQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



**3，优化算法**

基本思想：贪心法，逐棵树进行学习，每棵树拟合之前模型的偏差。

### **三、第t棵树学什么？**

###  

要完成构建xgboost模型，我们需要确定以下一些事情。



1，如何boost? 如果已经得到了前面t-1棵树构成的加法模型，如何确定第t棵树的学习目标？



2，如何生成树？已知第t棵树的学习目标的前提下，如何学习这棵树？具体又包括是否进行分裂？选择哪个特征进行分裂？选择什么分裂点位？分裂的叶子节点如何取值？



我们首先考虑如何boost的问题，顺便解决分裂的叶子节点如何取值的问题。

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0RkRqZUiaaWHR5LOhiau1Ub1NBq95icH2AzxhJGALrPN7mooo2icLU6icC6A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR04V9ESutbFZ6eqmY5RUwyu6YohfugwwGpB0F8exfgBc0bJO6ic9Ug8jQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR09IF4icI2p1HcLibicLaAw3JcYqg1QD64QagqFjkDnMq84Gguoej1QYBtA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0gWlcQhTq8iasykFK9BrnvXbFXknOHt9Rl1yaejLz9vSk6EFZ2kvhUFQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)


### **四、如何生成第t棵树？**

xgboost采用二叉树，开始的时候，全部样本都在一个叶子节点上。然后叶子节点不断通过二分裂，逐渐生成一棵树。

xgboost使用levelwise的生成策略，即每次对同一层级的全部叶子节点尝试进行分裂。

对叶子节点分裂生成树的过程有几个基本的问题：是否要进行分裂？选择哪个特征进行分裂？在特征的什么点位进行分裂？以及分裂后新的叶子上取什么值？

叶子节点的取值问题前面已经解决了。我们重点讨论几个剩下的问题。

**1，是否要进行分裂？**
根据树的剪枝策略的不同，这个问题有两种不同的处理。如果是预剪枝策略，那么只有当存在某种分裂方式使得分裂后目标函数发生下降，才会进行分裂。

但如果是后剪枝策略，则会无条件进行分裂，等树生成完成后，再从上而下检查树的各个分枝是否对目标函数下降产生正向贡献从而进行剪枝。

xgboost采用预剪枝策略，只有分裂后的增益大于0才会进行分裂。

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0bDu5YWbKfb5k6Np28TfpWcg4FZJpTgb1udWiaxoTAnsJJKBaoxibKMKQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

**2，选择什么特征进行分裂？**

xgboost采用特征并行的方法进行计算选择要分裂的特征，即用多个线程，尝试把各个特征都作为分裂的特征，找到各个特征的最优分割点，计算根据它们分裂后产生的增益，选择增益最大的那个特征作为分裂的特征。

**3，选择什么分裂点位？**

xgboost选择某个特征的分裂点位的方法有两种，一种是全局扫描法，另一种是候选分位点法。
全局扫描法将所有样本该特征的取值按从小到大排列，将所有可能的分裂位置都试一遍，找到其中增益最大的那个分裂点，其计算复杂度和叶子节点上的样本特征不同的取值个数成正比。
而候选分位点法是一种近似算法，仅选择常数个（如256个）候选分裂位置，然后从候选分裂位置中找出最优的那个。

![img](https://mmbiz.qpic.cn/mmbiz_png/4WgILHBwVHibhx13Lugx4C4vibEEpKDjR0NEaYoARvShoshdKM5sciaz5ic565grdAWhF2zsRPib5yKImkEk0wkDjYA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 五、XGBoost算法原理小结

XGBoost（eXtreme Gradient Boosting）全名叫极端梯度提升，XGBoost是集成学习方法的王牌，在Kaggle数据挖掘比赛中，大部分获胜者用了XGBoost，XGBoost在绝大多数的回归和分类问题上表现的十分顶尖，本文较详细的介绍了XGBoost的算法原理。

目录

1. 最优模型的构建方法

2. Boosting的回归思想

3. XGBoost的目标函数推导

4. XGBoost的回归树构建方法

5. XGBoost与GDBT的区别

**最优模型的构建方法**

构建最优模型的一般方法是最小化训练数据的损失函数，我们用字母 L表示，如下式：

![img](https://t12.baidu.com/it/u=2088825977,1064375271&fm=173&app=49&f=JPEG?w=275&h=87&s=8D02ED128D214D0156D501DE0000C0B3)

式（1）称为经验风险最小化，训练得到的模型复杂度较高。当训练数据较小时，模型很容易出现过拟合问题。

因此，为了降低模型的复杂度，常采用下式：

![img](https://t10.baidu.com/it/u=3726621105,2442873595&fm=173&app=49&f=JPEG?w=351&h=52)

其中J(f)为模型的复杂度，式（2）称为结构风险最小化，结构风险最小化的模型往往对训练数据以及未知的测试数据都有较好的预测 。

应用：决策树的生成和剪枝分别对应了经验风险最小化和结构风险最小化，XGBoost的决策树生成是结构风险最小化的结果，后续会详细介绍。

**Boosting方法的回归思想**

Boosting法是结合多个弱学习器给出最终的学习结果，不管任务是分类或回归，我们都用回归任务的思想来构建最优Boosting模型 。

回归思想：把每个弱学习器的输出结果当成连续值，这样做的目的是可以对每个弱学习器的结果进行累加处理，且能更好的利用损失函数来优化模型。

假设

![img](https://t10.baidu.com/it/u=2575575693,679892115&fm=173&app=49&f=JPEG?w=60&h=36&s=8DA2E516CDA6F8111CC0C5D60000B0B3)

是第 t 轮弱学习器的输出结果，

![img](https://t11.baidu.com/it/u=3480491077,4153735365&fm=173&app=49&f=JPEG?w=27&h=47)

是模型的输出结果，

![img](https://t10.baidu.com/it/u=1589424537,273963798&fm=173&app=49&f=JPEG?w=24&h=26)

是实际输出结果，表达式如下：

![img](https://t12.baidu.com/it/u=3934660316,3850604984&fm=173&app=49&f=JPEG?w=269&h=110&s=8D32ED120B61680118DDC0DA0000D0B1)

上面两式就是加法模型，都默认弱学习器的输出结果是连续值。因为回归任务的弱学习器本身是连续值，所以不做讨论，下面详细介绍分类任务的回归思想。

**分类任务的回归思想：**

根据2.1式的结果，得到最终的分类器：

![img](https://t12.baidu.com/it/u=2106315725,639848079&fm=173&app=49&f=JPEG?w=393&h=58)

分类的损失函数一般选择指数函数或对数函数，这里假设损失函数为对数函数，学习器的损失函数是

![img](https://t11.baidu.com/it/u=2757775603,3145979471&fm=173&app=49&f=JPEG?w=345&h=37)

若实际输出结果yi=1，则：

![img](https://t10.baidu.com/it/u=2994708501,2270324777&fm=173&app=49&f=JPEG?w=314&h=48)

求（2.5）式对

![img](https://t11.baidu.com/it/u=3260474260,568114116&fm=173&app=49&f=JPEG?w=39&h=47&s=8DB2ED12EDF548111C78B5C2000070B1)

的梯度，得：

![img](https://t10.baidu.com/it/u=1519027692,1118277381&fm=173&app=49&f=JPEG?w=197&h=95&s=81306D328BB04C014875D0DA0000C0B3)

负梯度方向是损失函数下降最快的方向，（2.6）式取反的值大于0，因此弱学习器是往增大

![img](https://t12.baidu.com/it/u=58039754,2342150744&fm=173&app=49&f=JPEG?w=40&h=54&s=0530ED32EDF548110E68B0C20000C0B3)

的方向迭代的，图形表示为：

![img](https://t11.baidu.com/it/u=538277086,3452942280&fm=173&app=49&f=JPEG?w=389&h=283&s=4C843C728BDF40491E6560DE0000C0B2)

如上图，当样本的实际标记 yi 是 1 时，模型输出结果

![img](https://t12.baidu.com/it/u=58039754,2342150744&fm=173&app=49&f=JPEG?w=40&h=54&s=0530ED32EDF548110E68B0C20000C0B3)

随着迭代次数的增加而增加（红线箭头），模型的损失函数相应的减小；当样本的实际标记 yi 是 -1时，模型输出结果

![img](https://t12.baidu.com/it/u=58039754,2342150744&fm=173&app=49&f=JPEG?w=40&h=54&s=0530ED32EDF548110E68B0C20000C0B3)

随着迭代次数的增加而减小（红线箭头），模型的损失函数相应的减小 。这就是加法模型的原理所在，通过多次的迭代达到减小损失函数的目的。

小结：Boosting方法把每个弱学习器的输出看成是连续值，使得损失函数是个连续值，因此可以通过弱学习器的迭代达到优化模型的目的，这也是集成学习法加法模型的原理所在 。

**XGBoost算法的目标函数推导**

目标函数，即损失函数，通过最小化损失函数来构建最优模型，由第一节可知， 损失函数应加上表示模型复杂度的正则项，且XGBoost对应的模型包含了多个CART树，因此，模型的目标函数为：

![img](https://t10.baidu.com/it/u=1096985463,1889276164&fm=173&app=49&f=JPEG?w=357&h=54)

（3.1）式是正则化的损失函数，等式右边第一部分是模型的训练误差，第二部分是正则化项，这里的正则化项是K棵树的正则化项相加而来的。

**CART树的介绍：**

![img](https://t12.baidu.com/it/u=1604336024,2048239596&fm=173&app=49&f=JPEG?w=355&h=131&s=9988783391E67D035E7C10CF000080B2)

上图为第K棵CART树，确定一棵CART树需要确定两部分，第一部分就是树的结构，这个结构将输入样本映射到一个确定的叶子节点上，记为

![img](https://t11.baidu.com/it/u=1080851515,2092106391&fm=173&app=49&f=JPEG?w=56&h=33&s=8922CD16CF8EE8114AF548DA0200B0B3)

。第二部分就是各个叶子节点的值，q(x)表示输出的叶子节点序号，

![img](https://t11.baidu.com/it/u=3855316450,52407482&fm=173&app=49&f=JPEG?w=49&h=31&s=8C02ED16CD95E81108D4D8D20200D0B3)

表示对应叶子节点序号的值。由定义得：

![img](https://t10.baidu.com/it/u=1851728262,1452004307&fm=173&app=49&f=JPEG?w=202&h=36&s=8D42ED124567CB204A55E0D2000090B1)

**树的复杂度定义**

XGBoost法对应的模型包含了多棵cart树，定义每棵树的复杂度：

![img](https://t11.baidu.com/it/u=810269563,562881171&fm=173&app=49&f=JPEG?w=281&h=47&s=8D22ED12C55AEE335C5C20D60000D0B1)

其中T为叶子节点的个数，||w||为叶子节点向量的模 。γ表示节点切分的难度，λ表示L2正则化系数。

如下例树的复杂度表示：

![img](https://t10.baidu.com/it/u=2863031412,2342096706&fm=173&app=49&f=JPEG?w=640&h=370&s=0812CE121D5045CA0CCD68D8000050B2)

**目标函数推导**

根据（3.1）式，共进行t次迭代的学习模型的目标函数为：

![img](https://t11.baidu.com/it/u=236689006,1474271316&fm=173&app=49&f=JPEG?w=550&h=220&s=AC32ED1297D06DC25CFC0DC2000080B3)

泰勒公式的二阶导近似表示：

![img](https://t10.baidu.com/it/u=959253417,1988296487&fm=173&app=49&f=JPEG?w=512&h=53)

令

![img](https://t10.baidu.com/it/u=686929623,2192080821&fm=173&app=49&f=JPEG?w=53&h=29)

为Δx，则（3.5）式的二阶近似展开：

![img](https://t11.baidu.com/it/u=1862472463,3969586164&fm=173&app=49&f=JPEG?w=640&h=153&s=8D72E512C1354C23525D20DB000080B1)

其中：

![img](https://t10.baidu.com/it/u=602419326,77643855&fm=173&app=49&f=JPEG?w=204&h=35&s=8D60ED12C553FE325AF911C30000F0B1)

![img](https://t11.baidu.com/it/u=3021833638,1350476957&fm=173&app=49&f=JPEG?w=200&h=34&s=8C40F512C553EF305ADD10C20000E0B1)

![img](https://t12.baidu.com/it/u=1551381323,1490568674&fm=173&app=49&f=JPEG?w=107&h=33&s=8D42CD14C51FC6304E7439D60300C0B1)

表示前t-1棵树组成的学习模型的预测误差，gi和hi分别表示预测误差对当前模型的一阶导和二阶导 ，当前模型往预测误差减小的方向进行迭代。

忽略（3.8）式常数项，并结合（3.4）式，得：

![img](https://t11.baidu.com/it/u=833462836,1613458304&fm=173&app=49&f=JPEG?w=541&h=62)

通过（3.2）式简化（3.9）式：

![img](https://t10.baidu.com/it/u=4272700476,2093594111&fm=173&app=49&f=JPEG?w=550&h=61)

（3.10）式第一部分是对所有训练样本集进行累加，因为所有样本都是映射为树的叶子节点，我们换种思维，从叶子节点出发，对所有的叶子节点进行累加，得：

![img](https://t11.baidu.com/it/u=2042896387,2160999246&fm=173&app=49&f=JPEG?w=488&h=61)

令

![img](https://t12.baidu.com/it/u=1090269392,1428256557&fm=173&app=49&f=JPEG?w=201&h=50&s=8D02ED12CD16E4130EDCB0CE0000D0B1)

Gj 表示映射为叶子节点 j 的所有输入样本的一阶导之和，同理，Hj表示二阶导之和。

得：

![img](https://t10.baidu.com/it/u=2162289948,3953406118&fm=173&app=49&f=JPEG?w=431&h=53)

对于第 t 棵CART树的某一个确定结构（可用q(x)表示），其叶子节点是相互独立的，Gj和Hj是确定量，因此，（3.12）可以看成是关于叶子节点的一元二次函数 。最小化（3.12）式，得：

![img](https://t10.baidu.com/it/u=978046209,189317784&fm=173&app=49&f=JPEG?w=229&h=60&s=84306532C5356423487CE1DA0000D0B3)

得到最终的目标函数：

![img](https://t10.baidu.com/it/u=303000120,2319644979&fm=173&app=49&f=JPEG?w=321&h=66&s=8C32ED12CDF6EC035E7CE0D60000D0B3)

（3.14）也称为打分函数(scoring function)，它是衡量树结构好坏的标准，值越小，代表这样的结构越好 。我们用打分函数选择最佳切分点，从而构建CART树。

**CART回归树的构建方法**

上节推导得到的打分函数是衡量树结构好坏的标准，因此，可用打分函数来选择最佳切分点。首先确定样本特征的所有切分点，对每一个确定的切分点进行切分，切分好坏的标准如下：

![img](https://t11.baidu.com/it/u=2513959336,3320328419&fm=173&app=49&f=JPEG?w=456&h=78&s=8530E432C5674F304AF475DB0000E0B1)

Gain表示单节点obj*与切分后的两个节点的树obj*之差，遍历所有特征的切分点，找到最大Gain的切分点即是最佳分裂点，根据这种方法继续切分节点，得到CART树。若 γ 值设置的过大，则Gain为负，表示不切分该节点，因为切分后的树结构变差了。γ值越大，表示对切分后obj下降幅度要求越严，这个值可以在XGBoost中设定。

**XGBoost与GDBT的区别**

1. XGBoost生成CART树考虑了树的复杂度，GDBT未考虑，GDBT在树的剪枝步骤中考虑了树的复杂度。

2. XGBoost是拟合上一轮损失函数的二阶导展开，GDBT是拟合上一轮损失函数的一阶导展开，因此，XGBoost的准确性更高，且满足相同的训练效果，需要的迭代次数更少。

3. XGBoost与GDBT都是逐次迭代来提高模型性能，但是XGBoost在选取最佳切分点时可以开启多线程进行，大大提高了运行速度。

---
参考: 
https://mp.weixin.qq.com/s/cMgd-wBlzjacL21FPK2y7Q
https://www.cnblogs.com/pinard/p/10979808.html
