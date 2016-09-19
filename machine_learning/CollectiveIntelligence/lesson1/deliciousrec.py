#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

from pydelicious import get_popular,get_userposts,get_urlposts

def initializeUserDict(tag, count=2):
    user_dict = {}

    for p1 in get_popular(tag=tag)[0:count]:
        print p1
        for p2 in get_urlposts(p1['href']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict

if __name__ == '__main__':
    print initializeUserDict('programming');
