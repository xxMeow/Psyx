# OhFish

### Abstract

##### Physical Machine

|    Metric | Google Cloud Platform VPS               |
| --------: | --------------------------------------- |
|  OS Image | Ubuntu 20.04 LTS                        |
|        IP | Static IPv4                             |
|       CPU | 1 core                                  |
|    Memory | 2G                                      |
|      Disk | SSD 10G                                 |
| Fire Wall | Allow HTTP Traffic, Allow HTTPS Traffic |
|   DNS PTR | Yes                                     |

##### Technology Stack

- Linux + Google Cloud Platform
- Nginx
- MySQL
- Gunicorn + Flask
- Supervisor
- Python + Ananconda(Miniconda3)

### Server Setting

##### Basic

- Set timezone

    ```bash
    $ sudo timedatectl set-timezone "Asia/Seoul"
    ```

- Add the following lines to `/etc/profile`:

    ```bash
    # OhFish ######################################################################
    
    # show timestamp of history
    HISTTIMEFORMAT="%F %T "
    
    # forbid the `rm` command
    alias rm='echo "< Forbidden > Use the `trash-put` command instead of `rm`."'
    ```

##### Identity

> GCP forbids root login as default, both of the root and user account come with no password
>
> But user can get root priviliges by simply using `sudo` at this time

- Set root's password for the first time

    ```bash
    $ sudo passwd root
    Enter new UNIX password: 
    Retype new UNIX password: 
    passwd: password updated successfully
    ```

- Modify the SSH config to enable root login with password

    - Open the config file

        ```bash
        $ sudo vim /etc/ssh/sshd_config
        ```

    - Modify the following 2 lines to be `yes`:

        ```bash
        PermitRootLogin yes # PermitRootLogin prohibit-password
        PasswordAuthentication yes # PasswordAuthentication no
        ```

    - Restart SSH service (NOT the server itself)

        ```bash
        $ sudo /etc/init.d/ssh restart
        ```

- Logout and now root can login with password

    ```bash
    $ ssh root@$(SERVER_IP)
    ```

##### (option) Login to `snap` Store

```bash
$ sudo snap login xmx1025@gmail.com
```

##### Environment Check

- Run the following check list

    ```bash
    df
    lslogins -u
    echo $PATH
    
    whereis python
    which python
    python --version
    
    whereis pip
    which pip
    pip --version
    
    whereis git
    which git
    git --version
    git config --list
    
    ls -al
    ```

- Result

    ```bash
    root@ohfish:~# df
    Filesystem     1K-blocks    Used Available Use% Mounted on
    /dev/root        9983232 1419724   8547124  15% /
    devtmpfs          498008       0    498008   0% /dev
    tmpfs             502008       0    502008   0% /dev/shm
    tmpfs             100404     920     99484   1% /run
    tmpfs               5120       0      5120   0% /run/lock
    tmpfs             502008       0    502008   0% /sys/fs/cgroup
    /dev/sda15        106858    3934    102924   4% /boot/efi
    /dev/loop0         30720   30720         0 100% /snap/snapd/8790
    /dev/loop1         56704   56704         0 100% /snap/core18/1885
    /dev/loop2         73088   73088         0 100% /snap/lxd/16558
    /dev/loop3        121856  121856         0 100% /snap/google-cloud-sdk/144
    tmpfs             100400       0    100400   0% /run/user/0
    tmpfs             100400       0    100400   0% /run/user/1001
    root@ohfish:~# lslogins -u
     UID USER    PROC PWD-LOCK PWD-DENY LAST-LOGIN GECOS
       0 root      81        0        0      09:50 root
    1000 ubuntu     0        0        1            Ubuntu
    1001 xmx1025    5        0        1      09:50 
    root@ohfish:~# echo $PATH
    /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
    root@ohfish:~# 
    root@ohfish:~# whereis python
    python: /usr/bin/python3.8 /usr/lib/python2.7 /usr/lib/python3.8 /etc/python3.8 /usr/local/lib/python3.8
    root@ohfish:~# which python
    root@ohfish:~# python --version
    
    Command 'python' not found, did you mean:
    
      command 'python3' from deb python3
      command 'python' from deb python-is-python3
    
    root@ohfish:~# 
    root@ohfish:~# whereis pip
    pip:
    root@ohfish:~# which pip
    root@ohfish:~# pip --version
    
    Command 'pip' not found, but there are 18 similar ones.
    
    root@ohfish:~# 
    root@ohfish:~# whereis git
    git: /usr/bin/git /usr/share/man/man1/git.1.gz
    root@ohfish:~# which git
    /usr/bin/git
    root@ohfish:~# git --version
    git version 2.25.1
    root@ohfish:~# git config --list
    root@ohfish:~# 
    root@ohfish:~# ls -al
    total 36
    drwx------  6 root root 4096 Aug 30 09:51 .
    drwxr-xr-x 19 root root 4096 Aug 30 08:56 ..
    -rw-r--r--  1 root root 3106 Dec  5  2019 .bashrc
    drwx------  2 root root 4096 Aug 30 09:50 .cache
    -rw-r--r--  1 root root  161 Dec  5  2019 .profile
    drwx------  2 root root 4096 Aug 30 09:51 .snap
    drwx------  2 root root 4096 Aug 30 08:55 .ssh
    -rw-------  1 root root 1294 Aug 30 09:49 .viminfo
    drwxr-xr-x  3 root root 4096 Aug 30 08:55 snap
    ```

##### Global Tools

> Before install anything, update the `apt` first
>
> ```bash
> $ sudo apt update
> ```
>
> Before install any tools with apt, check its dependencies with:
>
> ```
> $ apt depends [package name]
> ```

- tree
- net-tools (including `netstat`)

##### Miniconda3

- Download the installer script of [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) to `/usr/local/` as root

    ```bash
    $ wget -P /usr/local/ https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    ```

- Install it

    ```bash
    $ bash /usr/local/Miniconda3-latest-Linux-x86_64.sh
    ```

    Specify the installation path to `/usr/local/miniconda3`

- Initialization

    ```bash
    Do you wish the installer to initialize Miniconda3
    by running conda init? [yes|no]
    [no] >>> yes
    ```

    It will add some lines to root's `.bashrc`, cut and paste those lines to `/etc/profile`

- Add a new group which all users in it can use this miniconda3

    ```bash
    $ groupadd grpMiniconda3
    $ chgrp -R grpMiniconda3 /usr/local/miniconda3
    ```

- Change the privilege of this group

    ```bash
    $ chmod 770 -R /usr/local/miniconda3
    ```

- Add user to this group to allow them use miniconda3 (Don't forget the -a parameter!! It's for "append"!)

    ```bash
    $ usermod -a -G grpMiniconda3 xmx1025
    ```

- Delete the installer script and re-login

- Check

    ```bash
    # conda
    root@ohfish:~# which conda
    /usr/local/miniconda3/bin/conda
    root@ohfish:~# conda --version
    conda 4.8.3
    # python
    root@ohfish:~# whereis python
    python: /usr/bin/python3.8 /usr/lib/python2.7 /usr/lib/python3.8 /etc/python3.8 /usr/local/lib/python3.8 /usr/local/miniconda3/bin/python3.8-config /usr/local/miniconda3/bin/python3.8 /usr/local/miniconda3/bin/python
    root@ohfish:~# which python
    /usr/local/miniconda3/bin/python
    root@ohfish:~# python --version
    Python 3.8.3
    # pip
    root@ohfish:~# whereis pip
    pip: /usr/local/miniconda3/bin/pip
    root@ohfish:~# which pip
    /usr/local/miniconda3/bin/pip
    root@ohfish:~# pip --version
    pip 20.0.2 from /usr/local/miniconda3/lib/python3.8/site-packages/pip (python 3.8)
    ```

##### Nginx

- Install

    ```bash
    root@ohfish:~# apt update
    root@ohfish:~# apt install nginx
    ```

    It will be started automatically:

    ```bash
    root@ohfish:~# systemctl status nginx
    ● nginx.service - A high performance web server and a reverse proxy server
         Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
         Active: active (running) since Sun 2020-08-30 13:00:51 KST; 2min 13s ago
           Docs: man:nginx(8)
       Main PID: 3865 (nginx)
          Tasks: 2 (limit: 1167)
         Memory: 5.4M
         CGroup: /system.slice/nginx.service
                 ├─3865 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
                 └─3866 nginx: worker process
    
    Aug 30 13:00:50 ohfish systemd[1]: Starting A high performance web server and a reverse proxy server...
    Aug 30 13:00:51 ohfish systemd[1]: Started A high performance web server and a reverse proxy server.
    ```

- FireWall

    - Open port 80 and 443 for HTTP and HTTPS

        ```bash
        root@ohfish:~# ufw allow 'Nginx Full'
        Rules updated
        Rules updated (v6)
        ```

    - Open port 22 for SSH

        ```bash
        root@ohfish:~# ufw allow ssh
        Rules updated
        Rules updated (v6)
        ```

    - Enable firewall and check the status

        ```bash
        root@ohfish:~# ufw enable
        Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
        Firewall is active and enabled on system startup
        root@ohfish:~# ufw status
        Status: active
        
        To                         Action      From
        --                         ------      ----
        Nginx Full                 ALLOW       Anywhere
        22/tcp                     ALLOW       Anywhere
        Nginx Full (v6)            ALLOW       Anywhere (v6)
        22/tcp (v6)                ALLOW       Anywhere (v6)
        ```

- Make SSL Certification

    - Upload the `.ca-bundle` and `.crt` files to anywhere of server (I made `/root/.ssl_certification/` directory)

    - Combine them into a single file:

        ```bash
        $ cat ohfish_me.crt ohfish_me.ca-bundle >> ohfish_me_chain.crt
        ```

        > Open it with vim to check if there're incorrect new line

- Config

    - Default Configuration: `/etc/nginx/nginx.conf`

        User Configuration File(s): `/etc/nginx/conf.d/*.conf`

    - Remove the default config file

        ```bash
        $ unlink /etc/nginx/sites-enabled/default
        ```

    - Add our new config file

        ```bash
        $ touch /etc/nginx/conf.d/ohfish.conf
        $ chmod 755 -R /etc/nginx/conf.d/ohfish.conf
        ```

    - Edit our config file:

        ```bash
        $ vim /etc/nginx/conf.d/ohfish.conf
        ```

        Write blocks like following and test the installation of SSL:

        ```bash
        server {
        
            listen 443 ssl;
            listen [::]:443 ssl;
        
            ssl_certificate /root/.ssl/ohfish_me_chain.crt;
            ssl_certificate_key /root/.ssl/ohfish_me.key;
        
            root /home/xmx1025/OhFish/html;
            server_name ohfish.me;
        
            location / {
                root /home/xmx1025/OhFish/html;
                index index.html index.htm;
            }
            
        }
        ```

        Reload the Nginx:

        ```bash
        root@ohfish:/etc/nginx# nginx -t
        nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
        nginx: configuration file /etc/nginx/nginx.conf test is successful
        root@ohfish:/etc/nginx# nginx -s reload
        ```

        Then check SSL installation at [HERE](https://decoder.link)

    - Add the following block to permanently redirect HTTP traffic to HTTPS non-www

        ```bash
        server {
        
            listen 80;
            listen [::]:80;
        
            server_name ohfish.com www.ohfish.com;
            
            return 301 https://ohfish.me$request_uri;
        
        }
        ```

- Forbid ip access by setting `default_server`

- (Testing) Allow CORS requests:

    - Edit the config file to add following lines:

        ```bash
        location /api {
        	proxy_pass https://localhost:5000/;
        	proxy_set_header Host $host;
        	proxy_set_header X_Forwarded-For $proxy_add_x_forwarded_for;
        	
        	add_header Access-Control-Allow-Origin *;
        	#add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
        	add_header Access-Control-Allow-Methods 'GET, POST';
        	add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        	
        	#if ($request_method = 'OPTIONS') {
            #    return 204;
            #}
        }
        ```

    - Flask also needs to be configured

##### MySQL

- Install

    ```bash
    root@ohfish:~# apt update
    root@ohfish:~# apt install mysql-server
    ```

    It will be started automatically:

    ```bash
    root@ohfish:~# systemctl status mysql
    ● mysql.service - MySQL Community Server
         Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: enabled)
         Active: active (running) since Sun 2020-08-30 14:03:09 KST; 12s ago
       Main PID: 5867 (mysqld)
         Status: "Server is operational"
          Tasks: 39 (limit: 1167)
         Memory: 326.3M
         CGroup: /system.slice/mysql.service
                 └─5867 /usr/sbin/mysqld
    
    Aug 30 14:03:08 ohfish systemd[1]: Starting MySQL Community Server...
    Aug 30 14:03:09 ohfish systemd[1]: Started MySQL Community Server.
    ```

- Improve security by run command `mysql_secure_installation` without any parameters:

    ```bash
    root@ohfish:~# mysql_secure_installation
    
    Securing the MySQL server deployment.
    
    Connecting to MySQL using a blank password.
    
    VALIDATE PASSWORD COMPONENT can be used to test passwords
    and improve security. It checks the strength of password
    and allows the users to set only those passwords which are
    secure enough. Would you like to setup VALIDATE PASSWORD component?
    
    Press y|Y for Yes, any other key for No: y
    
    There are three levels of password validation policy:
    
    LOW    Length >= 8
    MEDIUM Length >= 8, numeric, mixed case, and special characters
    STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file
    
    Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 0  
    Please set the password for root here.
    
    New password: 
    
    Re-enter new password: 
    
    Estimated strength of the password: 50 
    Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) : y
    By default, a MySQL installation has an anonymous user,
    allowing anyone to log into MySQL without having to have
    a user account created for them. This is intended only for
    testing, and to make the installation go a bit smoother.
    You should remove them before moving into a production
    environment.
    
    Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
    Success.
    
    
    Normally, root should only be allowed to connect from
    'localhost'. This ensures that someone cannot guess at
    the root password from the network.
    
    Disallow root login remotely? (Press y|Y for Yes, any other key for No) : n
    
     ... skipping.
    By default, MySQL comes with a database named 'test' that
    anyone can access. This is also intended only for testing,
    and should be removed before moving into a production
    environment.
    
    
    Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
     - Dropping test database...
    Success.
    
     - Removing privileges on test database...
    Success.
    
    Reloading the privilege tables will ensure that all changes
    made so far will take effect immediately.
    
    Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
    Success.
    
    All done!
    root@ohfish:~# mysql --version
    mysql  Ver 8.0.21-0ubuntu0.20.04.4 for Linux on x86_64 ((Ubuntu))
    ```

- Login as root

    ```bash
    $ mysql
    ```

- Add new user (a admin + a visitor)

    ```bash
    mysql> CREATE USER 'xmx1025'@'localhost' IDENTIFIED BY 'password';
    Query OK, 0 rows affected (0.00 sec)
    
    mysql> CREATE USER 'visitor'@'%' IDENTIFIED BY 'password';
    Query OK, 0 rows affected (0.01 sec)
    ```

    > As host name:
    >
    > - `localhost` means "this computer" and MySQL treats this particular hostname specially: when a user with that host logs into MySQL it will attempt to connect to the local server by using a Unix socket file.
    > - `%` means "any host"

- Give privileges to MySQL user accounts

    ```bash
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'xmx1025'@'localhost';
    Query OK, 0 rows affected (0.01 sec)
    
    mysql> GRANT INSERT, SELECT ON *.* TO 'visitor'@'%';
    Query OK, 0 rows affected (0.02 sec)
    ```

- Port (Default: 3306)

    Show the current port:

    ```bash
    mysql> SHOW VARIABLES LIKE 'port';
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | port          | 3306  |
    +---------------+-------+
    1 row in set (0.03 sec)
    ```

    ⚠️This port shouldn't be opened to the internet!

### Conclusion

##### Ubuntu Accounts

- root
- ubuntu
- xmx1025

##### MySQL Accounts

- root
- xmx1025@localhost - ALL PRIVILEGES
- visitor@% - Insert + Select

##### /root

```bash
root@ohfish:~# ls -al
total 72
drwx------  8 root root  4096 Sep  3 17:14 .
drwxr-xr-x 19 root root  4096 Aug 30 11:37 ..
-rw-------  1 root root  5849 Sep  3 16:48 .bash_history
-rw-r--r--  1 root root  3107 Aug 30 12:15 .bashrc
drwx------  2 root root  4096 Aug 30 09:50 .cache
drwxr-xr-x  2 root root  4096 Aug 30 12:09 .conda
-rw-------  1 root root   289 Aug 31 11:01 .mysql_history
-rw-r--r--  1 root root   161 Dec  5  2019 .profile
drwx------  2 root root  4096 Aug 30 09:51 .snap
drwx------  2 root root  4096 Aug 30 08:55 .ssh
drwxr-xr-x  2 root root  4096 Sep  3 17:00 .ssl
-rw-------  1 root root 18125 Sep  3 17:14 .viminfo
drwxr-xr-x  3 root root  4096 Aug 30 08:55 snap
```

