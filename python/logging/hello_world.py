#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

log_format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
logging.basicConfig(
	level=logging.DEBUG,
	format=log_format,
	datefmt="%a, %d %b %Y %H:%M:%S",
	filename='hello_world.log',
	filemode='w'
	)

# 定义RotatingFileHandler, 最多备份5个日志, 每个日志最大10M
Rthandler = RotatingFileHandler('hello_world.log', maxBytes=10*1024*1024,backupCount=5)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)

logging.debug('This is a debug message')
logging.info('This is a info message')
logging.warning('This is a warning message')