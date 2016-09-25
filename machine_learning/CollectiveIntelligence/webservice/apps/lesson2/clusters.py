#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import sys
import json
sys.path.append('..')
from common.similarity import *

class BiCluster:
    ''' 聚类
    '''
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id

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

def get_blog_words(filename):
    ''' 从vec文件中构建vec
    '''
    fd = open(filename)
    lines = [line.strip() for line in fd.readlines() if line != '']

    # 第一行是words
    word_names = lines[0].strip().split('\t')

    blog_words = []
    for line in lines[1:]:
        p = line.strip().split('\t')

        blog_name = p[0]
        words = [word_names[i] for i in range(1, len(p)) if p[i] != '0']

        blog_words.append(json.dumps({blog_name : words}))

    return blog_words

def get_cluster(rows):
    ''' 返回BiCluster的列表

    :param rows: [[1,2,3], [4,5,6]]
    :return: [BiCluster]
    '''
    # rows中每个列表长度必须相同
    lengths = [len(l) for l in rows]
    if len(set(lengths)) != 1:
        raise Exception("rows' list's length must be the same")

    return [BiCluster(vec = rows[i], id = i) for i in range(len(rows))]

def get_closest_pair(cluster, distances, distance=sim_pearson):
    ''' 返回distance最小的pair

    :param cluster: [BiCluster]
    :param distances: {(id1, id2) : distance} 缓存pair间距离
    :param distance: 计算相似度方法
    :return:
    '''
    closest_pair = (0, 1)
    closest_distance = distance(cluster[0].vec, cluster[1].vec)

    # 遍历每个配对, 寻找最小距离
    for i in range(len(cluster)):
        for j in range(i + 1, len(cluster)):
            # 用distances缓存距离, 避免重复计算
            if (cluster[i].id, cluster[j].id) not in distances:
                distances[(cluster[i].id, cluster[j].id)] = distance(cluster[i].vec, cluster[j].vec)

            d = distances[(cluster[i].id, cluster[j].id)]

            if d < closest_distance:
                closest_pair = (i, j)
                closest_distance = d

    return closest_pair,closest_distance

def hcluster(rows, distance=sim_pearson):
    ''' 聚类算法, 将相似度最高两个节点合成聚类
    '''
    distances = {}
    current_cluster_id = -1
    cluster = get_cluster(rows)

    while len(cluster) > 1:
        # 获取距离最小pair
        closest_pair,closest_distance = get_closest_pair(cluster, distances, distance)

        # 计算两个聚类平均值
        merge_vec = [(cluster[closest_pair[0]].vec[i] + cluster[closest_pair[1]].vec[i]) for i in range(len(cluster[0].vec))]

        # 建立新聚类
        new_bi_cluster = BiCluster(merge_vec,
                                left=cluster[closest_pair[0]],
                                right=cluster[closest_pair[1]],
                                distance=closest_distance, id=current_cluster_id)

        # 不在原始集合中聚类, 其id为负数
        current_cluster_id -= 1

        del cluster[closest_pair[0]]
        # 删除之后index代表的含义会变化
        if closest_pair[0] > closest_pair[1]:
            del cluster[closest_pair[1]]
        else:
            del cluster[closest_pair[1] - 1]

        cluster.append(new_bi_cluster)

    return cluster[0]

def print_cluster(cluster, labels=None, n=0):
    ''' 利用缩进来建立层级关系
    '''
    for i in range(n):
        print ' ',

    if cluster.id < 0:
        # 负数标记代表这是一个分支
        print '-' * 4
    else:
        if labels == None:
            print cluster.id
        else:
            print labels[cluster.id]

    if cluster.left != None:
        print_cluster(cluster.left, labels=labels, n=n+1)

    if cluster.right != None:
        print_cluster(cluster.right, labels=labels, n=n+1)

if __name__ == '__main__':
    rownames,clonames,data = readfile('blog_data.txt')

    cluster = hcluster(data)
    blog_names = rownames
    blog_words = get_blog_words('blog_data.txt')

    print_cluster(cluster, labels=blog_names)
