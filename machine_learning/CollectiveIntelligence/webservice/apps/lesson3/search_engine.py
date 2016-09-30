#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

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

    def get_rowid_by_field(self, table, field, value):
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
            rowids.append(self.get_rowid_by_field(table, field, value))

        return rowids

    def get_match_urls(self, words):
        ''' 查询关联所有words的urls

        :param query: string 'programming java'
        :return:
        '''
        words = words.split(' ')
        word_rowids = self.get_rowids_by_values('word_list', 'word', words)









