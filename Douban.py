# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Douban.py
# Description :    主程序入口
# Author      :    Frank
# Date        :    2014.03.08
# ######################################################

import os
import urllib2
import time
import datetime
from BeautifulSoup import BeautifulSoup

def crawl_page(start=1, end=0, user='61303280', filepath='htmlfile/'):
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

def drawHTML(dates, rates, tag_count, user):
    """
    输出带图表的html文件
    :param dates:  观看时间的列表
    :param rates:
    :param tag_count:
    :param user:
    :return:
    """
    dates = sorted(dates)

def analyze(user='61303280'):
    pass


if __name__ == "__main__":
    folder = "htmlfile/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    crawl_page(start=1, end=0, user='52269090', filepath='htmlfile/')
    analyze(user='61303280')




