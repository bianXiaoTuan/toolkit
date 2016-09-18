#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
python函数传参 == 传对象
"""

def change_list(arr):
    arr[0] = 1

def change_int(a):
    a = 1

if __name__ == '__main__':
    arr = [0, 1, 2]
    a = 0

    change_list(arr)
    change_int(a)

    print arr
    print a
