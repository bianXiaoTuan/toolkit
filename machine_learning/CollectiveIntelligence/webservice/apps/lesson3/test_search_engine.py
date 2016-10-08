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

    def test_get_value_by_id(self):
        ''' 测试get_value_by_id
        '''
        value = self.searcher.get_value_by_id('test', 'word', 1)
        self.assertEqual(value, 'chenhuan', 'get_value_by_id failed')

    def test_get_values_by_ids(self):
        ''' 测试get_value_by_id
        '''
        values = self.searcher.get_values_by_ids('test', 'word', [1, 2])
        self.assertEqual(values, ['chenhuan', 'jianghong'], 'get_values_by_ids failed')

    def test_get_id_by_value(self):
        ''' 测试get_id_by_value
        '''
        id = self.searcher.get_id_by_value('test', 'word', 'chenhuan')
        self.assertEqual(id, 1, 'get_id_by_value failed')

    def test_get_ids_by_values(self):
        ''' 测试get_values_by_ids
        '''
        ids = self.searcher.get_ids_by_values('test', 'word', ['chenhuan', 'jianghong'])
        self.assertEqual(ids, [1, 2], 'get_ids_by_values failed')

    def test_get_score_by_words_frequency(self):
        ''' 测试get_score_by_words_frequency
        '''
        frequency = self.searcher.get_score_by_words_frequency('http://chenhuan0103.com', [316, 1601])
        print frequency

if __name__ == '__main__':
    unittest.main()
