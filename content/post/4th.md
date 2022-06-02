---
title: "4th"
date: 2022-06-02T09:46:54+08:00
lastmod: 2022-06-02T09:46:54+08:00
author: ["Reid"]
categories: 
- 
tags: 
- 
series:
- 
description: ""
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: ""
draft: false # 是否为草稿
comments: true
showToc: true # 显示目录
TocOpen: true # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
disableShare: true # 底部不显示分享栏
showbreadcrumbs: true #顶部显示当前路径
cover:
    image: ""
    caption: ""
    alt: ""
    relative: false
---

4th file

```go
func copyBuf(key, value []byte) []byte {

	buf := make([]byte, len(key)+len(value))

	copy(buf[:len(key)], key)
	copy(buf[len(key):], value)
	return buf
}
```

I want to check why not hmtl