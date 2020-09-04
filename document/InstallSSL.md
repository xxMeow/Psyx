# Install SSL

> 在Linux+Nginx环境下安装单域名SSL证书

### Generating CSR on Apache + OpenSSL/ModSSL/Nginx + Heroku

> CSR是一块加密文本，保存了你申请SSL证书时所提交的Certificate Authority
>
> 通常使用将要安装这个SSL证书的服务器去生成CSR，它会包含网站的信息，并将在被加密后包含在SSL证书里
>
> 生成.csr时，一个.key文件也会被一起生成，该.key文件一旦遗失或泄露则只能重新生成整个新的CSR

##### CSR Information

> 确认以下信息，它们将在稍后的步骤中用于生成CSR

- Common Name 将要认证的完整域名 -- `ohfish.me`
- Country 两位字母的国家代码 -- `KR`
- Locality 城市的全名 -- `Seoul`
- Organization 组织名称，没有可填`NA` -- `NA`
- Organizational Unit 部门名称，没有可填`NA` -- `NA`
- Email address 申请证书的邮箱 -- `xmx1025@gmail.com`

- Challenge Password and Optional Company Name 此项必须留空，填写任何内容都会导致错误

##### Key Algorithm

> Linux下通常使用OpenSSL来生成CSR，只要安装了web server(Apache OR Nginx)，就表示OpenSSL可以使用
>
> 工具决定了，接下来选择将要使用的加密算法。可以RSA和ECDSA中二选一，在此将使用RSA加密

- 在根目录下建立一个新目录来存放证书：

    ```bash
    $ mkdir ~/.ssl
    ```

- 生成CSR

    ```bash
    $ cd ~/.ssl
    $ openssl req -new -newkey rsa:2048 -nodes -keyout ohfish_me.key -out ohfish_me.csr
    ```

    运行结果如下：

    ```bash
    root@ohfish:~/.ssl# openssl req -new -newkey rsa:2048 -nodes -keyout ohfish_me.key -out ohfish_me.csr
    Generating a RSA private key
    .........................................................................+++++
    .................................................................................................................+++++
    writing new private key to 'ohfish_me.key'
    -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:KR
    State or Province Name (full name) [Some-State]:Seoul
    Locality Name (eg, city) []:Seoul
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:NA
    Organizational Unit Name (eg, section) []:NA
    Common Name (e.g. server FQDN or YOUR name) []:ohfish.me
    Email Address []:xmx1025@gmail.com
    
    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:
    An optional company name []:
    root@ohfish:~/.ssl# ls -al
    total 16
    drwxr-xr-x 2 root root 4096 Sep  3 15:33 .
    drwx------ 8 root root 4096 Sep  3 15:18 ..
    -rw-r--r-- 1 root root 1033 Sep  3 15:33 ohfish_me.csr
    -rw------- 1 root root 1704 Sep  3 15:31 ohfish_me.key
    ```

    可以看到生成了一个.csr和一个.key文件

##### Activate SSL

- 选择并完成DNS-based或HTTP-based认证

- 认证通过后，将会收到一封邮件

- 下载.zip附件，内有一个.ca_bundle和一个.crt文件，将这两个文件传上服务器中刚刚建立的`~/.ssl`文件夹

    ```bash
    $ scp ohfish_me.ca-bundle ohfish_me.crt root@34.64.140.177:/root/.ssl
    ```

