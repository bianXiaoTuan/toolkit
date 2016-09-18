#!/usr/bin/env python
#-*- coding:utf-8 -*-

import memcache

mc = memcache.Client(['127.0.0.1:12000'],debug=0)

name = 'jiang'
if not mc.get('name'):
    mc.set("name","chenhuan")
else:
	name = mc.get('name')
print name

mc.set_multi({ 'name': 'chenhuan', 'age': 26}, key_prefix='baidu')
print mc.get_multi(['name', 'age'], key_prefix='baidu')
