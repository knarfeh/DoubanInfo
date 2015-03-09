# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    crawlpage.py
# Description :    爬取豆瓣已看电影网页
# Author      :    Frank
# Date        :    2014.03.08
# ######################################################

import os
import urllib2
import time
from BeautifulSoup import BeautifulSoup

def crawl_page(start=1, end=0, user='61303280', filepath='htmlfile/'):
    u"""
    爬取网页，从start页爬取到end页，如果end是0，爬取所有的页
    :param start: 起始页
    :param end: 结束页
    :param user: 用户ID
    :param filepath: 保存文件夹的路径，最后一个字符是/
    :return:
    """
    if not os.path.exists(filepath + user):
        os.makedirs(filepath + user)
    if end == 0:
        content = urllib2.urlopen('http://movie.douban.com/people/'+user+'/collect').read()
        soup = BeautifulSoup(content)
        end = int(soup.find('span', {'class': 'thispage'})['data-total-page'])   # 获得总共页数
    for index in range(start, end+1):
        content = urllib2.urlopen('http://movie.douban.com/people/'
                                  + user + '/collect?start='
                                  + str(15*(index-1))
                                  + '&sort=time&rating=all&filter=all&mode=grid').read()
        with open(os.path.join(filepath, user, str(index)+'.html'), 'w') as output:
            output.write(content)
        print user, index, 'done'
        time.sleep(3)