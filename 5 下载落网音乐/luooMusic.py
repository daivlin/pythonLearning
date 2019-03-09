#coding:utf-8
'''
Auth:daivlin
Date:2019-1-26
'''

import os
import time
import urllib
import threading
from selenium import webdriver

class Luoo(object):
    def __init__(self,issue):
        ''' init ,参数为期数 '''
        self.issue_url = r"http://www.luoo.net/music/" + "%03d"%issue
        #self.issue_url = r"http://www.luoo.net/vol/index/1376"
        driver = webdriver.PhantomJS()
        driver.get(self.issue_url)

        #每期名称如: VOL666 欢迎来到巴黎
        self.issue_name = "VOL." + "%03d"%issue + " " + driver.title
        self.music_list = []
        try:
            luooPlayer = driver.execute_script("return luooPlayer") #读取js变量
            var = 1
            for i in luooPlayer["playlist"]:
                self.music_list.append(("%02d"%var,i["mp3"]))
                var += 1
        except:
            print("No issue: %s"%issue)

        #音乐列表为元组：(name,url)
        driver.quit()

    def get_issue_name(self):
        ''' 获取期刊号 '''
        return self.issue_name

    def get_music_list(self):
        ''' 获取音乐列表 '''
        return self.music_list

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
            try:
                urllib.urlretrieve(self.url, MUSICPATH)
            except:
                import urllib.request
                urllib.request.urlretrieve(self.url, MUSICPATH)
            print("%s.mp3 was downloaded"%self.name)

def startRun(beginIssue,endIssue):
	'''开始下载，range函数的最后一位是不包含的，所以需加1'''
	for i in range(int(beginIssue),int(endIssue)+1):
		r = Luoo(i)
		name = r.get_issue_name()
		tds = []
		for j in r.get_music_list():
			tds.append(DownloadThread(name,j[0],j[1]))
		print("start download %s"%name)
		for td in tds:
			td.start()
		for tj in tds:
			tj.join()
		print("%s download complate"%name)
		print("=========================")
	print("All have downloaded")

if __name__ == "__main__":
	beginIssue = int(input(u"请输入要下载的开始期数:\n"))
	endIssue = int(input(u"请输入要下载的结束期数:\n"))
	startRun(beginIssue,endIssue)
