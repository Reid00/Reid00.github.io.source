---
title: "常用Normalization方法的总结与思考"
date: 2022-06-08T11:36:46+08:00
lastmod: 2022-06-08T11:36:46+08:00
author: ["Reid"]
categories: 
- Machine Learning
- 机器学习
tags: 
- Normalization
- BN
- LN
- IN
- GN
keyword:
- Machine Learning
- 机器学习
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

## 简介

常用的Normalization方法主要有：Batch Normalization（BN，2015年）、Layer Normalization（LN，2016年）、Instance Normalization（IN，2017年）、Group Normalization（GN，2018年）。它们都是从激活函数的输入来考虑、做文章的，以不同的方式**对激活函数的输入进行 Norm** 的。

我们将输入的 **feature map shape** 记为**[N, C, H, W]**，其中N表示batch size，即N个样本；C表示通道数；H、W分别表示特征图的高度、宽度。这几个方法主要的区别就是在：

1. BN是在batch上，对N、H、W做归一化，而保留通道 C 的维度。BN对较小的batch size效果不好。BN适用于固定深度的前向神经网络，如CNN，不适用于RNN；

2. LN在通道方向上，对C、H、W归一化，主要对RNN效果明显；

3. IN在图像像素上，对H、W做归一化，用在风格化迁移；

4. GN将channel分组，然后再做归一化。

![img](https://mmbiz.qpic.cn/sz_mmbiz_jpg/gYUsOT36vfoMdJzNnwHQ7Elg9fUeYPYz8lmO7YQC1FQ8yFKw5ibW1u7GVpTxm6Kv989mCcRGrQn4jArecib8qOqQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)每个子图表示一个特征图，其中N为批量，C为通道，（H，W）为特征图的高度和宽度。通过蓝色部分的值来计算均值和方差，从而进行归一化。

**如果把特征图比喻成一摞书，这摞书总共有 N 本，每本有 C 页，每页有 H 行，每行 有W 个字符。**

1. BN 求均值时，相当于把这些书按页码一一对应地加起来（例如第1本书第36页，第2本书第36页......），再除以每个页码下的字符总数：N×H×W，因此可以把 BN 看成求“平均书”的操作（注意这个“平均书”每页只有一个字），求标准差时也是同理。

2. LN 求均值时，相当于把每一本书的所有字加起来，再除以这本书的字符总数：C×H×W，即求整本书的“平均字”，求标准差时也是同理。

3. IN 求均值时，相当于把一页书中所有字加起来，再除以该页的总字数：H×W，即求每页书的“平均字”，求标准差时也是同理。

4. GN 相当于把一本 C 页的书平均分成 G 份，每份成为有 C/G 页的小册子，求每个小册子的“平均字”和字的“标准差”。

---
参考:
1. https://mp.weixin.qq.com/s/dDMPBYjPeilivSA8J8W7lA 
2. https://zhuanlan.zhihu.com/p/72589565