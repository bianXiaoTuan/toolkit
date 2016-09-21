#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import csv
from math import sqrt

def build_movie_id_name_map(csv_file):
    '''构建movie_id 到 movie_name 映射
    '''
    id_name = {}
    reader = csv.reader(file(csv_file, 'rU'))
    for line in reader:
        if len(line) == 1:
            movie_id = line[0].split(',')[0]
            movie_name = line[0].split(',')[1]
        else:
            movie_id = line[0]
            movie_name = line[1]

        id_name.setdefault(movie_id, {})
        id_name[movie_id] = movie_name

    return id_name

def build_movie_critics(csv_file, count=1000):
    '''读取csv文件,构建critics, 读取count行
    userId,movieId,rating,timestamp

    @:param: csv_file string 文件名

    @:return {movie: {
        movie_id : rating
    }}
    '''
    movie_id_name_map = build_movie_id_name_map('ml-latest/movies.csv')

    c = 0
    critics = {}
    reader = csv.reader(file(csv_file, 'rU'))
    for line in reader:
        if c > count:
            break

        user_id,movie_id,rating,timestamp = line

        movie_name = movie_id_name_map[movie_id]
        critics.setdefault(movie_name, {})
        critics[movie_name][user_id] = float(rating)

        # critics.setdefault(movie_id, {})
        # critics[movie_id][user_id] = float(rating)

        c += 1

    return critics

def build_user_critics(csv_file, count=1000):
    '''读取csv文件,构建critics, 读取count行
    userId,movieId,rating,timestamp

    @:param: csv_file string 文件名

    @:return {user_id: {
        movie_id : rating
    }}
    '''
    # 获取
    movie_id_name_map = build_movie_id_name_map('ml-latest/movies.csv')

    c = 0
    critics = {}
    reader = csv.reader(file(csv_file, 'rU'))
    for line in reader:
        if c > count:
            break

        user_id,movie_id,rating,timestamp = line

        critics.setdefault(user_id, {})
        critics[user_id][movie_id_name_map[movie_id]] = float(rating)

        c += 1

    return critics

def sim_distance(prefs, item1, item2):
    '''根据欧几里得距离返回两个人相似系数
       0~1 数字越大越相近
    '''
    items = [item for item in prefs[item1] if item in prefs[item2]]

    # 没有任何交集
    if len(items) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[item1][item] - prefs[item2][item], 2) for item in items])
    return 1 / (1 + sum_of_squares)

def sim_pearson(prefs, item1, item2):
    '''根据皮尔逊相关系数返回两个人相似系数
        0~1 数字越大越相近
    '''
    items = [item for item in prefs[item1] if item in prefs[item2]]

    # 没有任何交集
    n = len(items)
    if n == 0:
        return 0

    item1_dict = prefs[item1]
    item2_dict = prefs[item2]

    sumXY = sum([item1_dict[item] * item2_dict[item] for item in items])

    sumX = sum([item1_dict[item] for item in items])
    sumY = sum([item2_dict[item] for item in items])

    sumX2 = sum([pow(item1_dict[item], 2) for item in items])
    sumY2 = sum([pow(item2_dict[item], 2) for item in items])

    element = n * sumXY - sumX * sumY
    denominator = sqrt((n * sumX2 - pow(sumX, 2)) * (n * sumY2 - pow(sumY, 2)))

    if denominator == 0:
        return 1

    return element / denominator

def matchs(prefs, key, similarity=sim_pearson):
    '''返回和key相似的item列表
    '''
    scores = []
    for other in prefs:
        if other != key:
            sim = similarity(prefs, key, other)
            if sim == 0:
                continue
            scores.append((sim, other))

    scores.sort()
    scores.reverse()
    return scores

def get_recommendations(prefs, key, similarity=sim_pearson):
    '''key=user 则推荐电影; key=movie 则推荐影评人
    '''
    score_sum = {}
    sim_sum = {}
    for other in prefs:
        if other == key:
            continue

        # 计算相似度
        sim = similarity(prefs, key, other)
        if sim == 0:
            continue

        for item in prefs[other]:
            if item in prefs[key]:
                continue

            score_sum.setdefault(item, 0)
            score_sum[item] += prefs[other][item] * sim

            sim_sum.setdefault(item, 0)
            sim_sum[item] += sim

        rankings = [(score/sim_sum[item], item) for item,score in score_sum.items()]

        rankings.sort()
        rankings.reverse()
        return rankings

def build_similar_item_map(prefs):
    '''构建一个item相似度数据集, 返回count个结果
    '''
    result = {}

    for item in prefs:
            top_match = matchs(prefs, item)[0:10]
            result[item] = top_match

    return result

def get_recommendations_by_similar_item(user_prefs, movie_prefs, user):
    '''根据物品相似来进行推荐
    '''
    user_ratings = user_prefs[user]
    similar_item_map = build_similar_item_map(movie_prefs)

    score_sum = {}
    sim_sum = {}

    for item,score in user_ratings.items():
        for sim_score,sim_item in similar_item_map[item]:

            if sim_item in user_ratings:
                continue

            score_sum.setdefault(sim_item, 0)
            # user对item的评分 * sim_item和item的相似度
            score_sum[sim_item] += score * sim_score

            sim_sum.setdefault(sim_item, 0)
            sim_sum[sim_item] += sim_score

    rankings = [(score_sum[item]/sim_sum[item], item) for item in score_sum]

    rankings.sort()
    rankings.reverse()

    return rankings

if __name__ == '__main__':
    user_critics = build_user_critics('ml-latest/ratings.csv', 1000)
    movie_critics = build_movie_critics('ml-latest/ratings.csv', 1000)

    print get_recommendations_by_similar_item(user_critics, movie_critics, '1')
    print get_recommendations_by_similar_item(user_critics, movie_critics, '2')
    print get_recommendations_by_similar_item(user_critics, movie_critics, '3')
    print get_recommendations_by_similar_item(user_critics, movie_critics, '4')
