#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
自定义上下文管理器, with用法 
"""

class MyContextManager(object):
    def __enter__(self):
        print "entering..."

    def __exit__(self, exception_type, exception_value, traceback):
        print "leaving..."
        if exception_type is None:
            print 'no exception'
            return False
        elif exception_type is ValueError:
            print 'value error'
            return True
        else:
            print 'other error'
            return True
