#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import sys
import random

sys.path.append('..')
from common.similarity import *

def readfile(file):
    ''' 从vec文件中构建vec
    '''
    fd = open(file)
    lines = [line.strip() for line in fd.readlines() if line != '']

    # 第一行是列标题
    clonames = lines[0].strip().split('\t')[1:]

    data = []
    rownames = []
    for line in lines[1:]:
        p = line.strip().split('\t')

        # 第一列是行名
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])

    return rownames,clonames,data

def get_point_position_range(rows):
    ''' 返回每个word出现过最大值和最小值

    :param rows:  [[1, 2, 3], [2, 4, 5]]
    :return: [(min, max), (min, max), (min, max)]
    '''
    return [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]

def get_random_mid_points(rows, k):
    ''' 随机创建k个中心点

    return: [] k个随机点坐标 e.g. [[1, 2, 3]]
    '''
    # 每个word出现最小~最大范围
    ranges = get_point_position_range(rows)

    clusters = []
    for j in range(k):
        point = []
        for i in range(len(rows[0])):
            min = ranges[i][0]
            max = ranges[i][1]

            delta = random.random() * (max - min)
            point.append(min + delta)

        clusters.append(point)

    return clusters

def get_closest_mid_point(row, mid_points, distance=sim_pearson):
    ''' 返回距离当前点最近中心点index

    :param row: [1, 2, 3] 当前点坐标
    :param mid_points: [[1, 2, 3]] * k 中心点坐标
    :return: int 距离最近中心点坐标
    '''
    closest_index = 0    # 距离哪个中心点最近
    closest_distance = distance(row, mid_points[0])    # 距离中心点最近距离为多少
    for j in range(len(mid_points)):
        d = distance(row, mid_points[j])
        if d <= closest_distance:
            closest_distance = d
            closest_index = j

    return closest_index

def get_mid_point(rows):
    ''' rows中所有点平均值

    :param rows: [[1, 2, 3, 4], [2, 3, 4, 5]]
    :return: [1.5, 2.5, 3.5, 4.5]
    '''
    if len(rows) == 0:
        return []

    mid_point = []
    length = len(rows[0])
    for i in range(length):
        var = 0.0
        var += sum([row[i] for row in rows])
        mid_point.append(var/len(rows))

    return mid_point

def get_mid_points(rows, clusters):
    ''' 创建新的clusters中心点

    :return:
    '''
    k = len(clusters)
    mid_points = [[]] * k

    for i in range(k):
        # 匹配到的rows
        match_rows = [rows[j] for j in clusters[i]]
        mid_points[i] = get_mid_point(match_rows)

    return mid_points

def get_clusters(rows, mid_points, distance=sim_pearson):
    ''' 将rows中节点分配到距离最近中心点上

    :param rows: [[1, 2, 3, 4], [2, 3, 4, 5], ...] 点坐标
    :param mid_points: [[1, 2, 3, 4]] * k 中心点
    :return: [[]] * k  每个中心点对应最近点
    '''
    clusters = [[] for i in range(len(mid_points))]

    for i in range(len(rows)):
        # 获取当前点距离最近中心点
        closest_index = get_closest_mid_point(rows[i], mid_points, distance)
        clusters[closest_index].append(i)

    return clusters

def kcluster(rows, distance=sim_pearson, k=4):
    ''' K-均值聚类算法
    '''
    # 随机创建k个中心点
    mid_points = get_random_mid_points(rows, k)

    last_clusters = None
    while True:
        # 删除clusters为0的元素
        mid_points = [mid_point for mid_point in mid_points if len(mid_point) != 0]

        # 每个row距离最近的中心点, 形成聚类
        clusters = get_clusters(rows, mid_points, distance)

        if last_clusters == clusters:
            break

        last_clusters = clusters

        # 计算新中心点
        mid_points = get_mid_points(rows, clusters)

    return clusters

def print_k_cluster(clusters, blog_names):
    ''' 打印聚类结果
    '''
    print [[blog_names[i] for i in cluster]for cluster in clusters]

if __name__ == '__main__':
    rownames,clonames,data = readfile('blog_data.txt')

    blog_names = rownames
    clusters = kcluster(data, k=4)

    print_k_cluster(clusters, blog_names)
