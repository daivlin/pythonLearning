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

luooUrl = "http://www.luoow.com/r/{}/"

def parse_javascript(js):
    '''解析js文本中的mp3数据,以字典形式返回：{'name':mp3Name,'url':}'''
    patternName = re.compile(r'"name":"(.*?)"') #name
    patternMp3 = re.compile(r'"src":"(.*?.mp3)"') #mp3Url
    namesList = patternName.findall(js)
    mp3List = patternMp3.findall(js)
    
    musicDictList = [{"name":name,"url":url} for name,url in zip(namesList,mp3List)]
    
    return musicDictList

class LuooMusic(object):
    '''下载落网'''
    def __init__(self,url):
        self.url = url
        try:
            self.html = pq(url = self.url)
        except:
            self.html = ""
        
    def get_title(self):
        '''获取每一期的标题'''
        
        if self.html:
            return self.html("title").text()
        else:
            return ""
        
    def get_coverUrl(self):
        '''获取每一期封面'''
        if self.html:
            return self.html(".container .cover_img img").attr("src")
        else:
            return ""
        
    def get_musicDictList(self):
        '''获取每一期音乐列表'''
        if self.html:
            return parse_javascript(self.html("script")[1].text)
        else:
            return ""
            
class DownloadCoverThread(threading.Thread):
    ''' 下载线程'''
    def __init__(self,name,url):
        super(DownloadThread,self).__init__()
        self.name = name
        self.url = url

    def run(self):
        ''' 下载封面 '''
        ABSPATH = os.path.dirname(os.path.realpath(__file__))
        COVERPATH = os.path.join(ABSPATH,"%s-cover.jpg"%self.name)
        if not os.path.exists(COVERPATH):
            with open(COVERPATH,"wb") as f:
                f.write(rq.get(self.url).content)
            print("%s was downloaded"%self.name)

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


def download_cover_thread(name,url):
    ''' 下载封面 '''
    ABSPATH = os.path.dirname(os.path.realpath(__file__))
    COVERPATH = os.path.join(ABSPATH,"%s-cover.jpg"%name)
    if not os.path.exists(COVERPATH):
        with open(COVERPATH,"wb") as f:
            f.write(rq.get(url).content)
        print("%s was downloaded"%name)

def download_music_thread(dirname,name,url):
    ''' 下载音乐 '''
    ABSPATH = os.path.dirname(os.path.realpath(__file__))
    DOWNDIR = os.path.join(os.path.join(ABSPATH,"Luoo"),"%s"%dirname)
    MUSICPATH = os.path.join(DOWNDIR,"%s.mp3"%name)
    try:
        os.mkdir(DOWNDIR)
    except:
        pass
    #if not os.path.exists(MUSICPATH):
    with open(MUSICPATH,"wb") as f:
        f.write(rq.get(url).content)
    print("%s was downloaded"%name)

if __name__ == "__main__":
    luooUrl = "http://www.luoow.com/mi/{}/"       #单曲
    for i in range(1,50):
        r = LuooMusic(luooUrl.format(i))
        dirname = "mi {} - {}".format(i,r.get_title())
        musicList = r.get_musicDictList()
        trs = []
        for music in musicList:
            trs.append(threading.Thread(target=download_music_thread,args=(dirname,music["name"],music["url"])))
            print("add %s thread"%music["name"])

        for tr in trs:
            tr.start()
            
        for tr in trs:
            tr.join()

    print("All have downloaded")
