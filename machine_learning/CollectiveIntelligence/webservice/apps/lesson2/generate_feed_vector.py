#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import re
import feedparser
from multiprocessing import Pool

def get_words(sentence):
    '''分词
    '''
    # 去除HTML标记
    sentence = re.compile(r'<[^>]+>').sub('', sentence)
    # 过滤word
    words = re.compile(r'[^A-Z^a-z]').split(sentence)
    return [word.lower() for word in words if word != '']

def get_wordcouts(url):
    '''返回RSS订阅源的标题和包含单词计数情况字典
    '''
    d = feedparser.parse(url)
    entries = d.entries

    wordcounts = {}
    for entry in entries:
        if 'summary' in entry:
            summary = entry.summary
        else :
            summary = entry.description

        words = get_words(summary)

        for word in words:
            wordcounts.setdefault(word, 0)
            wordcounts[word] += 1

    return wordcounts

def get_wordlist(word_blogcounts, blog_num, exclude_filename, lower_limit, upper_limit):
    '''从word_counts中提取wordlist

    :param word_blogcounts: 出现word的blog数
    :param blog_num: blog数
    :param lower_limit: word出现频率下限
    :param upper_limit: word出现频率上限
    :return: [] 符合上下限单词表
    '''
    wordlist = []
    exclude_words = get_exclude_words(exclude_filename)
    for word,count in word_blogcounts.items():
        if len(word) <= 2:
            continue

        if word in exclude_words:
            continue

        frac = float(count) / blog_num
        if lower_limit <= frac and frac <= upper_limit:
            wordlist.append(word)

    return wordlist

def get_exclude_words(filename):
    ''' 读取filename文件中过滤word
    '''
    fd = open(filename)
    return [word.strip() for word in fd.readlines() if word != '']

def get_urls(feed_list_file, count=3):
    ''' 返回urls列表
    '''
    fd = open(feed_list_file)
    return [url.strip() for url in fd.readlines() if url.strip() != '' and url[0] != '#' ][0:count]

def get_domain(url):
    ''' 解析url返回domain信息
    
    :param url: string http://www.chenhuan0103.com/xxxxx
    :return: www.chenhuan0103.com
    '''
    domain = url.split('/')[2]
    return domain
    
def statics_rss_url(url):
     ''' 统计rss_url中关键词信息

    :param url: string rss url
    :return:
     blog_word_map: {}   # blog的word数
    '''
     print url
     domain = get_domain(url)
     wordcounts = get_wordcouts(url)
     return domain,wordcounts

def get_blog_wordcounts(urls):
    ''' 解析urls内容,返回每篇博客关键词的wordcount统计

    :param urls: []
    :return: {domainname : {word : count}}
    '''
    # 利用多进程方式实现
    pool = Pool(len(urls))
    tmp_blog_word_map = pool.map(statics_rss_url, urls)

    # 过滤掉无关键词blog
    blog_wordcounts = {item[0] : item[1] for item in tmp_blog_word_map if len(item[1]) != 0}

    return blog_wordcounts

def get_word_blogcounts(blog_wordcounts):
    ''' 返回每个word在多少篇blog中出现过

    :param blog_wordcounts: {domainname : {word : count}}
    :return: {word : count}
    '''
    word_blogcounts = {}
    for domain,wordcounts in blog_wordcounts.items():
        for word in wordcounts:
            word_blogcounts.setdefault(word, 0)
            word_blogcounts[word] += 1

    return word_blogcounts

def statics_rss_urls(urls):
    '''统计rss_urls中关键词信息

    :param urls: [] rss url列表
    :return:
     word_blogcounts: {}   # 出现word的blog数
     blog_word_map: {}   # 每篇blog的word数
     blog_num: int       # 博客数
    '''
    # 构建blog_word_map
    blog_wordcounts = get_blog_wordcounts(urls)

    # 构建word_blogcounts
    word_blogcounts = get_word_blogcounts(blog_wordcounts)

    return blog_wordcounts,word_blogcounts

def write_statics_to_file(result_file, blog_word_map, wordlist):
    '''将统计结果矩阵写入文件result_file中
    '''
    out = open(result_file, 'w')

    # 第一行标识单词
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s' % word)

    out.write('\n')

    for domain,wordcounts in blog_word_map.items():
        # 第一列blog名字
        out.write(domain)

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
    url_num = 100
    urls = get_urls(feed_list_file, url_num)

    # 获取博客数量
    blog_num = len(urls)

    # 统计word_blogcounts, blog_word_map
    blog_wordcounts,word_blogcounts = statics_rss_urls(urls)

    # 构建wordlist
    lower_limit = 0.1
    upper_limit = 0.9
    wordlist = get_wordlist(word_blogcounts, blog_num, 'exclude_words.txt', lower_limit, upper_limit)

    # 构建blog 和 word矩阵写入文件blog_data.txt
    write_statics_to_file('blog_data.txt', blog_wordcounts, wordlist)

if __name__ == '__main__':
    get_feed_vector('feedlist')
