---
title: "Utterances 给 Hugo PaperMod 主题添加评论系统"
date: 2022-06-08T17:45:08+08:00
lastmod: 2022-06-08T17:45:08+08:00
author: ["Reid"]
categories: 
- Hugo
tags: 
- PaperMod
- 评论
- Comment
keyword:
- Hugo
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

# 安装 Utterances
首先要有一个 GitHub 仓库。如果是用 GitHub Page 托管网站就可以不需要额外创建，就用你的GitHub Page repositroy 如:<username>.github.io 仓库, 当然也可以自己重新创建一个，用来存放评论。但是需要注意的是这个仓库必须是Public 的。
比如我的为https://github.com/Reid00/hugo-blog-talks

然后去 https://github.com/apps/utterances 安装 utterances。

在打开的页面中选择`Only select repositories`，并在下拉框中选择自己的博客仓库（比如我就是 `Reid00/hugo-blog-talks`，也可以安装到其他仓库, 也可以所有仓库，但是不推荐），然后点击 Install。
![install](https://raw.githubusercontent.com/Reid00/image-host/main/20220608/image.3pq7t1csfb80.webp)

# 配置Hugo
复制以下代码，repo 要修改成自己的仓库，repo 为你存放评论的仓库。
```sh
<script src="https://utteranc.es/client.js"
    repo="Reid00/hugo-blog-talks"
    issue-term="pathname"
    label="Comment"
    theme="github-light"
    crossorigin="anonymous"
    async>
</script>
```
在主题配置目录下创建 `layouts/partials/comments.html` 文件，并添加上述内容
```sh
{{- /* Comments area start */ -}}
{{- /* to add comments read => https://gohugo.io/content-management/comments/ */ -}}
<script src="https://utteranc.es/client.js"
    repo="Reid00/hugo-blog-talks"
    issue-term="pathname"
    label="Comment"
    theme="github-light"
    crossorigin="anonymous"
    async>
</script>
{{- /* Comments area end */ -}}
```
然后根据 PaperMod 文档，打开 config.yml 文件，添加以下内容
```sh
params:
  comments: true
```

# 问题
如果你用GitHub Action 部署的GitHub Page, 并且你的workflow 里面写了
```sh
- name: Check out repository code
uses: actions/checkout@v3
with:
    submodules: recursive  # Fetch Hugo themes (true OR recursive)
    fetch-depth: 0   
```
这个时候，theme 主题会自动pull 源主题的repo，覆盖`layouts/partials/comments.html` 文件， 此时，你可以在项目的`layouts` 创建改文件和内容即可。