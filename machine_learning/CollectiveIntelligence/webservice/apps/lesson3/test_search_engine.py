#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import unittest
from search_engine import *
from bs4 import BeautifulSoup

class SearchEngineTest(unittest.TestCase):

    def setUp(self):
        ''' 初始化
        '''
        # 测试爬虫
        self.searcher = SearchEngine('database.sqlite')
        self.table = 'test'

        # 创建一个测试表
        self.cursor = self.searcher.get_cursor()
        sql = "create table %s(word)" % self.table
        try:
            self.cursor.execute(sql)
        except:
            pass

    def tearDown(self):
        ''' 清理
        '''

    def test_get_rowid_by_field(self):
        ''' 测试get_rowid_by_field
        '''
        rowid1 = self.searcher.get_rowid_by_field('test', 'word', 'chenhuan')
        rowid2 = self.searcher.get_rowid_by_field('test', 'word', 'jianghong')

        self.assertEqual(rowid1, 1, 'get_rowid_by_field fail')
        self.assertEqual(rowid2, 2, 'get_rowid_by_field fail')

    def test_get_wordids_by_words(self):
        ''' 测试get_wordids_by_words
        '''
        rowids = self.searcher.get_rowids_by_values('test', 'word', ['chenhuan', 'jianghong'])
        self.assertEqual(rowids, [1, 2], 'get_rowids_by_field fail')

if __name__ == '__main__':
    unittest.main()
