---
title: "Raft Etcd 之 Linearizable Read"
date: 2023-02-10T14:40:20+08:00
lastmod: 2023-02-10T14:40:20+08:00
author: ["Reid"]
categories: 
- Storage
- Raft
tags: 
- Raft
- MIT6.824
- Consensus
- 共识算法
keyword:
- Storage
- Raft
- MIT6.824
- Consensus
- 共识算法
description: ""
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Raft-Etcd-之Linearizable Read
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

# 介绍
linearizable read 简单的说就是不返回 stale 数据，具体可以参考[Strong consistency models](https://aphyr.com/posts/313-strong-consistency-models)

Read Index 机制就是 Leader 在收到读请求时进行如下几步：
1. 如果 Leader 在当前任期还没有提交过日志，先提交一条空日志
2. Leader 保存记录当前 commit index 作为 readIndex
3. 通过心跳，询问成员自己还是不是 Leader，如果收到过半的确认，则可确信自己仍是 Leader
4. 等待 Apply Index 超过 readIndex
5. 读取数据，响应 Client

etcd不仅实现了leader上的read only query，同时也实现了follower上的read only query，原理是一样的，只不过读请求到达follower时，commit index是需要向leader去要的，leader返回commit index给follower之前，同样，需要走上面的ReadIndex流程，因为leader同样需要check自己到底还是不是leader

# ReadIndex 思路
在[论文](https://raft.github.io/raft.pdf)中 第八节，page13 有提到过大概思路:
>Read-only operations can be handled without writing anything into the log. However, with no additional measures, this would run the risk of returning stale data, since the leader responding to the request might have been superseded by a newer leader of which it is unaware. Linearizable reads must not return stale data, and Raft needs two extra precautions to guarantee this without using the log. First, a leader must have the latest information on which entries are committed. The Leader Completeness Property guarantees that a leader has all committed entries, but at the start of its term, it may not know which those are. To find out, it needs to commit an entry from its term. Raft handles this by having each leader commit a blank no-op entry into the log at the start of its term. Second, a leader must check whether it has been deposed before processing a read-only request (its information may be stale if a more recent leader has been elected). Raft handles this by having the leader exchange heartbeat messages with a majority of the cluster before responding to read-only requests. Alternatively, the leader could rely on the heartbeat mechanism to provide a form of lease [9], but this would rely on timing for safety (it assumes bounded clock skew).

在收到读请求时，leader 节点保存下当前的 commit index，并往 peers 发送心跳。如果确定该节点依然是 leader，则只需要等到该 commit index 的 log entry 被 apply 到状态机时就可以返回客户端结果。

# LeaseRead 思路
LeaseRead 与 ReadIndex 类似，但更进一步，不仅省去了 Log，还省去了网络交互。它可以大幅提升读的吞吐也能显著降低延时。基本的思路是 Leader 取一个比 Election Timeout 小的租期，在租期不会发生选举，确保 Leader 不会变，所以可以跳过 ReadIndex 的第二步，也就降低了延时。 LeaseRead 的正确性和时间挂钩，因此时间的实现至关重要，如果漂移严重，这套机制就会有问题。

Wait Free
到此为止 Lease 省去了 ReadIndex 的第二步，实际能再进一步，省去第 3 步。这样的 LeaseRead 在收到请求后会立刻进行读请求，不取 commit index 也不等状态机。由于 Raft 的强 Leader 特性，在租期内的 Client 收到的 Resp 由 Leader 的状态机产生，所以只要状态机满足线性一致，那么在 Lease 内，不管何时发生读都能满足线性一致性。有一点需要注意，只有在 Leader 的状态机应用了当前 term 的第一个 Log 后才能进行 LeaseRead。因为新选举产生的 Leader，它虽然有全部 committed Log，但它的状态机可能落后于之前的 Leader，状态机应用到当前 term 的 Log 就保证了新 Leader 的状态机一定新于旧 Leader，之后肯定不会出现 stale read。
可以参考[post](https://cn.pingcap.com/blog/linearizability-and-raft#%E7%BA%BF%E6%80%A7%E4%B8%80%E8%87%B4%E6%80%A7%E5%92%8C-raft)

# Etcd 源码实现
先留个坑，暂时没时间，后续有时间再分析。