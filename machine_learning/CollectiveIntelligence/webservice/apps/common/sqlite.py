#!/usr/bin/env python
#_*_ encoding=utf-8 _*_
import sqlite3

def create_tables():
    ''' sqlite hello world
    '''
    # Connect to sqlite
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    # 创建数据库表
    c.execute('create table url_list(url)')
    c.execute('create table word_list(word)')
    c.execute('create table word_location(url_id, word_id, location)')
    c.execute('create table link(from_id integer, to_id integer)')
    c.execute('create table link_words(word_id, link_id)')

    # 创建索引
    c.execute('create index url_index on url_list(url)')
    c.execute('create index word_index on word_list(word)')
    c.execute('create index word_url_index on word_location(word_id)')
    c.execute('create index url_to_index on link(to_id)')
    c.execute('create index url_from_index on link(from_id)')

    # Save (commit) the changes
    conn.commit()

    # We can also close the cursor if we are done with it
    c.close()

if __name__ == '__main__':
    create_tables()

