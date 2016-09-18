#!/usr/bin/env python
# -*- coding:utf-8 -*-

arr1 = range(-5, 5)
arr2 = filter(lambda n:n > 0, arr1)

lambda_add = lambda x, y : x + y
print lambda_add(5, 6)
