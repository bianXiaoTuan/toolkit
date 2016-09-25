#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

from math import *

def sim_pearson(prefs, person1, person2):
    '''皮尔逊相关系数
    '''
    si = [item for item in prefs[person1] if item in prefs[person2]]

    length = len(si)
    if length == 0:
        return 0

    # 计算所有偏好和
    sum1 = sum([prefs[person1][item] for item in si])
    sum2 = sum([prefs[person2][item] for item in si])

    # 求平方和
    sum1Sq = sum([pow(prefs[person1][item], 2) for item in si])
    sum2Sq = sum([pow(prefs[person2][item], 2) for item in si])

    # 求乘机和
    pSum = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    # 计算皮尔逊评价值
    num = pSum - sum1 * sum2 / length
    den = sqrt((sum1Sq - pow(sum1, 2) / length) * (sum2Sq - pow(sum2, 2) / length))

    if den == 0:
        return 0

    return num / den

def sim_distance(prefs, person1, person2):
    '''欧几里德距离
    '''
    si = [item for item in prefs[person1] if item in prefs[person2]]

    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in si])

    return 1 / (1 + sqrt(sum_of_squares))

def top_matches(prefs, person, similarity=sim_pearson):
    '''按照和person相似度从高到低排序
    '''
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores

def get_recommendations(prefs, person, similarity=sim_pearson):
    '''推荐列表
    '''
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person:
            continue

        # 计算相似度
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total/simSums[item], item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()

    return rankings

if __name__ == '__main__':
    critics = {
        'Lisa Rose' : {
            'Lady in the Water' : 2.5,
            'Snakes on a Plane' : 3.5,
            'Just My Luck' : 3.0,
            'Superman Returns' : 3.5,
            'You, Me and Dupree' : 2.5,
            'The Night Listener' : 3.0
        },
        'Gene Seymour' : {
            'Lady in the Water' : 3.0,
            'Snakes on a Plane' : 3.5,
            'Just My Luck' : 1.5,
            'Superman Returns' : 5.0,
            'You, Me and Dupree' : 3.0,
            'The Night Listener' : 3.5
        },
        'Michael Phillips' : {
            'Lady in the Water' : 2.5,
            'Snakes on a Plane' : 3.0,
            'Superman Returns' : 3.5,
            'The Night Listener' : 4.0
        },
        'Claudia Puig' : {
            'Snakes on a Plane' : 3.0,
            'The Night Listener' : 4.5,
            'Just My Luck' : 3.0,
            'Superman Returns' : 4.0,
            'You, Me and Dupree' : 2.5
        },
        'Mick LaSalle' : {
            'Lady in the Water' : 3.0,
            'Snakes on a Plane' : 4.0,
            'Just My Luck' : 3.0,
            'Superman Returns' : 3.5,
            'You, Me and Dupree' : 2.5,
            'The Night Listener' : 3.0
        },
        'Jack Matthews' : {
            'Lady in the Water' : 3.0,
            'Snakes on a Plane' : 4.0,
            'Just My Luck' : 2.0,
            'Superman Returns' : 3.0,
            'You, Me and Dupree' : 2.0,
            'The Night Listener' : 3.0
        },
        'Toby' : {
            'Snakes on a Plane' : 3.5,
            'Superman Returns' : 4.0,
            'You, Me and Dupree' : 1.0,
        },
        'Chen' : {
            'Lady in the Water' : 3.0,
            'Snakes on a Plane' : 4.0,
            'Just My Luck' : 3.0,
        },
        'Jiang' : {
            'Lady in the Water' : 3.0,
            'Snakes on a Plane' : 4.0,
            'Just My Luck' : 3.0,
            'Superman Returns' : 3.5,
            'You, Me and Dupree' : 2.5,
            'The Night Listener' : 3.0
        },
    }

    print top_matches(critics, 'Chen', sim_distance)
    print top_matches(critics, 'Chen', sim_pearson)

    print get_recommendations(critics, 'Chen', sim_distance)
    print get_recommendations(critics, 'Chen', sim_pearson)

