pip 的默认的安装源速度很慢，更换为国内的源地址，可以提高下载速度

    首先进入~/.pip 目录

cd ~/.pip

    如果不存在，进行创建

mkdir ~/.pip

    编辑 pip 配置文件

vi ~/.pip/pip.conf

- 永久修改：
linux:
修改 ~/.pip/pip.conf (没有就创建一个)， 内容如下：
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```
- windows:
直接在user目录中创建一个pip目录，如：C:\Users\xx\pip，新建文件pip.ini，内容如下
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```



    配置文件内容

    mirrors.tuna.tsinghua.edu.cn 是清华的源地址，上面还有很多其它的源

pip国内的一些镜像

  阿里云 http://mirrors.aliyun.com/pypi/simple/  
  中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/  
  豆瓣(douban) http://pypi.douban.com/simple/  
  清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/  
  中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/  

```
[global]
timeout = 5000
index-url = http://pypi.douban.com/simple/
[install]
use-mirrors = true
mirrors = http://pypi.douban.com/simple/
```
