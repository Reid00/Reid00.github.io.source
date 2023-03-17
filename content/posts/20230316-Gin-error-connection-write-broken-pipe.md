---
title: "Gin Error Connection Write Broken Pipe"
date: 2023-03-16T19:34:51+08:00
lastmod: 2023-03-16T19:34:51+08:00
author: ["Reid"]
categories: 
- Golang
- Gin
tags: 
- Golang
- Gin
keyword:
- Golang
description: Gin Error Connection Write Broken Pipe
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Gin-error-connection-write-broken-pipe
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

# 简介
最近使用Gin 框架写接口，总是会出现一些`write: connection reset by peer` 或者 `write: broken pipe` 的错误, 在查询资料的时候，发现TCP的下面的情况可以触发一下两种错误。
另外Gin 的出现这个错误的原因这边有个分析[Gin-RST](https://testerhome.com/articles/23296)
大概原因就是DB 连接池太小，有大量请求排队等待空闲链接，排队时间越长积压的请求越多，请求处理耗时越大，直到积压请求太多把句柄打满，出现了死锁。

# write: broken pipe
触发原因:

服务器接收第一个客户端字节并关闭连接。已关闭的服务端 在收到 客户端的下一个字节写入 将导致服务器用 `RST` 数据包进行应答。当向接收 `RST` 的 `socket` 发送更多字节时，该`socket`将返回`broken pipe`。这就是客户机向服务器发送最后一个字节时发生的情况。

经过测试:
向一个已经关闭的`socket` 写入数据，(无论buffer 是否写满) 都会出现第一次返回RST， 第二次写入出现`broken pipe error`, 读的话是`EOF`

```go
package main

import (
    "errors"
    "log"
    "net"
    "os"
    "syscall"
    "time"
)

func server() {
    listener, err := net.Listen("tcp", ":8080")
    if err != nil {
        log.Fatal(err)
    }

    defer listener.Close()

    conn, err := listener.Accept()
    if err != nil {
        log.Fatal("server", err)
        os.Exit(1)
    }
    data := make([]byte, 1)
    if _, err := conn.Read(data); err != nil {
        log.Fatal("server", err)
    }

    conn.Close()
}

func client() {
    conn, err := net.Dial("tcp", "localhost:8080")
    if err != nil {
        log.Fatal("client", err)
    }

    // write to make the connection closed on the server side
    if _, err := conn.Write([]byte("a")); err != nil {
        log.Printf("client: %v", err)
    }

    time.Sleep(1 * time.Second)

    // write to generate an RST packet
    if _, err := conn.Write([]byte("b")); err != nil {
        log.Printf("client: %v", err)
    }

    time.Sleep(1 * time.Second)

    // write to generate the broken pipe error
    if _, err := conn.Write([]byte("c")); err != nil {
        log.Printf("client: %v", err)
        if errors.Is(err, syscall.EPIPE) {
            log.Print("This is broken pipe error")
        }
    }
}

func main() {
    go server()

    time.Sleep(3 * time.Second) // wait for server to run

    client()
}

```

# connection reset by peer
触发原因:
如果服务器用`socket`接收缓冲区中剩余的字节关闭连接，那么将向客户端发送一个 RST 数据包。当客户端尝试从这样一个关闭的连接中读取时，它将通过对等错误获得连接重置。

经过测试: 当向一个写满了缓冲区，并关闭的socket 进行read 或者write 操作都会导致`connection reset by peer`


```go
package main

import (
    "errors"
    "log"
    "net"
    "os"
    "syscall"
    "time"
)

func server() {
    listener, err := net.Listen("tcp", ":8080")
    if err != nil {
        log.Fatal(err)
    }

    defer listener.Close()

    conn, err := listener.Accept()
    if err != nil {
        log.Fatal("server", err)
        os.Exit(1)
    }
    data := make([]byte, 2)
    if _, err := conn.Read(data); err != nil {
        log.Fatal("server", err)
    }

    conn.Close()
}

func client() {
    conn, err := net.Dial("tcp", "localhost:8080")
    if err != nil {
        log.Fatal("client", err)
    }

    if _, err := conn.Write([]byte("abc")); err != nil {
        log.Printf("client: %v", err)
    }

    time.Sleep(1 * time.Second) // wait for close on the server side
    // 下面的操作第一次read /write 都会 出现ECONNRESET  reset by peer
    // 第二次的读则是EOF， 如果是写则是`write: broken pipe`

    // if _, err := conn.Write([]byte("ab")); err != nil {
    //     log.Printf("client: %v", err)
    // }

    data := make([]byte, 1)
    if _, err := conn.Read(data); err != nil {
        log.Printf("client: %v", err)
        if errors.Is(err, syscall.ECONNRESET) {
            log.Print("This is connection reset by peer error")
        }
    }
}

func main() {
    go server()

    time.Sleep(3 * time.Second) // wait for server to run

    client()
}
```
