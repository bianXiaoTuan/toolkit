#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import csv
from math import sqrt

def build_movie_critics(csv_file):
    '''读取csv文件,构建critics
    userId,movieId,rating,timestamp

    @:param: csv_file string 文件名

    @:return {movie: {
        movie_id : rating
    }}
    '''
    critics = {}
    reader = csv.reader(file(csv_file, 'rU'))
    for line in reader:
        user_id,movie_id,rating,timestamp = line

        critics.setdefault(movie_id, {})
        critics[movie_id][user_id] = float(rating)


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
        return 1

    return element / denominator

def top_matchs(prefs, user, similarity=sim_pearson):
    '''按照similarity相似度计算函数, 返回按user相似度排序map
    '''
    scores = [(similarity(prefs, user, other), other) for other in prefs if other != user]

    scores.sort()
    scores.reverse()
    return scores

def get_recommendations(prefs, user, similarity=sim_pearson):
    '''推荐
    '''
    movie_score_sum = {}
    movie_sim_sum = {}
    for other in prefs:
        if other == user:
            continue

        # 计算相似度
        sim = similarity(prefs, user, other)
        if sim == 0:
            continue

        # 电影打分
        for movie in prefs[other]:
            # 看过电影不推荐
            if movie in prefs[user]:
                continue

            movie_score_sum.setdefault(movie, 0)
            movie_score_sum[movie] += prefs[other][movie] * sim

            movie_sim_sum.setdefault(movie, 0)
            movie_sim_sum[movie] += sim

        rankings = [(score/movie_sim_sum[movie], movie) for movie,score in movie_score_sum.items()]

        rankings.sort()
        rankings.reverse()
        return rankings

if __name__ == '__main__':
    critics = build_user_critics('ml-latest/ratings.csv')
    print get_recommendations(critics, '9797')

