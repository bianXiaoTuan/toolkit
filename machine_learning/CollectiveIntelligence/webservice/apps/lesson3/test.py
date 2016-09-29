#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import unittest
from crawler import *
from bs4 import BeautifulSoup

class ClusterTest(unittest.TestCase):

    def setUp(self):
        ''' 初始化
        '''
        self.crawler = Crawler('sqlite.database')

    def tearDown(self):
        ''' 清理
        '''
        pass

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
