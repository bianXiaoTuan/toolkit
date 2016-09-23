#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import re
import feedparser

def get_words(sentence):
    '''分词
    '''
    words = re.compile(r'[^A-Z^a-z]').split(sentence)
    return [word.lower() for word in words if word != '']

def get_wordcouts(url):
    '''返回RSS订阅源的标题和包含单词计数情况字典
    '''
    d = feedparser.parse(url)
    entries = d.entries

    if 'title' in d.feed :
        title = d.feed.title
    else :
        title = url

    wordcounts = {}
    for entry in entries:
        words = get_words(entry['title'])

        for word in words:
            wordcounts.setdefault(word, 0)
            wordcounts[word] += 1

    return title,wordcounts

def get_wordlist(word_blog_map, blog_num, lower_limit, upper_limit):
    '''从word_counts中提取wordlist

    :param word_blog_map: 出现word的blog数
    :param blog_num: blog数
    :param lower_limit: word出现频率下限
    :param upper_limit: word出现频率上限
    :return: [] 符合上下限单词表
    '''
    wordlist = []
    
    length = len(word_blog_map)
    for word,count in word_blog_map.items():
        frac = float(count) / blog_num

        if lower_limit <= frac and frac <= upper_limit:
            wordlist.append(word)

    return wordlist

def get_urls(feed_list_file, count=5):
    '''
    '''
    fd = open(feed_list_file)
    return [url.strip() for url in fd.readlines() if url.strip() != ''][0:count]

def statics_rss_urls(urls):
    '''统计rss_urls中关键词信息

    :param urls: [] rss url列表
    :return:
     word_blog_map: {}   # 出现word的blog数
     blog_word_map: {}   # 每篇blog的word数
     blog_num: int       # 博客数
    '''
    word_blog_map = {}    # 出现word的blog数
    blog_word_map = {}    # 每篇blog的word数
    blog_num = 0          # 博客数

    for url in urls:
        print url + ' begin'

        title,wordcounts = get_wordcouts(url)
        blog_word_map[title] = wordcounts

        # 每个word有多少个blog
        for word,count in wordcounts.items():
            word_blog_map.setdefault(word, 0)
            word_blog_map[word] += 1 if count > 0 else 0

        blog_num += 1

    return word_blog_map,blog_word_map,blog_num

def write_statics_to_file(result_file, blog_word_map, wordlist):
    '''将统计结果矩阵写入文件result_file中
    '''
    out = open(result_file, 'w')

    # 第一行标识单词
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s' % word)

    out.write('\n')

    for title,wordcounts in blog_word_map.items():
        # 第一列blog名字
        out.write(title)

        for word in wordlist:
            if word in wordcounts:
                out.write('\t%d' % wordcounts[word])
            else:
                out.write('\t%d' % 0)

        out.write('\n')
    out.close()

def get_feed_vector(feed_list_file):
    '''生成博客关键词统计
    '''
    # 从文件获取RSS URL
    urls = get_urls(feed_list_file, 1)

    # 统计blog_word_map, word_blog_map 和 blog_num
    blog_word_map,word_blog_map,blog_num = statics_rss_urls(urls)

    # 构建wordlist
    wordlist = get_wordlist(word_blog_map, blog_num, 0.1, 0.5)

    # 构建blog 和 word矩阵写入文件blog_data.txt
    write_statics_to_file('blog_data.txt', blog_word_map, wordlist)

if __name__ == '__main__':
    get_feed_vector('feedlist')
