# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Douban.py
# Description :    主程序入口
# Author      :    Frank
# Date        :    2014.03.08
# ######################################################

import os

from crawlpage import crawl_page
from analyzehtml import analyze
from drawhtml import drawHTML

if __name__ == "__main__":
    folder = "htmlfile/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    # crawl_page(start=1, end=0, user='52269090', filepath='htmlfile/')
    analyze(user='52269090', filepath='htmlfile/')



