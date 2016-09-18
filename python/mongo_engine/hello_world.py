#!/usr/bin/python
# _*_ coding: utf-8 _*_

from mongoengine import *

"""连接至mongoDB数据库
1. 第一个参数: 数据库名字
2. 第二个参数: host地址
3. 第三个参数: port
"""
connect('apache', host = '127.0.0.1', port = 12345)

class Access(DynamicDocument):
    """nginx用户访问记录
    使用DynamicDocument, 避免Field不存在的异常

    mongoDB记录格式如下:
    {
        "_id":"564ec99e83fceca951000006",
        "host":"127.0.0.1",
        "user":"-",
        "method":"GET",
        "path":"/",
        "code":"200",
        "size":"90422",
        "referer":"-",
        "agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
        "time":"2015-11-20T07:19:52Z"
    }
    """
    host = StringField(default='')
    user = StringField(default='') 
    method = StringField(default='')
    path = StringField(default='')
    code = IntField(default='')
    size = IntField(default='')
    referer = StringField(default='')
    agent = StringField(default='')
    time = DateTimeField(default='')

if __name__ == '__main__':
    for record in Access.objects:
        print record.code
