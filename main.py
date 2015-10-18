#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: main.py
@time: 2015/10/18 10:17
@描叙：执行入口。
"""
from Naruto import Naruto
import time


def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':

    s1 = u"时间：2015年10月18日"
    s2 = u"作者：吴文付 hi_php@163.com"
    s3 = u"描叙:下载动漫书籍.默认的下载目录为c:\\动漫下载器。"
    screen_width = 200

    text_width = len(s1+s2+s3)
    box_width = text_width+6

    left_margin = (screen_width-box_width)//2

    print
    print ' '+'+'+'-'*(box_width-2)+'+'
    print ' '+'| '
    print ' '+'| '+s1
    print ' '+'| '+s2
    print ' '+'| '+s3
    print ' '+'| '
    print ' '+'+'+'-'*(box_width-2)+'+'
    print

    for x in reversed(xrange(1,20)):
        print(u'正在下载服务器漫画目录 %s秒后完成'%x)
        time.sleep(1)


    nar01 =  Naruto();
    nar01.get_book()
    num = len(nar01.book)
    print(u'共发现%s本漫画书'% num)
    print(u'目录如下:')
    i = 0
    for book in nar01.book:
        i +=1
        print(u'第%s本:%s'%(i,book['title']))

    #提示用户输入。要下载哪一本。
    print(u'请选择需要下载哪一本(如输入1则下载第一本，如果输入1,2 这表示下载第一本与第二本，输入1:5 这表示下载第1本到第5本):')
    id = raw_input()

    #如果不合格要求，这重新提示
    while( not id.isdigit() or int(id)> num or int(id)<1):
        print(u"你输出不符合要求，请重新输入")
        print(u'请选择需要下载哪一本(如输入1则下载第一本):')
        id = raw_input()
    print(u'你选择下载:%s' % nar01.book[int(id)-1]['title'])
    # print(id)
    # exit()

    j = 0
    #循环处理每一本书籍。
    for book in nar01.book:
        j +=1
        #如果不是用户选择的书籍，跳过。
        if(int(id) != j):
            continue
        nar01.get_chapter(book)
        print(u'获取<<%s>>所有章节成功，共计%s章'% (book['title'],len(book['chapters'])))
        #处理每一个章节。
        #这里对章节进行一次倒序。
        book['chapters'] = reversed(book['chapters'])
        for chapter in book['chapters']:
            nar01.get_img(chapter)
            # print(chapter['imgs'])
            # exit()
            #处理了某一本书的某一个章节
            #下载该章节的图片。
            i = 0
            print(u'获取<<%s>>[%s]章节的图片成功,共计%s张' % (book['title'],chapter['title'],len(chapter['imgs'])))
            for img in chapter['imgs']:
                i += 1
                imgdir = u'c:\\漫画下载器\\%s\\%s\\' %(book['title'],chapter['title'])
                url = chapter['img_sub']+'%s' % img
                # print(u'处理url:%s'% url)
                nar01.down_img(imgdir,i,url)
            # exit()


        #处理了某一个本书的所有章节。

    #处理了所有书

    #这里可以统一开始下载.
