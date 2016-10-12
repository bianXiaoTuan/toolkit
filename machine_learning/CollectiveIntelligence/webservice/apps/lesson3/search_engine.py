#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import sys
import sqlite3

sys.path.append('..')
from common.common import *

class SearchEngine:
    ''' 搜索引擎
    '''
    def __init__(self, db_name):
        ''' 初始化
        '''
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        ''' 清除
        '''
        self.conn.close()

    def get_cursor(self):
        ''' 返回数据库cursor
        '''
        return self.cursor

    def get_value_by_id(self, table, field, id):
        ''' 通过rowid获取field的值
        '''
        sql = "SELECT %s FROM %s WHERE rowid = %d" % (field, table, id)
        value = self.cursor.execute(sql).fetchone()[0]
        return value

    def get_values_by_ids(self, table, field, ids):
        ''' 获取ids 对应的 values

        :param rowids: [1, 2, 3]
        :return: ['chenhuan', 'huan']
        '''
        values = [self.get_value_by_id(table, field, id) for id in ids]
        return values

    def get_urls_by_word_id(self, word_id):
        ''' 返回满足匹配word的url列表

        :param word_id: 1
        :return: ['http://xxx', 'http://xxx']
        '''
        # 获取word_id对应url_ids
        sql = "SELECT DISTINCT url_id FROM word_location WHERE word_id = %d" % word_id
        url_ids = self.cursor.execute(sql).fetchall()
        url_ids = [url_id[0] for url_id in url_ids]

        # 获取url_ids对应的url
        urls = self.get_values_by_ids('url_list', 'url', url_ids)

        return urls

    def get_id_by_value(self, table, field, value):
        ''' 通过field == value 查询rowid

        :return int
        '''
        sql = "SELECT rowid FROM %s WHERE %s = '%s'" % (table, field, value)
        id = self.cursor.execute(sql).fetchone()[0]
        return id

    def get_ids_by_values(self, table, field, values):
        ''' 通过values获取value对应id

        :param values: ['chen', 'huan']
        :return: [1, 2]
        '''
        rowids = [self.get_id_by_value(table, field, value) for value in values]
        return rowids

    def get_urls_by_word_ids(self, word_ids):
        ''' 返回满足匹配所有words的url列表

        :param word_ids: [1, 2, 3, 4, 5]
        :return: ['http://xxx', 'http://xxx']
        '''
        each_match_urls = [self.get_urls_by_word_id(word_id) for word_id in word_ids]

        # 取所有match_urls的并集
        distinct_match_urls = each_match_urls[0]
        for match_urls in each_match_urls[1:]:
            distinct_match_urls = set(distinct_match_urls).intersection(set(match_urls))

        return list(distinct_match_urls)

    def get_match_urls(self, words):
        ''' 查询和全部words都关联的urls

        :param words: string e.g. 'programming java'
        :return ['http://xxx', 'http://xxxx']
        '''
        # 获取words的word_ids
        words = words.split(' ')
        word_ids = self.get_ids_by_values('word_list', 'word', words)

        # 获取和word关联的全部urls
        match_urls = self.get_urls_by_word_ids(word_ids)

        return match_urls

    def get_score_by_words_frequency(self, url, word_ids):
        ''' 获取根据word_ids匹配出url的评分

        :param url: String e.g. http://xxxx
        :param word_ids:  [] e.g. [1, 2, 3]
        :return: double 0.1112
        '''
        url_id = self.get_id_by_value('url_list', 'url', url)

        where_condition = []
        for word_id in word_ids:
            where_condition.append('word_id=%d' % word_id)
        where_condition = ' or '.join(where_condition)

        sql = "SELECT COUNT(rowid) FROM word_location WHERE url_id = %d AND (%s)" % (url_id, where_condition)
        frequency = self.cursor.execute(sql).fetchone()[0]
        return frequency

    def get_scored_urls_by_word_ids(self, word_ids):
        ''' 查询和全部word_ids都关联的urls, 并按照一定的算法进行排序
        '''
        # 获取和word关联的全部urls
        match_urls = self.get_urls_by_word_ids(word_ids)

        return [(self.get_score_by_words_frequency(url, word_ids), url) for url in match_urls]

    def normalize_scores(self, url_counts, small_is_better=True):
        ''' 归一化处理

        value - min / max - min

        :param url_counts: { url : word出现次数 }
        :param small_is_better: True = 数字越小, 表示评分越高
        :return:
        '''
        min_v = min(url_counts.values())
        max_v = max(url_counts.values())

        # 如果所有count都一样
        if min_v == max_v:
            if small_is_better:
                return dict([(url, 0) for url,count in url_counts.items()])
            else:
                return dict([(url, 1) for url,count in url_counts.items()])

        if small_is_better:
            return dict([(url, 1 - float(count - min_v) / float(max_v - min_v)) for url,count in url_counts.items()])
        else:
            return dict([(url, float(count - min_v) / float(max_v - min_v)) for url,count in url_counts.items()])

    def get_match_urls_and_word_locations(self, words):
        ''' 查询和全部words都关联的urls, 并返回words在url中出现位置

        :param words: [] e.g. ['kafka', 'java', 'storm']
        :return: [(url_id, word1_location, word2_location)]
        '''
        # 获取words的word_ids
        word_ids = self.get_ids_by_values('word_list', 'word', words)

        '''
        构建SQL:
        SELECT w0.url_id,w0.location,w1.location
        FROM word_location w0, word_location w1
        WHERE w0.url_id = w1.url_id AND w0.word_id = 10 AND w1.word_id = 17 ;
        '''
        # w0.url_id,w0.location,w1.location
        s1 = ','.join(['w0.url_id'] + ['w%d.location' % i for i in range(len(word_ids))])

        # word_location w0, word_location w1
        s2 = ','.join(['word_location w%d' % i for i in range(len(word_ids))])

        # w0.url_id = w1.url_id AND w1.url_id = w2.url_id
        s3 = ' AND '.join(['w%d.url_id = w%d.url_id' % (i, i+1) for i in range(len(word_ids) - 1)])

        # w0.word_id = 10 AND w1.word_id = 17
        s4 = ' AND '.join(['w%d.word_id = %d' % (i, word_ids[i]) for i in range(len(word_ids))])

        if len(word_ids) == 1:
            sql = "SELECT %s FROM %s WHERE %s" % (s1, s2, s4)
        else:
            sql = "SELECT %s FROM %s WHERE %s AND %s" % (s1, s2, s3, s4)

        return self.cursor.execute(sql).fetchall()

    def distance_score(self, urls_and_word_locations):
        ''' 按照words之间距离进行评分

        :param urls_and_word_locations: [(url_id, word1_location, word2_location)]
        :return: {url: 评分}
        '''
        if len(urls_and_word_locations[0]) <= 2:
            return dict([(row[0], 1.0) for row in urls_and_word_locations])

        MAX = 1000000
        url_min_distance = dict([(row[0], MAX) for row in urls_and_word_locations])

        for row in urls_and_word_locations:
            url = row[0]
            distance = sum([abs(row[i] - row[i-1]) for i in range(2, len(row))])

            if distance < url_min_distance[url]:
                url_min_distance[url] = distance

        print url_min_distance

        return self.normalize_scores(url_min_distance, small_is_better=True)

    def location_score(self, urls_and_word_locations):
        ''' 按照words在HTML出现的位置进行评分

        :param urls_and_word_locations: [(url_id, word1_location, word2_location)]
        :return: {url: 评分}
        '''
        MAX = 1000000
        url_location_sum = dict([(row[0], MAX) for row in urls_and_word_locations])

        # location之和为所有word_location中最小的
        for row in urls_and_word_locations:
            url = row[0]

            location_sum = sum(row[1:])
            if location_sum < url_location_sum[url]:
                url_location_sum[url] = location_sum

        return self.normalize_scores(url_location_sum, small_is_better=False)

    def frequency_score(self, urls_and_word_locations):
        ''' 按照words出现的频率进行评分

        :param urls_and_word_locations: [(url_id, word1_location, word2_location)]
        :return: { url: 评分}
        '''
        url_counts = dict([(row[0], 0) for row in urls_and_word_locations])

        # url = row[0], 每出现一次word匹配则记一次数
        for row in urls_and_word_locations:
            url_counts[row[0]] += 1

        return self.normalize_scores(url_counts, small_is_better=False)

    def get_scored_urls(self, words):
        ''' 查询和全部words都关联的urls, 并按照算法进行排序

        :param words: String e.g. 'kafka java storm'
        :return:
        '''
        # 获取和words匹配的urls, 及words在url中位置
        urls_and_word_locations = self.get_match_urls_and_word_locations(words)

        # {'url':'评分'}
        scored_urls = dict([(url[0], 0) for url in urls_and_word_locations])

        ''' 评价函数 '''

        # 根据词频推荐
        # weights = [(1.0, self.frequency_score(urls_and_word_locations))]

        # 根据在文档中位置推荐
        # weights = [(1.0, self.location_score(urls_and_word_locations))]

        # 根据单词距离推荐
        weights = [(1.0, self.distance_score(urls_and_word_locations))]

        # 评价函数按照加权打分
        for (weight, scores) in weights:
            for url in scored_urls:
                scored_urls[url] += weight * scores[url]

        return scored_urls

    def query(self, words):
        ''' 完成检索

        :param words: [] e.g. ['kafka', 'java', 'storm']
        '''
        scored_urls = self.get_scored_urls(words)

        # 调整url 和 score位置并排序
        ranked_scored_urls = sorted([(score, url) for (url, score) in scored_urls.items()], reverse=1)

        # 打印结果
        for (score, url_id) in ranked_scored_urls:
            print '%f\t%s' % (score, self.get_value_by_id('url_list', 'url', url_id))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage %s [word] [word] ...' % sys.argv[0]
        exit(-1)

    words = [word.lower() for word in sys.argv[1:]]

    seacher = SearchEngine('database.sqlite')
    seacher.query(words)
