#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
from mongoengine import *
connect('access_record', host = 'chenhuan0103.com', port=12345)

class NginxAccessRecord(DynamicDocument):
    """nginx 访问日志记录
    """
    host = StringField()
    user = StringField() 
    method = StringField()
    path = StringField()
    code = IntField()
    size = IntField()
    referer = StringField()
    agent = StringField()
    time = DateTimeField()

if __name__ == '__main__':
	start = time.time()
	print len(NginxAccessRecord.objects(path__contains="articleFront/view&id="))
	end = time.time()
	print end - start

	start = time.time()
	print len(NginxAccessRecord.objects(Q(path__contains="articleFront/view&id=") & (Q(agent__ne="Baidu") | Q(agent__ne="Google"))))
	end = time.time()
	print end - start
