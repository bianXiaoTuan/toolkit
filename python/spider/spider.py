#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 chenhuan0103.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: spider.py
Author: chenhuan0103.com
Date: 2015/11/03 10:00:00
Desc: spider
"""

import re
import urllib
import traceback
from HTMLParser import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider:
    """抓取网页
    """
    def get_html(self, url):
        """抓取网页信息

        Returns:
            html: 字符串
        """
        page = urllib.urlopen(url)
        html = '' 
        for line in page.readlines():
            html = html + line.strip()
        return html

class UrlParser(HTMLParser):
    """解析www.zongchou.com获取子项目URL
    """
    def __init__(self):
        """初始化函数
        """
        HTMLParser.__init__(self)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        """获取全部URL
        """
        if tag == 'a':
            if attrs and ('class', 'siteCardICH3') in attrs:
                for (key, value) in attrs:
                    if key == 'href':
                        self.urls.append(value)

    def close(self):
        """返回全部URL
        """
        HTMLParser.close(self)
        return self.urls

class HtmlParser():
    """HTML页面分析, 获取正则表达式匹配关键词
    """
    def __init__(self, url, regex_dict):
        """初始化函数

        Args:
            url: string 待分析网页url
            regex_dict: 字典 提取信息的正则表达式, 被提取字段使用()标示, 例子:
            {
                'title':r'<h1 class="jlxqTitle_h3">(.+)</h1>',
                ...
            }
        """
        self.url = url
        self.regex_dict = regex_dict
        self.html = self.__pre_process_html()

    def __pre_process_html(self):
        """对HTML文件做压缩预处理
        """
        page = urllib.urlopen(self.url)
        html = '' 
        for line in page.readlines():
            html = html + line.strip()
        return html

    def __get_info(self, regex):
        """按照regex从页面中提取信息

        Args:
            regex: string 正则表达式

        Returns: 
            result: [] 匹配到关键词
        """
        pattern = re.compile(regex)
        info_r = pattern.findall(self.html)
        return info_r

    def run(self):
        """返回正则表达式对应关键词

        Returns:
            resule: {} 例子:
            {
                'title':[''],
                'fields':['工艺', '农艺'],
            }
        """
        result = {}
        for key,regex in self.regex_dict.items():
            result[key] = self.__get_info(regex)
        return result

if __name__ == '__main__':
    try:
        # 获取众筹网全部项目url
        spider = Spider()
        html = spider.get_html("http://www.zhongchou.com/")
        parser = UrlParser()
        parser.feed(html)
        urls = parser.close()

        zhongchou_regex_dict = {
            u'项目名称': r'<h1 class="jlxqTitle_h3">(.+?)</h1>',
            u'公益领域': r'<a href=".+?" target="_blank" class="hoUdCLink">(.+?)</a>',
            u'支持数': r'<div class="xqDetailDataBox"><div class="xqDetailData"><p class="ftP">(.+?)</p><p class="scP">支持数</p></div>',
            u'已筹款': r'</div><div class="xqDetailData"><p class="ftP">(.+?)</p><p class="scP">已筹款</p></div>',
            u'目标筹款': r'<span class="rightSpan">目标筹资<b>(.+?)</b></span>',
            u'发起机构': r'<a href=".+?" class="countA hoUdLink">(.+?)</a>',
        }
        for url in urls:
            parser = HtmlParser(url, zhongchou_regex_dict)
            result = parser.run()
            for key,values in result.items():
                print key
                for value in values:
                    print value
                print '-'*10
            print '*'*30


    except Exception,e:
        print traceback.format_exc()
