---
title: "Dockerfile案例"
date: 2022-06-08T11:27:14+08:00
lastmod: 2022-06-08T11:27:14+08:00
author: ["Reid"]
categories: 
- Docker
tags: 
- Docker
- Dockerfile
keyword:
- Dockerfile
- Docker
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

## 一、DockerHub 官网链接

>https://hub.docker.com/

## 二、Dockerfile 关键字

**注意:** dockerfile 的关键字必须都是大写才能使用

- FROM

  - 指定基础镜像，当前新镜像是基于哪个镜像的。其中，`scratch`是个空镜像，这个镜像是虚拟的概念,并不实际存在,它表示一个空白的镜像，当前镜像没有依赖于其他镜像

    ```shell
    FROM scratch
    ```

- MAINTAINTER

  - 镜像维护者的姓名和邮箱地址

    ```shell
    MAINTAINER Sixah <sixah@163.com>
    ```

- RUN

  - 容器构建时需要运行的命令

    ```shell
    RUN echo 'Hello, Docker!'
    ```

- EXPOSE

  - 当前容器对外暴露出的端口

    ```shell
    EXPOSE 8080
    ```

    **注意：**

    -p 和 expose 区别

    - -p 80:8080 

      外部80 端口转向 向外暴露是 8080 端口的 Docker 容器。如果只写 -p 80 ，那么当作是 -p 80:80。也就是说，容器之间可以访问该 暴露8080端口的容器，其他用户也可以访问

    - exposes 80

    ​       表示 容器之间可以访问该 暴露80端口的容器，但是其他用户不可以可以访问。这样其实就是做到了 封闭。

- WORKDIR

  - 指定在创建容器后，终端默认登陆进来的工作目录，一个落脚点

    ```shell
    WORKDIR /home/
    ```

- ENV

  - 用来在构建镜像过程中设置环境变量

    ```shell
    ENV MY_PATH /usr/mytest
    ```

    这个环境变量可以在后续的任何RUN指令中使用，这就如同在命令前面指定了环境变量前缀一样;当然，也可以在其他指令中直接使用这些环境变量，比如：WORKDIR $MY_PATH

- ADD

  - 将宿主机目录下的文件拷贝进镜像且ADD命令会自动处理URL和解压tar压缩包

    ```shell
    ADD Linux_amd64.tar.gz
    ```

- COPY

  - 类似于ADD，拷贝文件和目录到镜像中，将从构建上下文目录中<源路径>的文件/目录复制到新的一层镜像内的<目标路径>位置

  - COPY 能实现的ADD 都可以实现，ADD 可以处理URL， 还可以自动解压，COPY不可以

    ```shell
    COPY . /go/src/app
    ```

- VOLUME

  - 容器数据卷，用于数据保存和持久化工作

    ```shell
    VOLUME　/data
    ```

- CMD

  - 指定一个容器启动时要运行的命令。Dockerfile中可以有多个CMD指令，但只有最后一个生效，CMD会被docker run之后的参数替换

    ```shell
    CMD ["/bin/bash"]
    ```

    **注意:**

    ```shell
    CMD -i 将代替 CMD ["/bin/bash"] 而CMD -i 无意义
    ```

    而ENTRYPOINT ，可以在后面追加参数

    如果dockerfile 最后是

    ENTRYPOINT curl ["s","baidu.com"]

    ```shell
    DOCKER run centos -i 意味着 ENTRYPOINT curl ["s","-i","baidu.com"]
    ```

- ENTRYPOINT

  - 指定一个容器启动是要运行的命令。ENTRYPOINT的目的和CMD一样，都是在指定容器启动程序及参数

- ONBUILD

  - 当构建一个被继承的Dockerfile时运行的命令，父镜像在被子镜像继承后，父镜像的ONBUILD指令被触发

## 三、 给基础的CentOS 添加基础功能

- 编写dockerfile

```shell
FROM　CENTOS
MAINTAINER zzz zzz@163.com
ENV MYPATH /usr/local
WORKDIR $MYPATH

RUN yum -y install vim
RUN yum -y install net-tools

EXPOSE 80

CMD echo $MYPATH
CMD echo "success -----ok"
CMD /bin/bash
```

- 构建 build

  ```shell
  docker build -f dockerfile路径 -t mycentos:v1.3 .
  ```

- 运行

  ```shell
  docker run -it 新镜像名:TAG
  ```

- 列出镜像的变更历史

  ```shell
  docker history 镜像名
  ```

  