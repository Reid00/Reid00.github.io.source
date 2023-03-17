---
title: "Golang MurMur3"
date: 2023-03-16T19:34:59+08:00
lastmod: 2023-03-16T19:34:59+08:00
author: ["Reid"]
categories: 
- Golang
tags: 
- MurMur
- Golang
keyword:
- MurMur
- Golang
description: Golang MurMur3
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Golang-MurMur3
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


## 哈希
哈希（Hash）也称为散列，是把任意长度的输入通过哈希算法变换为固定长度的输出，这个输出值也就是散列值。

哈希表是根据键值对（key value）而直接进行访问的数据结构，通过将键值对映射到表中一个位置来访问记录，以加快查询速度。映射函数又称为散列函数，存放记录的数组叫做哈希表。

如果两个输入串的哈希函数的值相同则发生了碰撞（Collision），既然把任意较长字符串转化为固定长度且较短的字符串，因此必有一个输出串对应多个输入串，碰撞是必然存在的。这种碰撞又称为哈希冲突。

## 散列函数
哈希算法是一种广义的算法，也可以认为是一种思想，使用哈希算法可提高存储空间的利用率和数据查询效率。

- 哈希函数又称为散列函数，采用散列算法。
- 哈希函数是一种从任何一种数据中创建小的数字“指纹”的方法。
- 哈希函数将数据打乱混合，重新创建一个叫做散列值的“指纹”。
- 哈希函数会将消息或数据压缩成摘要，使得数据量变小，将数据的格式固定下来。

## Go 接口
Golang的hash包提供多种散列算法，比如`crc32/64`, `adler32`, `fnv`...
```go
type Hash interface{
  io.Writer //嵌入io.Writer接口，向执行中的hash加入更多数据。
  Sum(b []byte) []byte//将当前hash追加到字节数组b后面，不会改变当前hash状态。
  Reset()//重置hash到初始化状态
  Size() int//返回hash结果返回的字节数
  BlockSize() int//返回hash的集成块大小，为提高效率，Write方法传入的字节数最好是block size的倍数。
}
```

## MD5
MD5消息摘要算法，是一种被广泛使用的密码散列函数，可以产出一个128位（16子节）的散列值。

MD5已被证实无法防止碰撞，已经不算是很安全的算法，因此不适用于安全性认证，比如SSL公开密钥认证或数字签名等用途。

对于需要高度安全性的数据，一般建议改用其他算法，比如SHA256。
```go

input := "123456"

hash := md5.New()                   //创建散列值
n, err := hash.Write([]byte(input)) //写入待处理字节
if err != nil {
    fmt.Println(err, n)
    os.Exit(-1)
}
//bytes := hash.Sum([]byte(""))
bytes := hash.Sum(nil) //获取最终散列值的字符切片
fmt.Printf("%v\n", bytes)
//[225 10 220 57 73 186 89 171 190 86 224 87 242 15 136 62]

fmt.Printf("%x\n", bytes) //以16进制字符串格式化字符切片
//e10adc3949ba59abbe56e057f20f883e
```

MD5和SHA256是非常常用的两种单向散列函数
```go
import (
    "crypto/md5"
    "encoding/hex"
    "testing"
)

func MD5(input string) string {
    c := md5.New()
    c.Write([]byte(input))
    bytes := c.Sum(nil)
    return hex.EncodeToString(bytes)
}
```

## SHA-1
```go
password := "123456"

ins := sha1.New()
ins.Write([]byte(password))
result := ins.Sum([]byte(""))
fmt.Printf("%x\n", result)
//7c4a8d09ca3762af61e59520943dc26494f8941b
```

```go
import (
    "crypto/sha1"
    "encoding/hex"
    "testing"
)

func SHA1(input string) string {
    c := sha1.New()
    c.Write([]byte(input))
    bytes := c.Sum(nil)
    return hex.EncodeToString(bytes)
}

```

## CRC32
- CRC即Cyclic Redundancy Check循环冗余校验码
- CRC是实现32位循环冗余校验或CRC-32校验和

在远距离数据通信中，为确保高效而无差错地传送数据，必须对数据进行校验即差错控制。
CRC（Cyclic Redundancy Check/Code）循环冗余校验是对一个传送数据块进行校验，是一种高效的差错控制方法。
ChecksumIEEE使用IEEE多项式返回数据的CRC-32校验和
```go
package test

import (
    "hash/crc32"
    "testing"
)

func CRC32(input string) uint32 {
    bytes := []byte(input)
    return crc32.ChecksumIEEE(bytes)
}

func TestHash(t *testing.T) {
    input := "123456"
    t.Log(CRC32(input)) //158520161
}
```


## MurMur
我们有时候想将一段内容（比如字符串）转换成一个随机整数值，这里我们使用murmur3 hash算法可以达到这个目的
1）hash算法有可能发生碰撞，即不同的输入转换出的hash值是一样的，好的算法当然发生碰撞的概率会很小。
2）murmur3算法是非加密哈希算法
- 加密哈希函数旨在保证安全性，很难找到碰撞。即：给定的散列h很难找到的消息m；很难找到产生相同的哈希值的消息m1和m2。
- 非加密哈希函数只是试图避免非恶意输入的冲突。作为较弱担保的交换，它们通常更快。如果数据量小，或者不太在意哈希碰撞的频率，甚至可以选择生成哈希值小的哈希算法，占用更小的空间。

示例代码: 

```go
package main
 
import (
    "fmt"
    "github.com/spaolacci/murmur3"
)
 
func main() {
    originalStr := "pwww.google.com"
 
    // 注意：生成的hash值有三种取值，uint32，uint64，uint128，分别对应方法Sum32，Sum64，Sum128
    // 下面例子以Sum64为例
 
    // 1、使用默认种子，生成哈希值
    // 默认种子，其实是seed=0
    hValue1 := murmur3.Sum64([]byte(originalStr))
    fmt.Printf("hValue1 is %d\n", hValue1)
    // hValue1 is 13092418635223121727

    // 默认返回值是uint64, 转化为int64
    hValue1 := murmur3.Sum64([]byte(originalStr))
    fmt.Printf("hValue1 is %d\n", hValue1)
    // hValue1 is -5354325438486429889
 
    // 2、使用指定种子，生成哈希值
    seed := uint32(0000)
    hValue2 := murmur3.Sum64WithSeed([]byte(originalStr), seed)
    fmt.Printf("hValue2 is %d\n", hValue2)
    // hValue2 is 13092418635223121727
 
    // 3、使用指定种子，生成哈希值，2的另一种写法
    h := murmur3.New64WithSeed(seed)
    h.Write([]byte(originalStr))
    hValue3 := h.Sum64()
    fmt.Printf("hValue3 is %d\n", hValue3)
    // hValue3 is 13092418635223121727
 
    // 如果使用h继续计算其他值，则需要首先调用Reset，引为write这里是追加写
    h.Reset()
    h.Write([]byte(originalStr))
    hValue4 := h.Sum64()
    fmt.Printf("hValue4 is %d\n", hValue4)
    // hValue4 is 13092418635223121727
}

```