#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import unittest
from crawler import *
from bs4 import BeautifulSoup

class ClusterTest(unittest.TestCase):

    def setUp(self):
        ''' 初始化
        '''
        self.crawler = Crawler('database.sqlite')
        self.table = 'test'

        # 创建一个测试表
        self.cursor = self.crawler.get_cursor()
        sql = "create table %s(word)" % self.table
        try:
            self.cursor.execute(sql)
        except:
            pass

    def tearDown(self):
        ''' 清理
        '''
        pass

    def test_get_entry_id(self):
        ''' 测试get_entry_id()
        '''
        entry_id = self.crawler.get_entry_id(self.table, 'word', 'chenhuan')

        sql = "SELECT rowid FROM %s WHERE word = '%s'" % (self.table, 'chenhuan')
        result = self.cursor.execute(sql).fetchone()[0]

        self.assertEqual(result, entry_id, 'get_entry_id fail')

    def test_get_url_html(self):
        ''' 测试get_url_html
        '''
        html = self.crawler.get_url_html('http://chenhuan0103.com')

        soup = BeautifulSoup(html, 'html.parser')
        blog_name = soup('a')[0].string

        self.assertEqual(blog_name, 'BianXiaoTuan')

    def test_get_words(self):
        ''' 测试get_words
        '''
        html = '''
        <a hrep="http://abc">chen<p>jiang hong</p> huan</a>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup('a')[0]
        words = self.crawler.get_words(soup)

        self.assertEqual(words, ['chen', 'jiang', 'hong', 'huan'], 'get_words fail')

    def test_get_text(self):
        ''' 测试get_text
        '''
        html = '''
        <a hrep="http://abc">chen huan</a>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup('a')[0]
        text = self.crawler.get_text(soup)

        self.assertEqual(text, 'chen huan', 'get_text fail')

    def test_separate_words(self):
        ''' 测试separate_words
        '''
        text = 'chen huan jiang hong pang guai'
        text = self.crawler.separate_words(text)
        self.assertEqual(text, ['chen', 'huan', 'jiang', 'hong', 'pang', 'guai'], 'separate_words fail')

if __name__ == '__main__':
    unittest.main()
