#!/user/bin/env python2
# -*- coding: utf-8 -*-


import os
import re
from BeautifulSoup import BeautifulSoup
from drawhtml import draw_html


def analyze(user='61303280', filepath='htmlfile/'):
    u"""
    根据爬取的豆瓣网页，返回观看日期，评分，标签等统计信息
    :param user:
    :param filepath:
    :return:
    """
    tag_count = {}
    dates = []
    rates = [0 for _ in xrange(6)]
    for doubanHtml in os.listdir(os.path.join(filepath, user)):
        with open(os.path.join(filepath, user, doubanHtml), 'r') as fileopend:
            content = fileopend.read()
            soup = BeautifulSoup(content.decode('utf8', 'ignore'))
            for item in soup.findAll('div', {'class': 'item'}):
                intro = str(item.find('li', {'class': 'intro'}).string.encode('utf8', 'ignore'))
                # 为了提取标签的信息
                intro = set(word.strip() for word in intro.split('/') if '分钟' not in word)
                rate = item.find('span', {'class': re.compile('rating[1-5].*')})
                # 获得评分，如果没有就评分，就置为0
                if rate:
                    rate = re.search('rating([1-5]).*', str(rate['class'])).group(1)
                else:
                    rate = '0'
                # 获得观看的日期
                date = str(item.find('span', {'class': 'date'}).string.encode('utf8', 'ignore'))
                tags = item.find('span', {'class': 'tags'})
                if tags:
                    tags = str(tags.string.encode('utf8', 'ignore'))
                    tags = set([tag for tag in tags.split()
                                if '标签' not in tag and '标签'.decode('utf8').encode('gbk') not in tag])
                else:
                    tags = set()
                if len(tags) != 0:
                    tags = intro.union(tags)
                else:
                    tags = intro

                dates.append((date, rate))
                rates[int(rate)] += 1
                for tag in tags:
                    if tag not in tag_count:
                        tag_count[tag] = [0 for _ in xrange(6)]
                    tag_count[tag][int(rate)] += 1    # 存储这个tag打rate（1-5）的次数有多少次
    # print tag_count

    # 观看电影的日期
    # with open('dates.txt', 'w') as f:
    #     dates = sorted(dates)
    #     f.write('\n'.join(['\t'.join(date) for date in dates])+'\n')
    # # 观看电影的评级
    # with open('rates.txt', 'w') as f:
    #     for i in xrange(6):
    #         f.write(str(i) + '\t' + str(rates[i]) + '\n')
    # # 观看电影的标签记录
    # # print tag_count {'': [0, 1, 0, 0, 0, 7],}
    # with open('tags.txt', 'w') as f:
    #     tags = [(tag, [float(sum(count[4:]))/sum(count), float(count[5])/sum(count),  # 4 5星加起来占比，5星占比
    #             count[5], count[4], count[3], count[2], count[1]])
    #             for tag, count in tag_count.iteritems() if sum(count) > 3 and len(tag.strip()) > 0]
    #     tags = sorted(tags, key=lambda x: x[1], reverse=True)
    #     # print tags # [('\xe9\x9f\xa9\xe8\xaf\xad', [1.0, 1.0, 9, 0, 0, 0, 0]),]
    #     for tag in tags:
    #         f.write(tag[0]+'\t'+'\t'.join(str(i) for i in tag[1])+'\n')

    draw_html(dates, rates, tag_count, user, filepath)
