---
title: "Slidev Markdown 转PPT"
date: 2023-03-06T14:00:08+08:00
lastmod: 2023-03-06T14:00:08+08:00
author: ["Reid"]
categories: 
- Slidev
tags: 
- Slidev
- Markdown
- PPT
keyword:
- Slidev
description: ""
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Slidev markdown-转PPT
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
Slidev 使用一种扩展的 Markdown 格式，在一个纯文本文件中存储和组织你的幻灯片。这让你专注于制作内容。而且由于内容和样式是分开的，这也使得在不同的主题之间切换变得更加容易。

[官网](https://cn.sli.dev/)
[GitHub](https://github.com/slidevjs/slidev)

# 如何使用
## Node.js 的安装
参考[Node](https://nodejs.org/zh-cn/download/) 安装合适的版本

## Slidev 安装简介
### 本地创建
快速开始最好的方式就是使用官方的初始模板。

- 使用 NPM：
可以本地创建一个slidev 的文件夹，然后在此文件夹下目录的命令行中输入下面的命令:
```sh
npm install slidev
```

安装完成之后会生成一个 slidev 的文件夹，里面有一个demo 的md 文件。


- 使用 Yarn：
```sh
yarn create slid
```

### 命令行界面
创建之后，按 `ctrl + c` 结束demo， 如果想要再次打开，可以使用 `npx slidev`

### 全局安装
你可以使用如下命令在全局安装 Slidev：
```sh
npm i -g @slidev/cli
```
然后即可在任何地方使用 slidev，而无需每次都创建一个项目。
```sh
slidev xx.md
```

### 查看相关命令
```sh
$ slidev --help
slidev [args]

命令：
  slidev [entry]               Start a local server for Slidev          [默认值]
  slidev build [entry]         Build hostable SPA
  slidev format [entry]        Format the markdown file
  slidev theme [subcommand]    Theme related operations
  slidev export [entry]        Export slides to PDF
  slidev export-notes [entry]  Export slide notes to PDF

位置：
  entry  path to the slides markdown entry        [字符串] [默认值: "slides.md"]

选项：
  -t, --theme    override theme                                         [字符串]
  -p, --port     port                                                     [数字]
  -o, --open     open in browser                          [布尔] [默认值: false]
      --remote   listen public host and enable remote control           [字符串]
      --tunnel   open localtunnel to make Slidev available on the internet      
                                                          [布尔] [默认值: false]
      --log      log level
           [字符串] [可选值: "error", "warn", "info", "silent"] [默认值: "warn"]
      --inspect  enable the inspect plugin for debugging  [布尔] [默认值: false]
  -f, --force    force the optimizer to ignore the cache and re-bundle
                                                          [布尔] [默认值: false]
  -h, --help     显示帮助信息                                             [布尔]
  -v, --version  显示版本号                                               [布尔]

```

### Demo
输入`slidev xx.md` 如果第一次创建会提示不存在，会你是否创建，输入Y
```sh
zhangbl@DESKTOP-8NHU8UF MINGW64 /c/slidev
$ slidev kg.md
√ Entry file "kg.md" does not exist, do you want to create it? ... yes


  ●■▲
  Slidev  v0.40.3 (global)

  theme   @slidev/theme-seriph
  entry   C:\slidev\kg.md

  public slide show   > http://localhost:3030/
  presenter mode      > http://localhost:3030/presenter/
  remote control      > pass --remote to enable

  shortcuts           > restart | open | edit

```

在下面 shortcuts 出告诉你，你可以输入restart，open，edit 两个单词的首字母r,o,e 分别对应重新加载这个markdown,
在浏览器中打开这个markdown(以PPT 播放的模式), 或者在编辑器中编辑这个markdown。

- 更改主题 
打开markdown 文件，在头部改为:
```sh
# try also 'default' to start simple
theme: default
```
就会重新加载，如果不存在就会询问是否下载。
更多主题访问[这里](https://cn.sli.dev/themes/gallery.html)

- 简单语法
    - 用 `---` 来分割，表示下一页
    - 如果需要远程访， 可以用`slidev xx.md --remote`
    在remote control 中可以看到访问的url
    ```sh
    zhangbl@DESKTOP-8NHU8UF MINGW64 /c/slidev
    $ slidev kg.md --remote

    ●■▲
    Slidev  v0.40.3 (global)

    theme   @slidev/theme-default
    entry   C:\slidev\kg.md

    public slide show   > http://localhost:3030/
    presenter mode      > http://localhost:3030/presenter/   
    remote control      > http://10.10.63.148:3030/presenter/

    shortcuts           > restart | open | edit | qrcode 
    ```

- 直接使用主题创建
```sh
slidev -t vuetiful kg.md
```

- 问题 [vite] Internal server error 
```sh
Element is missing end tag.
16:55:28 [vite] Internal server error: Element is missing end tag.
  Plugin: vite:vue
  File: /@slidev/slides/1.md:10:4
  8  |    </span>
  9  |  </div>
  10 |  <p><a href="https://github.com/slidevjs/slidev" target="_blank" alt="GitHub"
     |      ^
  11 |    class="abs-br m-6 text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white"></p>
  12 |  <carbon-logo-github /></a>
      at createCompilerError (C:\Users\ld\AppData\Roaming\npm\node_modules\@slidev\cli\node_modules\@vue\compiler-core\dist\compiler-core.cjs.js:19:19)   
      at emitError (C:\Users\ld\AppData\Roaming\npm\node_modules\@slidev\cli\node_modules\@vue\compiler-core\dist\compiler-core.cjs.js:1613:29)
      at parseElement 
...
```
github 上有这个[issue](https://github.com/slidevjs/slidev/issues/645)
解决方式:
```sh
A temporary solution is to delete the enter after alt="Github".
```
删除xx.md 文件中alt="Github" 后面的换行
