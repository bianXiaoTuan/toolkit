#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import re
import urllib2
import sqlite3
from bs4 import BeautifulSoup
from urlparse import urljoin

class Crawler:
    ''' 网络爬虫
    '''
    def __init__(self, db_name):
        ''' 初始化
        '''
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.ignore_words = set([])

    def __del__(self):
        ''' 清理
        '''
        self.cursor.close()

    def db_commit(self):
        ''' 提交数据库变更
        '''
        self.conn.commit()

    def separate_words(self, text):
        ''' 分词
        '''
        spliter = re.compile('\\W*')
        return [s.lower() for s in spliter.split(text) if s != '']

    def get_text(self, soup):
        ''' 从HTML网页中提取不带标签文字

        e.g. <a hrep='http:xxxx'>chenhuan</a>获取chenhuan
        '''
        # 如果标签没有嵌套关系, 直接返回HTML值
        text = soup.string
        if text != None:
            return text.strip()

        # 如果标签有嵌套关系, 需要递归调用
        contents = soup.contents
        texts = ''
        for content in contents:
            subtext = self.get_text(content)
            texts += subtext + '\n'
        return texts

    def get_words(self, soup):
        ''' 提取出soup中所有string

        return [string]
        '''
        text = self.get_text(soup)
        words = self.separate_words(text)
        return words

    def get_entry_id(self, table, field, value, create_new=True):
        ''' 用户entry id, 如果entry_id不存在, 则将其加入数据库
        '''
        sql = "SELECT rowid FROM %s WHERE %s = '%s'" % (table, field, value)
        result = self.cursor.execute(sql)
        result = result.fetchone()

        if result == None:
            sql = "INSERT INTO %s (%s) values ('%s')" % (table, field, value)
            result = self.cursor.execute(sql)
            return result.lastrowid
        else:
            return result[0]

    def add_to_index(self, url, soup):
        ''' 每个网页建立索引
        '''
        if self.is_indexed(url):
            return

        print 'Indexing ' + url

        # 获取url中单词
        words = self.get_words(soup)

        # 获取url_id
        url_id = self.get_entry_id('url_list', 'url', url)

        # 将每个单词和该url关联
        for i in range(len(words)):
            word = words[i]
            if word in self.ignore_words:
                continue

            word_id = self.get_entry_id('word_list', 'word', word)

            sql = 'INSERT INTO word_location(url_id, word_id, location) VALUES (%d, %d, %d)' % (url_id, word_id, i)
            self.cursor.execute(sql)

    def is_indexed(self, url):
        ''' 如果url已经建立过索引, 则返回True
        '''
        sql = "SELECT rowid FROM url_list WHERE url = '%s'"
        result = self.cursor.execute(sql).fetchone()

        if result != None:
            sql = "SELECT * FROM word_location WHERE url_id = %d" % result[0]
            result = self.cursor.execute(sql).fetchone()

            if result != None:
                return True

        return False

    def add_link_ref(self, url_from, url_to, link_text):
        ''' 添加一个关联两个网页链接
        '''
        pass


    def crawl(self, pages, depth=2):
        ''' 爬虫进行广度优先搜索, 并为网页建立索引
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

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])

                        if url.find("'") != -1:
                            continue

                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.is_indexed(url):
                            new_pages.add(url)

                        link_text = self.get_text(link)
                        self.add_link_ref(page, url, link_text)

                self.db_commit()

            pages = new_pages

if __name__ == '__main__':
    crawler = Crawler('sqlite.database')
    pages = ['http://baike.baidu.com/jingji/']

