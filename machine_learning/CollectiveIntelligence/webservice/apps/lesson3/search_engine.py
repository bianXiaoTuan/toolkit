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

    def get_rowid_by_value(self, table, field, value):
        ''' 通过field == value 查询rowid

        :return int
        '''
        sql = "SELECT rowid FROM %s WHERE %s = '%s'" % (table, field, value)
        rowid = self.cursor.execute(sql).fetchone()[0]
        return rowid

    def get_rowids_by_values(self, table, field, values):
        ''' 通过values获取value的全部id

        :param values: ['chen', 'huan']
        :return: [1, 2]
        '''
        rowids = []
        for value in values:
            rowids.append(self.get_rowid_by_value(table, field, value))

        return rowids

    def get_value_by_rowid(self, table, field, rowid):
        ''' 通过rowid获取field的值
        '''
        sql = "SELECT %s FROM %s WHERE rowid = %d" % (field, table, rowid)
        value = self.cursor.execute(sql).fetchone()[0]
        return value

    def get_values_by_rowids(self, table, field, rowids):
        ''' 获取

        :param rowids: [1, 2, 3]
        :return: ['chenhuan', 'huan']
        '''
        values = []
        for rowid in rowids:
            values.append(self.get_value_by_rowid(table, field, rowid))
        return values

    def get_match_urls_by_word_rowid(self, word_rowid):
        ''' 返回满足匹配word的url列表

        :param word_rowid: 1
        :return: ['http://xxx', 'http://xxx']
        '''
        # 获取rowid对应url_ids
        sql = "SELECT DISTINCT url_id FROM word_location WHERE word_id = %d" % word_rowid
        url_ids = self.cursor.execute(sql).fetchall()
        url_ids = [url_id[0] for url_id in url_ids]

        # 获取url_ids对应的url
        urls = self.get_values_by_rowids('url_list', 'url', url_ids)

        return urls

    def get_match_urls_by_word_rowids(self, word_rowids):
        ''' 返回满足匹配所有words的url列表

        :param word_rowids: [1, 2, 3, 4, 5]
        :return: ['http://xxx', 'http://xxx']
        '''
        each_match_urls = []
        for word_rowid in word_rowids:
            each_match_urls.append(self.get_match_urls_by_word_rowid(word_rowid))

        distinct_match_urls = each_match_urls[0]
        for match_urls in each_match_urls[1:]:
            distinct_match_urls = set(distinct_match_urls).intersection(set(match_urls))

        return list(distinct_match_urls)

    def get_match_urls(self, words):
        ''' 查询关联所有words的urls

        :param query: string 'programming java'
        '''
        words = words.split(' ')
        word_rowids = self.get_rowids_by_values('word_list', 'word', words)
        match_urls = self.get_match_urls_by_word_rowids(word_rowids)

        return match_urls

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage %s [word] [word] ...' % sys.argv[0]
        exit(-1)

    seacher = SearchEngine('database.sqlite')
    words = ' '.join([word.lower() for word in sys.argv[1:]])
    print seacher.get_match_urls(words)

