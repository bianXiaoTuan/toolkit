#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import sys
import feedparser

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s [url]' % sys.argv[0]
        exit(-1)

    url = sys.argv[1]
    d = feedparser.parse(url)
    entries = d.entries

    wordcounts = {}
    for entry in entries:
        print entry['title']
