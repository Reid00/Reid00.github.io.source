---
title: "{{ .TranslationBaseName | replaceRE "^[0-9]{8}-" "" | replaceRE "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
author: ["Reid"]
categories: 
- Storage
tags: 
- 
keyword:
- Storage
description: {{ .TranslationBaseName | replaceRE "^[0-9]{8}-" "" | replaceRE "-" " " | title }}
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: {{ .TranslationBaseName | replaceRE "^[0-9]{8}-" ""  }}
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

