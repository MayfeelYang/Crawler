#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import re

def getHtml(url):
    page = urllib.urlopen(url)
    #urllib.urlopen()方法用语打开一个URL地址，read()方法用语读取URL上面的数据
    html = page.read()
    return html


def getImg(html):
    reg = r'href="(.+?\.png)">'
    imgRe = re.compile(reg)
    imgList = re.findall(imgRe, html)
    count = 0
    print "the length of imgList: ", len(imgList)
    for imgURL in imgList:
        urllib.urlretrieve(imgURL, './download/%s.jpg' % count)
        #这里的核心就是用了urllib.urlretrieve()方法，将远程文件直接下载到本地
        count += 1
    return imgList


def getHtmls(urlPrefix, startID):
    wrongCount = 0
    for i in range(0, 50):
        url = urlPrefix + str(startID)
        try:
            getHtml(url)
        except Exception,e:
            wrongCount += 1
        startID += 1
        print "startID: ", startID
    print "wrongCount: ", wrongCount
    

if __name__ == "__main__":
    #------------下面是爬取1个指定页面--------------
    try:
        #html = getHtml("http://tieba.baidu.com/p/2460150890")
        html = getHtml("http://index.baidu.com/?tpl=trend&word=%CB%CE%D6%D9%BB%F9")
        #print html
        #下面是获取html中的图片的链接，并下载图片
        getImg(html)
    except Exception,e:
        print "Something wrong!!!!!"
    
    #------------下面是连续爬取50个页面--------------
    '''
    urlPrefix = "http://tieba.baidu.com/p/"
    startID = 2460150866
    getHtmls(urlPrefix, startID)
    '''
