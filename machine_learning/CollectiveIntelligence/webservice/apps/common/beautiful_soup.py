#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

from bs4 import BeautifulSoup

def hello_world():
    ''' BeautifulSoup
    '''
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie/chen/hong" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie/huan/jiang" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie/pang/guai" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """

    soup = BeautifulSoup(html_doc, 'html.parser')
    print soup.prettify()

    # 下面两种方式一样
    print soup.find_all('a')
    links = soup('a')

    for link in links:
        print link.attrs
        print link.string
        print link.contents

if __name__ == '__main__':
    hello_world()