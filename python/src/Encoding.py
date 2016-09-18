#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 chenhuan0103.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: Encoding.py
Author: chenhuan0103.com
Date: 2015/10/24 14:01:04
Desc: Python字符串编码
"""
import chardet

class Encoding:
    def __init__(self, str):
        self.__str = str

    def format(self):
        return chardet.detect(self.__str)
