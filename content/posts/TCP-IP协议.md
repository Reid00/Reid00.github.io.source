---
title: "TCP IP协议"
date: 2022-06-08T11:39:22+08:00
lastmod: 2022-06-08T11:39:22+08:00
author: ["Reid"]
categories: 
- OS
tags: 
- TCP
- IP
keyword:
- OS
- 网络
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
<meta name="referrer" content="no-referrer" />
## TCP/IP 协议族

通常我说 TCP/IP 是指 TCP/IP 协议族。它是基于 TCP 和 IP 这两个最初的协议之上的不同的通信协议的大集合。
例如：http、https、ftp、icmp、arp、rarp、smtp（简单邮件传输协议）

![img](https://mmbiz.qpic.cn/mmbiz_png/VVR9iar1ILuNeOwB4d6tZicHHKP4plU4Z875WFgzGLsMqu47EKIn94hDRiaF6WX0dQILGZsDO2rVddAzHkSnqfcrw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

>当输入 xxxxHub 后，到网页显示，其间发生了什么？这问题被面试官问了五六十次，熬夜赶出这篇文章
>
>https://mp.weixin.qq.com/s/ESJ8Zt0GBVXHKj3KICoqjg



## 一个网络请求是怎么传输的？

我们拿访问浏览器举个栗子，如图所示：

![img](https://mmbiz.qpic.cn/mmbiz_png/VVR9iar1ILuNeOwB4d6tZicHHKP4plU4Z8b30XibA3yzuFe65Idvr1LP2aOAXcVUUzOQcQUCjOBKLhD4TtT3FOgTA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## TCP、UDP有什么区别？各有什么优劣？

TCP 面向连接，提供可靠交付。通过 TCP 连接传输的数据，无差错、不丢失、不重复、并且按序到达。相对 UDP 开销大
UDP 面向无连接，不保证可靠交付。无拥塞控制，支持一对一、一对多、多对多，开销小。

## 关于 TCP 协议

![img](https://mmbiz.qpic.cn/mmbiz_png/VVR9iar1ILuNeOwB4d6tZicHHKP4plU4Z8bLKdMTorLDhGZ2S9DqFq2aOSHqDKDyepjQa75ExibJib5IAUkpvpzUOA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

- 确认 ACK - ACKnowledgement 仅当ACK = 1 时，确认才有效。简单来说，就是确认收到数据。
- 复位 RST - ReSet 标明 TCP 出现严重差错时，必须释放连接，重新建立连接。
- 同步 SYN - SYNchronization 在建立连接时，用来同步序号。当 SYN = 1，ACK = 0 时，表名这是一个连接请求报文。SYN = 1，ACK = 1 表示这是一个同意请求报文。
- 终止 FNI - FINis（表示终、完）用来释放连接。当 FNI = 1 表示此段报文发送方已发送完毕。

## 关于 UDP 协议

![img](https://mmbiz.qpic.cn/mmbiz_png/VVR9iar1ILuNeOwB4d6tZicHHKP4plU4Z8NEibbtzvE1ks9jZzgCzlJckCibyBKQK4Y9FgUKyRgLIOdxibtNRH97xqg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

## 解释三次握手

- 确认号 ack 期望收到对方下一个报文的序列号

- 序列号 seq

  ![img](https://mmbiz.qpic.cn/mmbiz_png/VVR9iar1ILuNeOwB4d6tZicHHKP4plU4Z8iag8FwkiaCOf3XsSekQOpkHoCYDhroyV0lsOtSJY7xfbr4lHY5zrEX8Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

1. SYN = 1 请求同步序列号，A 的序列号为：x
2. SYN = 1 ACK = 1，表示确认请求。B 发送的数据的序列号为：y，期望收到 下一个 A 的数据的序列号为：x + 1
3. ACK = 1 ，表示确认请求。A 发送的数据的序列号为：x + 1，期望收到下一个 B 的数据的序列号为：y + 1

## 说说TCP三次握手？为什么不两次？

如果发送两次就可以建立连接话，那么只要客户端发送一个连接请求，服务端接收到并发送了确认，就会建立一个连接。

可能出现的问题：如果一个连接请求在网络中跑的慢，超时了，这时客户端会从发请求，但是这个跑的慢的请求最后还是跑到了，然后服务端就接收了两个连接请求，然后全部回应就会创建两个连接，浪费资源！

如果加了第三次客户端确认，客户端在接受到一个服务端连接确认请求后，后面再接收到的连接确认请求就可以抛弃不管了。

## 说说TCP四次挥手？为什么不是三次？

据传输结束后，通信的双方都可以释放连接。现在 A 和 B 都处于 ESTABLISHED 状态。

![img](https://mmbiz.qpic.cn/mmbiz_png/VVR9iar1ILuNeOwB4d6tZicHHKP4plU4Z8mkh6oljy6jc49HMS8OMlmeQyZXylrBDjIoXpEaibPE5xX42Ovc88WJA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

第一次挥手：A 的应用进程先向其 TCP 发出连接释放报文段，并停止再发送数据，主动关闭 TCP 连接。A 把连接释放报文段首部的终止控制位 FIN 置 1，其序号 seq = u（等于前面已传送过的数据的最后一个字节的序号加 1），这时 A 进入 FIN-WAIT-1（终止等待1）状态，等待 B 的确认。请注意：TCP 规定，FIN 报文段即使不携带数据，也将消耗掉一个序号。

第二次挥手：B 收到连接释放报文段后立即发出确认，确认号是 ack = u + 1，而这个报文段自己的序号是 v（等于 B 前面已经传送过的数据的最后一个字节的序号加1），然后 B 就进入 CLOSE-WAIT（关闭等待）状态。TCP 服务端进程这时应通知高层应用进程，因而从 A 到 B 这个方向的连接就释放了，这时的 TCP 连接处于半关闭（half-close）状态，即 A 已经没有数据要发送了，但 B 若发送数据，A 仍要接收。也就是说，从 B 到 A 这个方向的连接并未关闭，这个状态可能会持续一段时间。A 收到来自 B 的确认后，就进入 FIN-WAIT-2(终止等待2)状态，等待 B 发出的连接释放报文段。

第三次挥手：若 B 已经没有要向 A 发送的数据，其应用进程就通知 TCP 释放连接。这时 B 发出的连接释放报文段必须使 FIN = 1。假定 B 的序号为 w（在半关闭状态，B 可能又发送了一些数据）。B 还必须重复上次已发送过的确认号 ack = u + 1。这时 B 就进入 LAST-ACK(最后确认)状态，等待 A 的确认。

第四次挥手：A 在收到 B 的连接释放报文后，必须对此发出确认。在确认报文段中把 ACK 置 1，确认号 ack = w + 1，而自己的序号 seq = u + 1（前面发送的 FIN 报文段要消耗一个序号）。然后进入 TIME-WAIT(时间等待) 状态。请注意，现在 TCP 连接还没有释放掉。必须经过时间等待计时器设置的时间 2MSL（MSL：最长报文段寿命）后，A 才能进入到 CLOSED 状态，然后撤销传输控制块，结束这次 TCP 连接。当然如果 B 一收到 A 的确认就进入 CLOSED 状态，然后撤销传输控制块。所以在释放连接时，B 结束 TCP 连接的时间要早于 A。

## 什么是拥塞控制？

简单来说，就是通过网络的拥塞情况来调整 TCP 发送端发送的数据量。发送量先由 1 指数级递增，到一定量时（65535 个字节）开始慢下来，这个时候还是递增的。等到开始丢包时，又开始降低发送速度。

## 什么是流量控制？

简单来说，就是 TCP 的接受端处理不过来，让 TCP 的发送端发送慢一点。接收端会维护一个处理窗口，即是接收端所能处理数据的能力。接收端将这个处理能力不断反馈给发送端，以此来让发送端调整发送的数据量的多少。

---

参考: https://mp.weixin.qq.com/s/xe3dEu17mGTqM46LRFxzhg