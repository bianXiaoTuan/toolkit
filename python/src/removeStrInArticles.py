#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 chenhuan0103.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: removeStrInArticles.py
Author: chenhuan0103.com
Date: 2015/10/24 14:01:04
Desc: 删除所有Article中指定字符
"""

import Mysql
import sys
import MySQLdb
import StrEncoding
import re

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    # 获取全部文章
    mysql = Mysql.Mysql('121.41.119.102', 'root', '123456', 'blog', 3306)

    sql = 'SELECT hachi_article.id,hachi_article.content FROM hachi_article'
    article = mysql.select(sql)

    for id,content in article:
        content = content.replace('<hr />', '')
        content = MySQLdb.escape_string(content)
        sql = "UPDATE hachi_article SET hachi_article.content='%s' WHERE hachi_article.id = %d" % (content, id)
        # mysql.update(sql)
