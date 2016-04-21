#!/user/bin/env python2
# -*- coding: utf-8 -*-

import os

from crawlpage import crawl_page
from analyzehtml import analyze
from drawhtml import draw_html


if __name__ == "__main__":
    folder = "htmlfile/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    # crawl_page(start=1, end=2, user='61303280', filepath='htmlfile/')
    analyze(user='61303280', filepath='htmlfile/')



