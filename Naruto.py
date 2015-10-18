#!/usr/bin/env python
# encoding: utf-8
import urllib2,urllib,os,re,socket
socket.setdefaulttimeout(25)

import time

"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: Naruto.py
@time: 2015/10/18 10:16
@描叙：火影类。实现下载功能。
@思路：源地址 http://www.fzdm.com/manhua/001/
1、获取章节名称与地址。
2、获取章节下的图片名称与地址。
3、下载图片。并按章节分文件夹保存。

需要增加的特性：多线程下载。下载错误需要记录。然后手动去下载。


获取执行的路径。

共计多少章节
共计多少图片
错误图片地址。

先获取所有需要下载的url
再执行下载图片操作



1-146 本漫画。






"""


def func():
    pass


class Naruto():
    def __init__(self):
        self.base_url = 'http://www.fzdm.com/'
        self.url =  'http://www.fzdm.com/manhua/' #漫画列表 #地址
        self.book = [] #书籍集合。元素是字典。每一个元素。有3个key。title 、link、chapters 表示 书名、书地址、所有的章节序列。
        # self.chapter = [] #章节集合.元素是字典。每一个元素。有3个key：title 、link 、imgs、表示章节名称、章节地址、章节的所有图片序列。



    #读取网页，
    def get_html(self,url):
        html = ''
        try:
            html = urllib2.urlopen(url).read()
        except Exception,e:
            print(u'打开网页%s错误:%s'% (url,e.message))
        return html
    #<a href="135/" title="AKB49漫画"><img src="//static.fzdm.com/none.png" alt="AKB49漫画"></a>
    def get_book(self):
        html = self.get_html(self.url)
        if(html):
            p1 = re.compile('<div class="round">.*?<li><a href="(.*?)" title="(.*?)">.*?</a>',re.S)
            rs = re.findall(p1,html)
            if(rs and len(rs)>0):
                for item in rs:
                    title = item[1].decode('utf-8','ignore')
                    link = 'http://www.fzdm.com/manhua/%s'% (item[0])
                    self.book.append({'title':title,'link':link,'chapters':[]})
            else:
                print(u'没有发现书籍:页面未找到')
        else:
            print(u'没有发现书籍:页面为空')


    #获取书籍的章节。获取指定书籍的章节。参数为书籍的字典。
    #<li class="pure-u-1-2 pure-u-lg-1-4"><a href="509/" title="旋风管家509话">旋风管家509话</a></li>
    #传递的是字典，可以改变。因此这里是传地址引用。
    def get_chapter(self,book):
        html = self.get_html(book['link'])
        if(html):
            p1 = re.compile('<li class="pure-u-\d-\d pure-u-lg-\d-\d"><a href="(.*?)" title="(.*?)">.*?</a>',re.S)
            rs = re.findall(p1,html)
            if(rs and len(rs)>0):
                for item in rs:
                    # print item
                    title = item[1].decode('utf-8','ignore')
                    link = '%s%s'% (book['link'],item[0])
                    book['chapters'].append({'title':title,'link':link,'imgs':[]})

            else:
                print(u'没有发现章节:页面未找到')
        else:
            print(u'没有发现章节:页面为空')


    #这里默认一个页面就一个图片。
    #先获取章节有多少图片 <font id="TotalPage">98</font>
    #再获取对应的页面地址
    #再获取图片的地址。
    #图片的数据在js里
    #var picCount = 18;var picAy = "2015/10/141101090.jpg,2015/10/141101091.jpg,2015/10/141101092.jpg,2015/10/141101093.jpg,2015/10/141101094.jpg,2015/10/141101095.jpg,2015/10/141101096.jpg,2015/10/141101097.jpg,2015/10/141101098.jpg,2015/10/141101099.jpg,2015/10/1411010910.jpg,2015/10/1411010911.jpg,2015/10/1411010912.jpg,2015/10/1411010913.jpg,2015/10/1411010914.jpg,2015/10/1411010915.jpg,2015/10/1411010916.jpg,2015/10/1411010917.jpg";picAy = picAy.split(",");var hosts = ["http://s2.nb-pintai.com/"];

    def get_img(self,chapter):
        # print(u'从地址 %s 获取图片'% chapter['link'])
        html = self.get_html(chapter['link'])
        # print html
        if(html):

            #先获取图片的地址。var hosts = ["http://s1.nb-pintai.com/"];


            p2 = re.compile('var hosts.*?=.*?["(.*?)"];\n</script>',re.S)
            rs2 = re.findall(p2,html)
            if(rs2 and len(rs2)>0):
                for item in rs2:
                    # print item
                    #找到第一个分号。切片
                    posend = item.index(";")
                    chapter['img_sub'] = item[0:posend][14:-2]
                    # print(self.host[14:-2])
                    # print(u'找到的图片url %s'% item)
            # exit()
            else:
                print(u"没有找到图片")
                return


            p1 = re.compile('var picCount =(.*?);var picAy = "(.*?)";picAy',re.S)
            rs = re.findall(p1,html)
            if(rs and len(rs)>0):
                for item in rs:
                    # print item[0] #图片的数量
                    # print item[1] #图片的字符串，逗号分隔。

                    # title = item[1].decode('utf-8','ignore')
                    # link = '%s/%s'% (chapter['link'],item[0])
                    chapter['imgs'] = item[1].split(',')
                    #这里的图片地址，需要添加 http://s2.nb-pintai.com/
                    #这里的图片地址不固定。http://s1.nb-pintai.com/

            else:
                print(u'没有发现图片:页面未找到')
        else:
            print(u'没有发现图片:页面为空')

    #传递目录(c:\\吴文付漫画\\xx书籍\\xx章节)、图片名称（id）、图片地址
    def down_img(self,imgdir,imgid,url):
        #获取图片的后缀。格式
        rs = url.split(".")
        #拼接图片保存位置.c:\\吴文付漫画\\xx书籍\\xx章节\\1.jpg
        # p = '%s\\%s.%s' %(imgdir,imgid,rs[-1].strip())
        p = '%s\\%s.jpg' %(imgdir,imgid)
        #设置目录
        if not(os.path.exists(imgdir)):
            os.makedirs(imgdir)
        print u'下载并保存图片为:%s' % p
        #下载图片
        try:
            urllib.urlretrieve(url,p)
        except Exception,e:
            print(u'下载图片 %s 失败' % url)




if __name__ == '__main__':
    pass