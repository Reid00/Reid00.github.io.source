---
title: "Vscode远程开发配置"
date: 2022-06-08T14:22:29+08:00
lastmod: 2022-06-08T14:22:29+08:00
author: ["Reid"]
categories: 
- vscode
tags: 
- vscode
- remote
- dev
- server
keyword:
- vscode
description: ""
weight: 2 # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
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

## 准备vscode 插件

- 在vs code的扩展商店中搜索remote-ssh, install
  ![remote-ssh](https://raw.githubusercontent.com/Reid00/image-host/main/20210817/image.5riodcmvsr00.png)

## 配置remmote-ssh 插件

- 使用快捷点, ctrl + shift + P 输入config
  ![config remote-ssh](https://raw.githubusercontent.com/Reid00/image-host/main/20210817/image.4x51cb1ih0o0.png)

- 选择第一个，在.ssh 目录的config文件
  ![directory](https://raw.githubusercontent.com/Reid00/image-host/main/20210817/image.2m9h9eqcwwc0.png)

- 按照以下格式配置

  ```shell
  Host Personal
  HostName 172.16.1.1
  User root
  Port 22
  IdentityFile C:\Users\ld\.ssh\id_rsa
  ```

  - Host: 自定义的服务器名称，用于个人区分
  - HostName: 需要远程的服务器的IP 地址
  - User: 远程服务器用的账号
  - Port: 默认ssh 端口22
  - IdentityFile: 免登录的id_rsa路径

`注意: 多次实验加入IdentityFile 都不能做到通过跳板机免密码，最后把客户机的id_rsa.pub添加到target 才免密， 相当于直接可以连接target机器了。`

- 如果通过跳板机连接服务器
  有时候我们需要跳板机来连接服务器，也即先连接一台跳板机服务器，然后通过这台跳板机所在的内网再次跳转到目标服务器。
  最简单的做法就是按上述方法连接到跳板机，然后在跳板机的终端用ssh指令跳转到目标服务器，但这样跳转后，我们无法在VScode中打开服务器的文件目录，操作起来很不方便。我们可以把config的设置改成如下，就可以通过c00跳板机跳转到c01了

    ```shell
    Host BackupCluster
    HostName 1.16.1.1
    User root
    Port 22
    ProxyCommand C:\Windows\System32\OpenSSH\ssh.exe -W %h:%p -q Personal
    IdentityFile C:\Users\ld\.ssh\id_rsa
    ```

    - ProxyCommand: openssh的安装目录（我这里是C:\Windows\System32\OpenSSH\ssh.exe）
    - -W表示stdio forwarding模式 接着后面的%h是一个占位符，表示要连接的目标机,也就是Hostname指定的ip或者主机名
    - %p同样也是占位符，表示要连接到目标机的端口。
    - %h, %p这里可以直接写死固定值，但是使用%h和%p可以保证在Hostname和Port变化的情况下ProxyCommand这行不用跟着变化

- openssh 的安装方法

  - 以管理员身份运行window Powershell，然后键入如下两条命令

    ```shell
    Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'
    ```

  - 这条是用来检测是否有适合安装的openssh软件，正常情况下应有如下返回：

    ```shell
    Name  : OpenSSH.Client~~~~0.0.1.0
    State : NotPresent
    Name  : OpenSSH.Server~~~~0.0.1.0
    State : NotPresent
    ```

  - 第二条命令：

    ```shell
    Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
    ```

    如果安装完成应有如下返回：

    ```shell
    Path          :
    Online        : True
    RestartNeeded : False
    ```

## 免密码登录 如从A登录B，A=>B

1. 本机创建ssh密钥, 生成在~/.ssh目录下

   ```shell
   ssh-keygen -t rsa
   ```

   说明：

   - authorized_keys：其实就是存放各个机器公钥的地方，
   - id_rsa : 生成的私钥文件，
   - id_rsa.pub ： 生成的公钥文件，
   - know_hosts : 已知的主机公钥清单，

   `设置互信其实就是将id_rsa.pub公钥信息发送到需要被信任的机器上的authorized_keys文件中即可，也就是A发送到B上authorized_keys文件中`

2. 发送密钥
   在A 机上运行

   ```shell
   ssh-copy-id root@192.168.x.x
   ```

   如果ssh-copy-id执行不了的话(没有ssh默认库的情况)，可以使用scp进行发送，即：

   ```shell
   scp -p ~/.ssh/id_rsa.pub root@192.168.x.x:/root/.ssh/authorized_keys
   ```

   通过以上命令, 即可将公钥发送过去，发送过去之后可以登录B机器查看authorized_keys文件，可以看到了机器A的公钥信息，如过是多个机器发送给B的话则保存多个公钥信息，如下
   ![ssh](https://raw.githubusercontent.com/Reid00/image-host/main/20210817/image.59r5imjs9bc0.png)
   发送成功之后，再次ssh登录，从A机器登录到B 机器。