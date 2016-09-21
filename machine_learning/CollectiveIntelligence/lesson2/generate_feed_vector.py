#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import feedparser
import re

def get_words(sentence):
    '''分词
    '''
    words = re.compile(r'[^A-Z^a-z]').split(sentence)
    return [word.lower() for word in words if word != '']


def get_wordcouts(url):
    '''返回RSS订阅源的标题和包含单词计数情况字典
    '''
    word_counts = {}

    d = feedparser.parse(url)
    entries = d.entries

    if 'title' in d.feed :
        blog_title = d.feed.title
    else :
        blog_title = url

    for entry in entries:
        words = [word.lower() for word in get_words(entry['title']) if word != '']

        for word in words:
            word_counts.setdefault(word, 0)
            word_counts[word] += 1

    return blog_title,word_counts

def build_word_list(word_blog_counts, blog_count, bottom, top):
    '''从word_counts中提取word_list
    '''
    word_list = []
    length = len(word_blog_counts)
    for word,count in word_blog_counts.items():
        frac = float(count) / blog_count

        if bottom <= frac and frac <= top:
            word_list.append(word)

    return word_list

def build_feed_vector(file):
    '''
    '''
    blog_count = 0
    total_word_blog_counts = {}
    total_word_counts = {}

    # 读取RSS源, 生成各博客关键词的wordcounts
    fd = open(file)
    for url in fd.readlines()[0:4]:
        blog_title,word_counts = get_wordcouts(url)
        total_word_counts[blog_title] = word_counts

        # 每个word有多少个blog
        for word,count in word_counts.items():
            total_word_blog_counts.setdefault(word, 0)
            if count > 0:
                total_word_blog_counts[word] += 1

        blog_count += 1

    # 构建word_list
    word_list = build_word_list(total_word_blog_counts, blog_count, 0.4, 0.6)

    # 构建blog 和 word矩阵写入文件blog_data.txt
    out = open('blog_data.txt', 'w')
    out.write('Blog')
    for word in word_list:
        out.write('\t%s' % word)

    out.write('\n')

    for title,word_counts in total_word_counts.items():
        out.write(title)

        for word in word_list:
            if word in word_counts:
                out.write('\t%d' % word_counts[word])
            else:
                out.write('\t%d' % 0)

        out.write('\n')

    out.close()

if __name__ == '__main__':
    build_feed_vector('feedlist')
