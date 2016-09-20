#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import csv
import json
from math import sqrt

def build_movie_critics(csv_file, max_count=10000):
    '''读取csv文件,构建critics
    userId,movieId,rating,timestamp

    @:param: csv_file string 文件名

    @:return {movie: {
        movie_id : rating
    }}
    '''
    critics = {}
    reader = csv.reader(file(csv_file, 'rU'))

    count = 0
    for line in reader:
        if count >= max_count:
            break

        user_id,movie_id,rating,timestamp = line

        critics.setdefault(movie_id, {})
        critics[movie_id][user_id] = float(rating)

        count = count + 1

    return critics

def build_user_critics(csv_file):
    '''读取csv文件,构建critics
    userId,movieId,rating,timestamp

    @:param: csv_file string 文件名

    @:return {user_id: {
        movie_id : rating
    }}
    '''
    critics = {}
    reader = csv.reader(file(csv_file, 'rU'))
    for line in reader:
        user_id,movie_id,rating,timestamp = line

        critics.setdefault(user_id, {})
        critics[user_id][movie_id] = float(rating)

    return critics

def sim_distance(prefs, user1, user2):
    '''根据欧几里得距离返回两个人相似系数
       0~1 数字越大越相近
    '''
    items = [item for item in prefs[user1] if item in prefs[user2]]

    # 没有任何交集
    if len(items) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[user1][item] - prefs[user2][item], 2) for item in items])
    return 1 / (1 + sum_of_squares)

def sim_pearson(prefs, user1, user2):
    '''根据皮尔逊相关系数返回两个人相似系数
        0~1 数字越大越相近
    '''
    items = [item for item in prefs[user1] if item in prefs[user2]]

    # 没有任何交集
    n = len(items)
    if n == 0:
        return 0

    user1_dict = prefs[user1]
    user2_dict = prefs[user2]

    sumXY = sum([user1_dict[item] * user2_dict[item] for item in items])

    sumX = sum([user1_dict[item] for item in items])
    sumY = sum([user2_dict[item] for item in items])

    sumX2 = sum([pow(user1_dict[item], 2) for item in items])
    sumY2 = sum([pow(user2_dict[item], 2) for item in items])

    element = n * sumXY - sumX * sumY
    denominator = sqrt((n * sumX2 - pow(sumX, 2)) * (n * sumY2 - pow(sumY, 2)))

    if denominator == 0:
        return 0

    return element / denominator


# def sim_pearson(prefs, person1, person2):
#     '''皮尔逊相关系数
#     '''
#     si = [item for item in prefs[person1] if item in prefs[person2]]
#
#     length = len(si)
#     if length == 0:
#         return 0
#
#     # 计算所有偏好和
#     sum1 = sum([prefs[person1][item] for item in si])
#     sum2 = sum([prefs[person2][item] for item in si])
#
#     # 求平方和
#     sum1Sq = sum([pow(prefs[person1][item], 2) for item in si])
#     sum2Sq = sum([pow(prefs[person2][item], 2) for item in si])
#
#     # 求乘机和
#     pSum = sum([prefs[person1][item] * prefs[person2][item] for item in si])
#
#     # 计算皮尔逊评价值
#     num = pSum - sum1 * sum2 / length
#     den = sqrt((sum1Sq - pow(sum1, 2) / length) * (sum2Sq - pow(sum2, 2) / length))
#
#     if den == 0:
#         return 0
#
#     return num / den


def top_matchs(prefs, user, similarity=sim_pearson):
    '''按照similarity相似度计算函数, 返回按user相似度排序map
    '''
    scores = [(similarity(prefs, user, other), other) for other in prefs if other != user]

    scores.sort()
    scores.reverse()

    return scores

if __name__ == '__main__':
    critics = build_user_critics('ml-latest/ratings.csv')

    print sim_pearson(critics, '9944', '9943')

    print top_matchs(critics, '9944')

