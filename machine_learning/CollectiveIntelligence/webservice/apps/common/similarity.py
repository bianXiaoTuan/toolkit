#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

from math import *

def sim_distance(vec1, vec2):
    ''' 根据欧几里得距离返回两个人相似系数

    :param vec1: [] e.g. [1, 2, 3, 4, 6]
    :param vec2: [] e.g. [2, 3, 4, 5, 0]
    :return: int 0~1 越相近, 则数字越小
    '''
    if len(vec1) != len(vec2):
        raise Exception('len(vec1) != len(vec2)')

    sum_of_squares = sum([pow(vec1[i] - vec2[i], 2) for i in range(len(vec1))])

    return 1 - 1 / (1 + sum_of_squares)

def sim_pearson(vec1, vec2):
    ''' 根据皮尔逊相关系数返回两个人相似系数

    :param vec1: [] e.g. [1, 2, 3, 4, 6]
    :param vec2: [] e.g. [2, 3, 4, 5, 0]
    :return: int 0~1 越相近的数字, 距离越小
    '''
    if len(vec1) != len(vec2):
        raise Exception('len(vec1) != len(vec2)')

    n = len(vec1)

    sum1 = sum(vec1)
    sum2 = sum(vec2)

    sum12 = sum([vec1[i] * vec2[i] for i in range(len(vec1))])

    sum1pow2 = sum([pow(vec1[i], 2) for i in range(len(vec1))])
    sum2pow2 = sum([pow(vec2[i], 2) for i in range(len(vec1))])

    element = n * sum12 - sum1 * sum2
    denominator = sqrt((n * sum1pow2 - pow(sum1, 2)) * (n * sum2pow2 - pow(sum2, 2)))

    if denominator == 0:
        return 0

    # 越相近, 数字越小
    return 1 - element / denominator

def test():
    ''' 检查import该文件是否成功
    '''
    return 'HelloWorld'

if __name__ == '__main__':
    vec1 = [0, 1, 2, 3, 4, 5]
    vec2 = [1, 2, 3, 4, 5, 7]
    vec3 = [2, 3, 4, 5, 6, 9]

    print sim_pearson(vec1, vec2)
    print sim_pearson(vec2, vec3)

