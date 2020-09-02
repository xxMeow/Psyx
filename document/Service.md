# Service

### Generate a SSH key

```bash
$ ssh-keygen -t rsa -C "xmx1025@gmail.com"
```

### Git

```bash
$ git config --global user.name "xxMeow"
$ git config --global user.email "xmx1025@gmail.com"
$ git config --list
user.name=xxMeow
user.email=xmx1025@gmail.com
```

### Python

##### Create virtual environment

```bash
$ conda create -n tfenv
$ conda activate tfenv
```

##### Search for packages

- 简单搜索

    ```bash
    $ conda search supervisor
    Loading channels: done
    # Name                       Version           Build  Channel
    supervisor                     3.3.3  py27h9aadb0f_0  pkgs/main
    supervisor                     3.3.4          py27_0  pkgs/main
    supervisor                     3.3.5          py27_0  pkgs/main
    supervisor                     4.0.2          py27_0  pkgs/main
    supervisor                     4.0.2          py36_0  pkgs/main
    ... ...
    ```

    四列分别为 包名称 / 包版本 / 包的build编号 / 包源，其中从build编号一般可以看出包的大概依赖。依此进行下一步搜索

- 详细依赖

    可以看出，conda使用`=`、`>`、`<`来限定对包的各项要求（版本 & buil编号）

    ⚠️最好用单引号或双引号整个括起来，不然大于号可能会被shell展开。。

    通常到这一步还不能确定要安装的包的build编号，可以只通过`supervisor=4.1.0`来查看该版本下所有build的详细依赖

    ```bash
    $ conda search -i supervisor=4.1.0=py38_0
    Loading channels: done
    supervisor 4.1.0 py38_0
    -----------------------
    file name   : supervisor-4.1.0-py38_0.conda
    name        : supervisor
    version     : 4.1.0
    build       : py38_0
    build number: 0
    size        : 582 KB
    license     : BSD-derived
    subdir      : linux-64
    url         : https://repo.anaconda.com/pkgs/main/linux-64/supervisor-4.1.0-py38_0.conda
    md5         : cb74bf81451bac10481f7e8cc9e3f214
    timestamp   : 2019-11-17 06:56:32 UTC
    dependencies: 
      - gettext >=0.19.8.1,<1.0a0
      - meld3 >=1
      - python >=3.8,<3.9.0a0
    ```

    可以在dependencies看到要求的python的版本为[3.8, 3.9)

##### Install packages

> 记住先进入要安装的虚拟环境，或通过`-n [env_name]`来指定环境

用conda安装以下包：

- `pymysql=0.9.2=py38_0`
- `Supervisor=4.1.0=py38_0`（这个包会下载一个python3.8.5。。我不是已经有python3.8.3了吗！！差评！）
- `flask=1.1.2`（新版的flask竟然对python版本没要求。。🐂🍺！）
- `gunicorn=20.0.4=py38_0`

在conda环境下使用pip安装以下包：

```bash
pip install Flask-RESTful
```

