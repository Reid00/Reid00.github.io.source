---
title: "WebAssembly(Wasm) 教程"
date: 2023-08-15T19:34:12+08:00
lastmod: 2023-08-15T19:34:12+08:00
author: ["Reid"]
categories: 
- WASM
- Rust
- Go
tags: 
- WASM
- Go
- Rust
keyword:
- WASM
description: WebAssembly(Wasm) 教程
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: WebAssembly(Wasm) 教程
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

# WebAssembly 简介
WebAssembly (有时缩写为 Wasm)为可执行程序定义了一种可移植的二进制代码格式和相应的文本格式以及软件接口，用于促进这些程序与其宿主环境之间的交互。
WebAssembly 的主要目标是在网页上启用高性能的应用程序，“但是它不会做出任何特定于 Web 的假设或提供特定于 Web 的特性，因此它也可以在其他环境中使用。”它是一个开放标准 ，旨在支持任何操作系统上的任何语言，实际上，所有最流行的语言都至少有一定程度的支持。
[from wasm](https://en.wikipedia.org/wiki/WebAssembly)
> WebAssembly (sometimes abbreviated Wasm) defines a portable binary-code format and a corresponding text format for executable programs as well as software interfaces for facilitating interactions between such programs and their host environment.
> The main goal of WebAssembly is to enable high-performance applications on web pages, "but it does not make any Web-specific assumptions or provide Web-specific features, so it can be employed in other environments as well."[7] It is an open standard[8][9] and aims to support any language on any operating system,[10] and in practice all of the most popular languages already have at least some level of support.

1. WebAssembly 是一种二进制编码格式，而不是一门新的语言。
2. WebAssembly 不是为了取代 JavaScript，而是一种补充（至少现阶段是这样），结合 WebAssembly 的性能优势，很大可能集中在对性能要求高（例如游戏，AI），或是对交互体验要求高（例如移动端）的场景。
3. C/C++ 等语言可以编译 WebAssembly 的目标文件，也就是说，其他语言可以通过编译器支持，而写出能够在浏览器前端运行的代码。

# Rust 如何使用WASM
完整项目看[此处](https://github.com/Reid00/rust-wasm-sample/tree/main/mywasm)
## 安装
1. 安装Rust, 参考[官网](https://www.rust-lang.org/tools/install)
2. install wasm-pack `cargo install wasm-pack`
3. [可选] install cargo-generate `cargo install cargo-generate`
4. Python3 用于启动一个简单的 HTTP 服务器

## 案例
1. 创建一个rust lib 项目 `cargo new --lib hello-wasm`
2. 打开项目,结构如下
```sh
-rw-r--r-- 1 zhangbl 197121 3203 Aug 16 15:41 Cargo.lock
-rw-r--r-- 1 zhangbl 197121  224 Aug 16 15:51 Cargo.toml
-rw-r--r-- 1 zhangbl 197121  314 Aug 16 17:35 index.html # 后面新建的
drwxr-xr-x 1 zhangbl 197121    0 Aug 16 18:13 pkg/       # 后面生成的
drwxr-xr-x 1 zhangbl 197121    0 Aug 16 15:27 src/      
drwxr-xr-x 1 zhangbl 197121    0 Aug 16 16:01 target/ 
```

打开src/lib.rs, 删除原先内容，用以下内容取代:
```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
extern {
    pub fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}!", name));
}
```

同时在cargo.toml 新增下面内容:
```toml
[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen="0.2"
```

3. 代码解析
- `use wasm_bindgen::prelude::*;`：导入了 wasm_bindgen 库的预导入（prelude）模块，它包含了一些常用的宏和类型。这样可以方便地在代码中使用 wasm_bindgen 提供的功能。
- `#[wasm_bindgen]`：这是一个属性宏，用于标记下面的函数和外部接口需要与 JavaScript 进行绑定
- `extern 块`：在 extern 块内部使用 pub fn alert(s: &str) 定义了一个外部函数接口。这个函数声明了一个参数 s，类型为字符串引用（&str）。 **从 Rust 调用 JavaScript 中的外部函数**
- `pub fn greet(name: &str)`：这是一个公共函数 greet 的定义，它接受一个字符串引用参数 name。**生成 JavaScript 可以调用的 Rust 函数**
- `alert(&format!("Hello, {}!", name))`：在 greet 函数中调用了外部接口函数 alert。它使用 format! 宏将传入的 name 参数插入到格式化的字符串中，然后调用 alert 函数显示警告框，内容为拼接好的问候信息。

4. toml 解析
[lib] 告诉编译器，将要编译的类型是c 语言的动态类型 库

5. 编译
`wasm-pack build --target web` 请注意这步很慢，耗时会很久，请去喝茶。
编译完成之后，出现pkg 包，里面提供了我们项目名的mywasm_bg.wasm 
```sh
total 38
-rw-r--r-- 1 zhangbl 197121  1116 Aug 16 17:39 mywasm.d.ts        
-rw-r--r-- 1 zhangbl 197121  4910 Aug 16 17:39 mywasm.js
-rw-r--r-- 1 zhangbl 197121  2503 Aug 16 16:03 mywasm_bg.js       
-rw-r--r-- 1 zhangbl 197121 17307 Aug 16 18:13 mywasm_bg.wasm     
-rw-r--r-- 1 zhangbl 197121   287 Aug 16 17:39 mywasm_bg.wasm.d.ts
-rw-r--r-- 1 zhangbl 197121   213 Aug 16 18:13 package.json  
```
6. 在项目目录下，新建index.html
```html
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>hello-wasm example</title>
</head>

<body>
    <script type="module">
        import init, { greet } from "./pkg/mywasm.js";
        init().then(() => {
            greet("WebAssembly")
        });
    </script>
</body>

</html>
```

7. 运行 `python -m http.server` 启动一个简单的web 服务, 让后访问 `http://localhost:8000`
![hello](https://cdn.staticaly.com/gh/Reid00/picx-images-hosting@master/20230816/image.35alc2e7oya0.png)


# Go 如何使用WASM (未完待续)
## Hello world
1. 新建main.go, 使用 js.Global().get(‘alert’) 获取全局的 alert 对象，通过 Invoke 方法调用。等价于在 js 中调用 window.alert("Hello World")。

```golang

package main

import "syscall/js"

func main() {
	alert := js.Global().Get("alert")
	alert.Invoke("Hello World!")
}
```

2. 将 main.go 编译为 static/main.wasm
`GOOS=js GOARCH=wasm go build -o static/main.wasm`

3. 拷贝 wasm_exec.js (JavaScript 支持文件，加载 wasm 文件时需要) 到 static 文件夹
`cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" static`

4. 创建 index.html，引用 static/main.wasm 和 static/wasm_exec.js。
```html
<html>
<script src="static/wasm_exec.js"></script>
<script>
	const go = new Go();
	WebAssembly.instantiateStreaming(fetch("static/main.wasm"), go.importObject)
		.then((result) => go.run(result.instance));
</script>

</html>
```