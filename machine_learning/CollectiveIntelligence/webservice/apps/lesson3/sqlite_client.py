#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import sqlite3

class SqliteClint:
    ''' sqlite 客户端, 封装sql操作
    '''

    def __init__(self, db_name):
        ''' 初始化
        '''
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        ''' 清理
        '''
        self.cursor.close()















