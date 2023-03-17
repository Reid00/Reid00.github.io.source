---
title: "CNN RNN GAN"
date: 2023-03-16T19:35:16+08:00
lastmod: 2023-03-16T19:35:16+08:00
author: ["Reid"]
categories: 
- Machine Learning
- 机器学习
- Deep Learning
tags: 
- CNN
- RNN
- GAN
keyword:
- Machine Learning
- 机器学习
- Deep Learning
description: CNN RNN GAN
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: CNN-RNN-GAN
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


### **01 全连接网络**

**全连接、密集和线性网络是最基本但功能强大的架构**这是机器学习的直接扩展，将神经网络与单个隐藏层结合使用。全连接层充当所有架构的最后一部分，用于获得使用下方深度网络所得分数的概率分布。

**如其名称所示，全连接网络将其上一层和下一层中的所有神经元相互连接。**网络可能最终通过设置权重来关闭一些神经元，但在理想情况下，最初所有神经元都参与训练。

### **02 编码器和解码器**

编码器和解码器可能是深度学习另一个最基本的架构之一。所有网络都有一个或多个**编码器–解码器**层。你可以将全连接层中的隐藏层视为来自编码器的编码形式，将输出层视为解码器，它将隐藏层解码并作为输出。通常，编码器将输入编码到中间状态，其中输入为向量，然后解码器网络将该中间状态解码为我们想要的输出形式。



编码器–解码器网络的一个规范示例是**序列到序列** （seq2seq）网络（图1.11），可用于机器翻译。一个句子将被编码为中间向量表示形式，其中整个句子以一些浮点数字的形式表示，解码器根据中间向量解码以生成目标语言的句子作为输出。

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOorJKgUJKcJQeY60GhqwInPQT7FiaoyxWX9PjM1u5MB1eIicUdRbibstiaOw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

▲图1.11 seq2seq 网络

**自动编码器**（图1.12）是一种特殊的编码器–解码器网络，属于**无监督学习**范畴。自动编码器尝试从未标记的数据中进行学习，将目标值设置为输入值。

例如，如果输入一个大小为100×100的图像，则输入向量的维度为10 000。因此，输出的大小也将为 10 000，但隐藏层的大小可能为 500。简而言之，你正在尝试将输入转换为较小的隐藏状态表示形式，从隐藏状态重新生成相同的输入。

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOoDHaeDAovFpIpaCXoiafibmLDWicvPict0jjx5NTHTrNyRoXKFD6h0KxeGQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

图1.12 自动编码器的结构

你如果能够训练一个可以做到这一点的神经网络，就会找到一个好的压缩算法，其可以将高维输入变为低维向量，这具有数量级收益。

如今，自动编码器正被广泛应用于不同的情景和行业。

### **03 循环神经网络**

循环神经网络（RNN）是**最常见的深度学习算法之一，它席卷了整个世界。**我们现在在自然语言处理或理解方面几乎所有最先进的性能都归功于RNN的变体。在循环网络中，你尝试识别数据中的最小单元，并使数据成为一组这样的单元。

在自然语言的示例中，最常见的方法是将一个单词作为一个单元，并在处理句子时将句子视为一组单词。你在整个句子上展开RNN，一次处理一个单词（图1.13）。RNN 具有适用于不同数据集的变体，有时我们会根据效率选择变体。**长短期记忆** （LSTM）和**门控循环单元**（GRU）是最常见的 RNN 单元。

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOozu5UbyVYqfjQ2p5SrFXHaoBTKq15l8cbxU2Iv16KATiaQbJPezNv9cQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

图1.13 循环网络中单词的向量表示形式

### **04 递归神经网络**

顾名思义，递归神经网络是一种树状网络，用于理解序列数据的分层结构。递归网络被研究者（尤其是 Salesforce 的首席科学家理查德·索彻和他的团队）广泛用于自然语言处理。

字向量能够有效地将一个单词的含义映射到一个向量空间，但当涉及整个句子的含义时，却没有像word2vec这样针对单词的首选解决方案。递归神经网络是此类应用最常用的算法之一。
递归网络可以创建解析树和组合向量，并映射其他分层关系（图1.14），这反过来又帮助我们找到组合单词和形成句子的规则。斯坦福自然语言推理小组开发了一种著名的、使用良好的算法，称为**SNLI，这是应用递归网络的一个好例子。**

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOoaCq4cNia2fv4hZ7icl19NYdKudW0O4jyasTetGytodWCibKaAj3ZIFv6Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

▲图1.14 递归网络中单词的向量表示形式

### **05 卷积神经网络**

卷积神经网络（CNN）（图1.15）使我们能够在计算机视觉中获得超人的性能，**它在2010年代早期达到了人类的精度，而且其精度仍在逐年提高。**

卷积网络是最容易理解的网络，因为它有可视化工具来显示每一层正在做什么。

Facebook AI研究（FAIR）负责人Yann LeCun早在20世纪90年代就发明了CNN。人们当时无法使用它，因为并没有足够的数据集和计算能力。CNN像滑动窗口一样扫描输入并生成中间表征，然后在它到达末端的全连接层之前对其进行逐层抽象。**CNN也已成功应用于非图像数据集。**

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOoOkrQsdHV4z19GrPl7DIt8wLjLOl1K0VKIoyvpssvDticfVoZ4cXucIA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

▲图1.15 典型的 CNN

Facebook的研究小组发现了一个基于卷积神经网络的先进自然语言处理系统，其卷积网络优于RNN，而后者被认为是任何序列数据集的首选架构。虽然一些神经科学家和人工智能研究人员不喜欢CNN（因为他们认为大脑不会像CNN那样做），但基于CNN的网络正在击败所有现有的网络实现。

### **06 生成对抗网络**

生成对抗网络（GAN）由 Ian Goodfellow 于 2014 年发明，自那时起，它颠覆了整个 AI 社群。它是最简单、最明显的实现之一，但其能力吸引了全世界的注意。GAN的配置如图1.16所示。

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOobxibdmZ88KNyHGuvbQVc3LruMFSWpMynZwOaQrCuibjuUdWbX72ZibJbA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

▲图1.16 GAN配置
两个网络相互竞争，最终达到一种平衡，即**生成网络可以生成数据，而鉴别网络很难将其与实际图像区分开。**

一个真实的例子就是警察和造假者之间的斗争：假设一个造假者试图制造假币，而警察试图识破它。最初，造假者没有足够的知识来制造看起来真实的假币。随着时间的流逝，造假者越来越善于制造看起来更像真实货币的假币。这时，警察起初未能识别假币，但最终他们会再次成功识别。

这种**生成–对抗**过程最终会形成一种平衡。GAN 具有极大的优势。

### **07 强化学习**

通过互动进行学习是人类智力的基础，强化学习是领导我们朝这个方向前进的方法。过去强化学习是一个完全不同的领域，它认为人类通过试错进行学习。然而，随着深度学习的推进，另一个领域出现了“**深度强化学习**”，它结合了深度学习与强化学习。


现代强化学习使用深度网络来进行学习，而不是由人们显式编码这些规则。我们将研究Q学习和深度Q学习，展示结合深度学习的强化学习与不结合深度学习的强化学习之间的区别。

强化学习被认为是通向一般智能的途径之一，其中计算机或智能体通过与现实世界、物体或实验互动或者通过反馈来进行学习。**训练强化学习智能体和训练狗很像，它们都是通过正、负激励进行的。**当你因为狗捡到球而奖励它一块饼干或者因为狗没捡到球而对它大喊大叫时，你就是在通过积极和消极的奖励向狗的大脑中强化知识。

**我们对AI智能体也做了同样的操作，但正奖励将是一个正数，负奖励将是一个负数。**尽管我们不能将强化学习视为与 CNN/RNN 等类似的另一种架构，但这里将其作为使用深度神经网络来解决实际问题的另一种方法，其配置如图1.17所示。

![img](https://mmbiz.qpic.cn/mmbiz_png/LSOjyib5giaVcSXA0iclQibOVRTFNQYOMwOoyLSmrR3DicHS6svpPfSImjI7k3ib4QcE82secR0kcnrQKULl0CGZyH0Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)