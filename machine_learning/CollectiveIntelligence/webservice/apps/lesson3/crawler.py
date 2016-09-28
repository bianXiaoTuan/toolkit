#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin

class Crawler:
    ''' 网络爬虫
    '''
    def __init__(self, db_name):
        ''' 初始化
        '''
        pass

    def __del__(self):
        pass

    def db_commit(self):
        pass

    def get_entry_id(self, table, field, value, create_new=True):
        ''' 用户entry id, 如果entry_id不存在, 则将其加入数据库
        '''
        return None

    def add_to_index(self, url, soup):
        ''' 每个网页建立索引
        '''
        print 'Indexing %s' % url

    def get_text_only(self, soup):
        ''' 从HTML网页中提取不带标签文字
        '''
        return None

    def separate_words(self, text):
        ''' 分词
        '''
        return None

    def is_indexed(self, url):
        ''' 如果url已经建立过索引, 则返回True
        '''
        return False

    def add_link_ref(self, url_from, url_to, link_text):
        ''' 添加一个关联两个网页链接
        '''
        pass


    def create_index_tables(self):
        ''' 创建数据库
        '''
        pass

    def crawl(self, pages, depth=2):
        ''' 爬虫进行广度优先搜索, 并未网页建立索引
        '''
        for i in range(depth):
            new_pages = set()

            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print 'Could not open %s' % page
                    continue

                soup = BeautifulSoup(c.read())
                self.add_to_index(page, soup)

                # 获取URL
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])

                        if url.find("'") != -1:
                            continue

                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.is_indexed(url):
                            new_pages.add(url)

                        link_text = self.get_text_only(link)
                        self.add_link_ref(page, url, link_text)

                self.db_commit()

            pages = new_pages


