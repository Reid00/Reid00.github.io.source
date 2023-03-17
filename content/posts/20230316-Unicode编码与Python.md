---
title: "Unicode编码与Python"
date: 2023-03-16T19:35:10+08:00
lastmod: 2023-03-16T19:35:10+08:00
author: ["Reid"]
categories: 
- Python
- 编码
tags: 
- 编码
- Unicode
keyword:
- Unicode
- Python
description: Unicode编码与Python
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Unicode编码与Python
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
这有篇很好的文章，可以明白这个问题:

为什么会报错“`UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)`”？本文就来研究一下这个问题。

字符串在`Python`内部的表示`是unicode`编码，因此，在做编码转换时，通常需要以`unicode`作为中间编码，即先将其他编码的字符串解码（`decode`）成`unicode`，再从`unicode`编码（`encode`）成另一种编码。

`decode`的作用是将其他编码的字符串转换成`unicode`编码，如`str1.decode('gb2312')`，表示将`gb2312`编码的字符串`str1`转换成`unicode`编码。

`encode`的作用是将`unicode`编码转换成其他编码的字符串，如`str2.encode('gb2312')`，表示将`unicode`编码的字符串`str2`转换成`gb2312`编码。

因此，转码的时候一定要先搞明白，字符串`str`是什么编码，然后`decode`成`unicode`，然后再`encode`成其他编码

代码中字符串的默认编码与代码文件本身的编码一致。

如：s='中文'

如果是在`utf8`的文件中，该字符串就是utf8编码，如果是在`gb2312`的文件中，则其编码为gb2312。这种情况下，要进行编码转换，都需 要先用decode方法将其转换成unicode编码，再使用encode方法将其转换成其他编码。通常，在没有指定特定的编码方式时，都是使用的系统默 认编码创建的代码文件。

如果字符串是这样定义：s=u'中文'

则该字符串的编码就被指定为unicode了，即python的内部编码，而与代码文件本身的编码无关。因此，对于这种情况做编码转换，只需要直接使用encode方法将其转换成指定编码即可。

如果一个字符串已经是unicode了，再进行解码则将出错，因此通常要对其编码方式是否为unicode进行判断：

isinstance(s, unicode) #用来判断是否为unicode

用非unicode编码形式的str来encode会报错

如何获得系统的默认编码？

```
#!/usr/bin/env python

#coding=utf-8

import sys

print sys.getdefaultencoding()
```

该段程序在英文WindowsXP上输出为：`ascii`

在某些`IDE`中，字符串的输出总是出现乱码，甚至错误，其实是由于IDE的结果输出控制台自身不能显示字符串的编码，而不是程序本身的问题。

如在UliPad中运行如下代码：

```
s=u"中文"

print s
```

会提示：`UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)`。这是因为UliPad在英文WindowsXP上的控制台信息输出窗口是按照ascii编码输出的（英文系统的默认编码是 ascii），而上面代码中的字符串是`Unicode`编码的，所以输出时产生了错误。

将最后一句改为：`print s.encode('gb2312')`

则能正确输出“中文”两个字。

若最后一句改为：`print s.encode('utf8')`

则输出：`\xe4\xb8\xad\xe6\x96\x87`，这是控制台信息输出窗口按照ascii编码输出utf8编码的字符串的结果。

`unicode(str,'gb2312')`与`str.decode('gb2312')`是一样的，都是将gb2312编码的str转为unicode编码

使用`str.__class__`可以查看str的编码形式

```
>>>>>

groups.google.com/group/python-cn/browse_thread/thread/be4e4e0d4c3272dd

-----
```

python是个容易出现编码问题的语言。所以，我按照我的理解写下下面这些文字。

### 1. 首先，要了解几个概念。

字节：计算机数据的表示。8位二进制。可以表示无符号整数：0-255。下文，用“字节流”表示“字节”组成的串。

字符：英文字符“abc”，或者中文字符“你我他”。字符本身不知道如何在计算机中保存。下文中，会避免使用“字符串”这个词，而用“文本”来表

示“字符”组成的串。

编码（动词）：按照某种规则（这个规则称为：编码（名词））将“文本”转换为“字节流”。（在python中：unicode变成str）

解码（动词）：将“字节流”按照某种规则转换成“文本”。（在`Python`中：str变成unicode）

实际上，任何东西在计算机中表示，都需要编码。例如，视频要编码然后保存在文件中，播放的时候需要解码才能观看。

`unicode：unicode`定义了，一个“字符”和一个“数字”的对应，但是并没有规定这个“数字”在计算机中怎么保存。（就像在C中，一个整数既

可以是int，也可以是`short`。`unicode`没有规定用int还是用`short`来表示一个“字符”）

`utf8`：`unicode`实现。它使用`unicode`定义的“字符”“数字”映射，进而规定了，如何在计算机中保存这个数字。其它的`utf16`等都是 `unicode`实现。

`gbk`：类似utf8这样的“编码”。但是它没有使用`unicode`定义的“字符”“数字”映射，而是使用了另一套的映射方法。而且，它还定义了如何在计算机中保存。

### 2. python中的encode，decode方法

首先，要知道`encode`是 `unicode`转换成`str`。`decode`是str转换成unicode。

下文中，u代表unicode类型的变量，s代表str类型的变量。

`u.encode('...')`基本上总是能成功的，只要你填写了正确的编码。就像任何文件都可以压缩成`zip`文件。

`s.decode('...')`经常是会出错的，因为`str`是什么“编码”取决于上下文，当你解码的时候需要确保s是用什么编码的。就像，打开zip文件的时候，你要确保它确实是zip文件，而不仅仅是伪造了扩展名的zip文件。

`u.decode()`,`s.encode()`不建议使用，s.encode相当于s.decode().encode()首先用默认编码（一般是ascii）转换成unicode在进行encode。

### 3. 关于#coding=utf8=

当你在py文件的第一行中，写了这句话，并确实按照这个编码保存了文本的话，那么这句话有以下几个功能。

1.使得词法分析器能正常运作，对于注释中的中文不报错了。

2.对于u"中文"这样`literal string`能知道两个引号中的内容是utf8编码的，然后能正确转换成unicode

3."中文"对于这样的literal string你会知道，这中间的内容是utf8编码，然后就可以正确转换成其它编码或unicode了。

### 4. Python编码和Windows控制台

我发现，很多初学者出错的地方都在print语句，这牵涉到控制台的输出。我不了解linux，所以只说控制台的。

首先，`Windows`的控制台确实是`unicode`（utf16_le编码）的，或者更准确的说使用字符为单位输出文本的。

但是，程序的执行是可以被重定向到文件的，而文件的单位是“字节”。

所以，对于C运行时的函数printf之类的，输出必须有一个编码，把文本转换成字节。可能是为了兼容95，98，

没有使用unicode的编码，而是mbcs（不是gbk之类的）。

windows的mbcs，也就是ansi，它会在不同语言的windows中使用不同的编码，在中文的windows中就是gb系列的编码。

这造成了同一个文本，在不同语言的windows中是不兼容的。

现在我们知道了，如果你要在windows的控制台中输出文本，它的编码一定要是“mbcs”。

对于python的unicode变量，使用print输出的话，会使用sys.getfilesystemencoding()返回的编码，把它变成str。

如果是一个utf8编码str变量，那么就需要 print s.decode('utf8').encode('mbcs')

最后，对于str变量，file文件读取的内容，urllib得到的网络上的内容，都是以“字节”形式的。

它们如果确实是一段“文本”，比如你想print出来看看。那么你必须知道它们的编码。然后decode成unicode。

如何知道它们的编码：

1. 事先约定。（比如这个文本文件就是你自己用utf8编码保存的）
2. 协议。（python文件第一行的#coding=utf8，html中的等）
3. 猜。

> 这个非常好，但还不是很明白将“文本”转换为“字节流”。（在python中：unicode变成str）

"最后，对于str变量，file文件读取的内容，urllib得到的网络上的内容，都是以“字节”形式的。"

虽然文件或者网页是文本的,但是在保存或者传输时已经被编码成bytes了,所以用"rb"打开的file和从socket读取的流是基于字节的.

"它们如果确实是一段“文本”，比如你想print出来看看。那么你必须知道它们的编码。然后decode成unicode。"

这里的加引号的"文本",其实还是字节流(bytes),而不是真正的文本(unicode),只是说明我们知道他是可以解码成文本的.

在解码的时候,如果是基于约定的,那就可以直接从指定地方读取如BOM或者python文件的指定coding或者网页的meta,就可以正确解码,

但是现在很多文件/网页虽然指定了编码,但是文件格式实际却使用了其他的编码(比如py文件指定了coding=utf8,但是你还是可以保存成ansi--记事本的默认编码),这种情况下真实的编码就需要去猜了

解码了的文本只存在运行环境中,如果你需要打印/保存/输出给数据库/网络传递,就又需要一次编码过程,这个编码与上面的编码没有关系,只是依赖于你的选择,但是这个编码也不是可以随便选择的,因为编码后的bytes如果又需要传递给其他人/环境,那么如果你的编码也不遵循约定,又给下一个人/环境造成了困扰,于是递归之~~~~

主要有一条非常容易误解：

> 一般人会认为Unicode（广义）统一了编码，其实不然。Unicode不是唯一的编码，而一大堆编码的统称。但是Windows下Unicode（狭义）一般特指UCS2，也就是UTF-16/LE

unicode作为字符集(ucs)是唯一的,编码方案(utf)才是有很多种

将字符与字节的概念区分开来是很重要的。Java 一直就是这样，Python也开始这么做了，Ruby 貌似还在混乱当中。

我也说两句。我对编码的研究相对比较深一些。因为工作中也经常遇到乱码，于是在05年，对编码专门做过研究，并在公司刊物上发过文章，最后形成了一个教材，每年在公司给新员工都讲一遍。于是项目中遇到乱码的问题就能很快的定位并解决了。

理论上，从一个字符到具体的编码，会经过以下几个概念。

- 字符集（`Abstract character repertoire`）
- 编码字符集（`Coded character set`）
- 字符编码方式（`Character encoding form`）
- 字符编码方案（`Character encoding scheme`）
- 字符集：就算一堆抽象的字符，如所有中文。字符集的定义是抽象的，与计算机无关。
- 编码字符集：是一个从整数集子集到字符集抽象元素的映射。即给抽象的字符编上数字。如`gb2312`中的定义的字符，每个字符都有个整数和它对应。一个整数只对应着一个字符。反过来，则不一定是。这里所说的映射关系，是数学意义上的映射关系。编码字符集也是与计算机无关的。`unicode`字符集也在这一层。
- 字符编码方式：这个开始与计算机有关了。编码字符集的编码点在计算机里的具体表现形式。通俗的说，意思就是怎么样才能将字符所对应的整数的放进计算机内存，或文件、或网络中。于是，不同人有不同的实现方式，所谓的万码奔腾，就是指这个。gb2312，utf-8,utf-16,utf-32等都在这一层。
- 字符编码方案：这个更加与计算机密切相关。具体是与操作系统密切相关。主要是解决大小字节序的问题。对于UTF-16和UTF-32

编码，`Unicode`都支持`big-endian`和`little-endian`两种编码方案。

一般来说，我们所说的编码，都在第三层完成。具体到一个软件系统中，则很复杂。

浏览器－apache－tomcat（包括tomcat内部的jsp编码、编译，文件读取）－数据库之间，只要存在数据交互，就有可能发生编码不一致，如果在读取数据时，没有正确的`decode`和`encode`，出现乱码就是家常便饭了。