[参考](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04#conclusion)

### 安装apache2、python3-pip、mod_wsgi版本
- sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3

### 安装python版本
- 安装虚拟环境	sudo pip3 install virtualenv
- 安装python版本（-p python3）	virtualenv -p python3 myprojectenv
- 安装启动虚拟环境		source myprojectenv/bin/activate
- 查看pip版本	pip --version
- 安装软件包	pip install django
- 在虚拟环境中运行项目	python index.py
- 退出虚拟环境	deactivate

### Configure Apache
-  sudo vim /etc/apache2/sites-available/000-default.conf
```
<VirtualHost *:80>         
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating        # redirection URLs. In the context of virtual hosts, the ServerName        # specifies what hostname must appear in the request's Host: header to        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        #DocumentRoot /var/www/html
        DocumentRoot /home/ubuntu/myWebSite

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are


        Alias /static/ /home/ubuntu/myWebSite/static/
        AddType text/html .py
        <Directory /home/ubuntu/myWebSite>
                Require all granted
        </Directory>
        WSGIDaemonProcess myWebSite python-home=/home/ubuntu/myproject/myprojectenv python-path=/home/ubuntu/myWebSite
        WSGIProcessGroup myWebSite
        WSGIScriptAlias / /home/ubuntu/myWebSite/index.py

        <Directory /home/ubuntu/myWebSite>
                <Files index.py>
                        Require all granted
                </Files>
        </Directory>
        <Directory /home/ubuntu/myWebSite/static>
                Require all granted
        </Directory>
</VirtualHost>
```
- 修改读写权限	如文本读写，数据库读写
- 检查配置 	sudo apache2ctl configtest
- 重启apache2 	sudo systemctl restart apache2

### ========= 如果出错 ==========
- 查看日志	tail /var/log/apache2/error.log

### ssh 发送文件至服务器
- scp -r /media/daivlin/DAIVLIN/web11/myPro/ ubuntu@132.232.119.208:/home/ubuntu/myWebSite  

