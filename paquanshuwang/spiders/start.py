#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:chan time:2019/5/1
from scrapy import cmdline

# 若要停止爬虫, 并在下一次接着运行就可以再一开始的时候使用下面的命令
# JOBDIR=crawl/quanshu_1 会创建一个目录, 目录下面存放的是你上一次运行的记录

#cmdline.execute("scrapy crawl quanshu -s JOBDIR=crawl/quanshu_1".split())
cmdline.execute("scrapy crawl pauqanshu".split())
