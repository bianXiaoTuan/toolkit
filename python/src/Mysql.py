#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 chenhuan0103.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: mysql.py
Author: chenhuan0103.com
Date: 2015/10/24 14:01:04
Desc: 封装Mysql数据库操作
"""

import MySQLdb

class Mysql:
    def __init__(self, host, user, passwd, db, port):
        """初始化DB信息

        Args:
            host:  数据库hostname
            user:  数据库user
            passwd:  数据库passwd
            db:  数据库db
            port:  数据库port
        """
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__db = db
        self.__port = port

        #连接至数据库
        try:
           self.__conn = MySQLdb.connect(self.__host, self.__user, self.__passwd, self.__db, self.__port, charset='utf8')
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        self.__cur = self.__conn.cursor()

    def __del__(self):
        """释放conn和cursor
        """
        try:
            self.__cur.close()
            self.__conn.commit()
            self.__conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def select(self, sql):
        """执行select SQL语句

        Args:
            sql: SQL语句

        Returns:
            result: [], select结果
        """
        try:
            infos = self.__cur.execute(sql)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        infos = self.__cur.fetchmany(infos)

        result = []
        for info in infos:
            result.append(info)

        return result

    def insert(self, sql):
        """执行insert SQL语句

        Args:
            sql: SQL语句
        """
        try:
            self.__cur.excute(sql)
        except MySQLdb.Error,e:
            self.__conn.rollback()
            print "Mysql Error: %s" % (e)

    def update(self, sql):
        """更新
        """
        try:
            self.__cur.execute(sql)
        except MySQLdb.Error,e:
            self.__conn.rollback()
            print "Mysql Error: %s" % (e)

if __name__ == '__main__':
    mysql = Mysql('121.41.119.102', 'root', '123456', 'blog', 3306)
    articles = mysql.select('select hachi_article.content from hachi_article')
    for article in articles:
        print article
