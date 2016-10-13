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

        self.clear_table_data()

    def __del__(self):
        ''' 清理
        '''
        self.cursor.close()

    def clear_table_data(self):
        ''' 清除database中数据
        '''
        tables = ['url_list', 'word_list', 'link', 'link_words', 'word_location']
        for table in tables:
            sql = "DELETE FROM %s" % table
            self.cursor.execute(sql)

        self.db_commit()

    def get_cursor(self):
        ''' 返回cursor
        '''
        return self.cursor

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

        :return: String e.g. chenhuan
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

    def get_value_by_id(self, table, field, id):
        ''' 通过rowid获取field的值
        '''
        sql = "SELECT %s FROM %s WHERE rowid = %d" % (field, table, id)
        value = self.cursor.execute(sql).fetchone()[0]
        return value

    def get_entry_id(self, table, field, value, create_new=True):
        ''' 用户entry id, 如果entry_id不存在, 则将其加入数据库
        '''
        value = value.replace("'", "")

        sql = "SELECT rowid FROM %s WHERE %s = '%s'" % (table, field, value)
        result = self.cursor.execute(sql)
        result = result.fetchone()

        if result == None:
            sql = "INSERT INTO %s (%s) values ('%s')" % (table, field, value)
            result = self.cursor.execute(sql)
            return result.lastrowid
        else:
            return result[0]

    def add_index(self, url, words):
        ''' 为网页建立索引
        将URL包含的每个word 和 URL关联起来
        word_location中location为word在url中出现位置
        '''
        if self.is_indexed(url):
            return

        print 'Indexing ' + url

        # 获取url_id
        url_id = self.get_entry_id('url_list', 'url', url)

        # 将每个单词和该url关联
        for i in range(len(words)):
            word = words[i]
            if len(word) < 3 or word in self.ignore_words:
                continue

            # 获取word_id
            word_id = self.get_entry_id('word_list', 'word', word)

            sql = '''INSERT INTO
            word_location(url_id, word_id, location)
            VALUES (%d, %d, %d)
            ''' % (url_id, word_id, i)

            self.cursor.execute(sql)

    def is_indexed(self, url):
        ''' 如果url已经建立过索引(url_list 和 word_location中都存在), 则返回True
        '''
        sql = "SELECT rowid FROM url_list WHERE url = '%s'"
        result = self.cursor.execute(sql).fetchone()

        if result != None:
            sql = "SELECT * FROM word_location WHERE url_id = %d" % result[0]
            result = self.cursor.execute(sql).fetchone()

            if result != None:
                return True

        return False

    def add_link_words(self, link_id, link_text):
        ''' 关联link_id 和 link_words

        :param link_id: int
        :param link_text: string
        '''
        word_id = self.get_entry_id('word_list', 'word', link_text)

        sql = "SELECT rowid FROM link_words WHERE word_id = %d AND link_id = %d" % (word_id, link_id)
        result = self.cursor.execute(sql)
        result = result.fetchone()

        if result == None:
            sql = "INSERT INTO link_words (word_id, link_id) values (%d, %d)" % (word_id, link_id)
            self.cursor.execute(sql)

    def add_link(self, url_from_id, url_to_id):
        ''' 关联url_from 至 url_to

        :param url_from_id: int
        :param url_to_id: int
        :return: link_id
        '''
        sql = "SELECT rowid FROM link WHERE from_id = %d AND to_id = %d" % (url_from_id, url_to_id)
        result = self.cursor.execute(sql)
        result = result.fetchone()

        if result == None:
            sql = "INSERT INTO link (from_id, to_id) values (%d, %d)" % (url_from_id, url_to_id)
            result = self.cursor.execute(sql)
            return result.lastrowid
        else:
            return result[0]

    def add_link_ref(self, url_from, url_to, link_text):
        ''' 添加一个关联两个网页链接

        :param url_from: String
        :param url_to: String
        :param link_text: String
        :return:
        '''
        url_from_id = self.get_entry_id('url_list', 'url', url_from)
        url_to_id = self.get_entry_id('url_list', 'url', url_to)

        # 插入link
        link_id = self.add_link(url_from_id, url_to_id)

        # 插入link_words
        self.add_link_words(link_id, link_text)

    def get_url_html(self, page):
        ''' 获取URL的HTML

        :param page: string url
        :return: None = page无法解析
        '''
        try:
            c = urllib2.urlopen(page)
        except:
            print 'Could not open %s' % page
            return None

        return c.read()

    def is_url(self, url):
        ''' 检查是以http开头, 为url

        :return: True = 以http开头
        '''
        return url[0:4] == 'http'

    def get_id_by_value(self, table, field, value):
        ''' 通过field == value 查询rowid

        :return int
        '''
        sql = "SELECT rowid FROM %s WHERE %s = '%s'" % (table, field, value)
        id = self.cursor.execute(sql).fetchone()[0]
        return id

    def get_to_url_ids_by_soup(self, url_id):
        ''' 通过url->beautifulsoup获取子链接的url_ids
        '''
        # url_id 转化成 url
        page = self.get_value_by_id('url_list', 'url', url_id)

        # 获取url的HTML内容
        html = self.get_url_html(page)
        if html == None: return
        soup = BeautifulSoup(html, 'html.parser')

        # 递归处理子链接
        links = soup('a')
        son_url_ids = []
        for link in links:
            if 'href' in dict(link.attrs):
                url = urljoin(page, link['href'])
                url = url.split('#')[0]

                son_url_ids.append(self.get_id_by_value('url_list', 'url', url))

        return list(set(son_url_ids))

    def get_to_url_ids_by_sql(self, url_id):
        ''' 通过SQL中获取from_id对应的to_id
        '''
        sql = "SELECT to_id FROM link WHERE from_id = %d" % (url_id)
        url_ids = self.cursor.execute(sql).fetchall()

        return list(set([url_id[0] for url_id in url_ids]))

    def check_link_ref(self, url_id):
        ''' 返回url_id对应的url_to_id

        :param url_id: int e.g. 37
        :return: [1, 2, 3, 4]
        '''
        to_url_ids_1 = self.get_to_url_ids_by_soup(url_id)
        to_url_ids_2 = self.get_to_url_ids_by_sql(url_id)

        if to_url_ids_1 == to_url_ids_2:
            print 'Link Success'
        else:
            print 'Link Fail'

    def crawl(self, pages, depth=2):
        ''' 爬虫进行广度优先搜索, 并为网页建立索引
        '''
        for i in range(depth):
            new_pages = set()

            for page in pages:
                if page.find('chenhuan0103') == -1:
                    continue

                # 获取HTML内容
                html = self.get_url_html(page)
                if html == None: continue
                soup = BeautifulSoup(html, 'html.parser')

                # 获取页面包含words
                words = self.get_words(soup)

                # 为当前页面添加索引
                self.add_index(page, words)

                # 递归处理子链接
                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        url = url.split('#')[0]

                        # 检查是否为合格URL, 且未被索引
                        if self.is_url(url) and not self.is_indexed(url):
                            new_pages.add(url)

                        # 关联page->url链接
                        self.add_link_ref(page, url, self.get_text(link))

                # 统一提交变更
                self.db_commit()
            pages = new_pages


if __name__ == '__main__':
    pages = ['http://chenhuan0103.com']

    crawler = Crawler('database.sqlite')
    crawler.crawl(pages, depth=2)
    crawler.check_link_ref(37)
