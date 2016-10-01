#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import sys
import sqlite3

class SearchEngine:
    ''' 搜索引擎
    '''
    def __init__(self, db_name):
        ''' 初始化
        '''
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        ''' 清除
        '''
        self.conn.close()

    def get_cursor(self):
        ''' 返回数据库cursor
        '''
        return self.cursor

    def get_value_by_id(self, table, field, id):
        ''' 通过rowid获取field的值
        '''
        sql = "SELECT %s FROM %s WHERE rowid = %d" % (field, table, id)
        value = self.cursor.execute(sql).fetchone()[0]
        return value

    def get_values_by_ids(self, table, field, ids):
        ''' 获取ids 对应的 values

        :param rowids: [1, 2, 3]
        :return: ['chenhuan', 'huan']
        '''
        values = [self.get_value_by_id(table, field, id) for id in ids]
        return values

    def get_urls_by_word_id(self, word_id):
        ''' 返回满足匹配word的url列表

        :param word_id: 1
        :return: ['http://xxx', 'http://xxx']
        '''
        # 获取word_id对应url_ids
        sql = "SELECT DISTINCT url_id FROM word_location WHERE word_id = %d" % word_id
        url_ids = self.cursor.execute(sql).fetchall()
        url_ids = [url_id[0] for url_id in url_ids]

        # 获取url_ids对应的url
        urls = self.get_values_by_ids('url_list', 'url', url_ids)

        return urls

    def get_urls_by_word_ids(self, word_ids):
        ''' 返回满足匹配所有words的url列表

        :param word_ids: [1, 2, 3, 4, 5]
        :return: ['http://xxx', 'http://xxx']
        '''
        each_match_urls = [self.get_urls_by_word_id(word_id) for word_id in word_ids]

        distinct_match_urls = each_match_urls[0]
        # 取所有match_urls的并集
        for match_urls in each_match_urls[1:]:
            distinct_match_urls = set(distinct_match_urls).intersection(set(match_urls))

        return list(distinct_match_urls)
        
    def get_id_by_value(self, table, field, value):
        ''' 通过field == value 查询rowid

        :return int
        '''
        sql = "SELECT rowid FROM %s WHERE %s = '%s'" % (table, field, value)
        id = self.cursor.execute(sql).fetchone()[0]
        return id

    def get_ids_by_values(self, table, field, values):
        ''' 通过values获取value对应id

        :param values: ['chen', 'huan']
        :return: [1, 2]
        '''
        rowids = [self.get_id_by_value(table, field, value) for value in values]
        return rowids

    def get_match_urls(self, words):
        ''' 查询关联和全部words都关联的urls

        :param words: string e.g. 'programming java'
        :return ['http://xxx', 'http://xxxx']
        '''
        words = words.split(' ')
        word_ids = self.get_ids_by_values('word_list', 'word', words)
        match_urls = self.get_urls_by_word_ids(word_ids)

        return match_urls

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage %s [word] [word] ...' % sys.argv[0]
        exit(-1)

    seacher = SearchEngine('database.sqlite')
    words = ' '.join([word.lower() for word in sys.argv[1:]])
    for url in seacher.get_match_urls(words):
        print url
