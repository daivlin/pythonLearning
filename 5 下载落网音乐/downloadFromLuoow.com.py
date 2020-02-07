#coding:utf-8
'''
Auth:daivlin
Date:2020-02-07
'''

import re
import urllib
import threading
import os
from pyquery import PyQuery as pq
import requests as rq

def parse_javascript(js):
    '''解析js文本中的mp3数据,以字典形式返回：{'name':mp3Name,'url':}'''
    patternName = re.compile(r'"name":"(.*?)"') #name
    patternMp3 = re.compile(r'"src":"(.*?.mp3)"') #mp3Url
    namesList = patternName.findall(js)
    mp3List = patternMp3.findall(js)
    
    musicDictList = [{"name":name[:2],"url":url} for name,url in zip(namesList,mp3List)]
    
    return musicDictList

class LuooMusic(object):
    '''下载落网'''
    def __init__(self,issueNum):
        self.url = "http://www.luoow.com/{}/".format(issueNum)
        self.html = pq(url = self.url)
        
    def get_title(self):
        '''获取每一期的标题'''
        return self.html("title").text()
        
    def get_coverUrl(self):
        '''获取每一期封面'''
        return self.html(".container .cover_img img").attr("src")
        
    def get_musicDictList(self):
        '''获取每一期音乐列表'''
        return parse_javascript(self.html("script")[1].text)

class DownloadThread(threading.Thread):
    ''' 下载线程'''
    def __init__(self,dirname,name,url):
        super(DownloadThread,self).__init__()
        self.dirname = dirname
        self.name = name
        self.url = url

    def run(self):
        ''' 下载音乐 '''
        ABSPATH = os.path.dirname(os.path.realpath(__file__))
        DOWNDIR = os.path.join(os.path.join(ABSPATH,"Luoo"),"%s"%self.dirname)
        MUSICPATH = os.path.join(DOWNDIR,"%s.mp3"%self.name)
        try:
            os.mkdir(DOWNDIR)
        except:
            pass
        if not os.path.exists(MUSICPATH):
            with open(MUSICPATH,"wb") as f:
                f.write(rq.get(self.url).content)
            #urllib.request.urlretrieve(self.url, MUSICPATH)    #乱码bug还未处理
            print("%s was downloaded"%self.name)
            
for i in range(993,1000):
    r = LuooMusic(i)
    name = r.get_title()
    tds = []
    index = 1
    for j in r.get_musicDictList():
        tds.append(DownloadThread(name,j["name"],j["url"]))
        index += 1
    print("start download %s"%name)
    for td in tds:
        td.start()
    for tj in tds:
        tj.join()
    print("%s download complate"%name)
    print("=========================")

print("All have downloaded")
