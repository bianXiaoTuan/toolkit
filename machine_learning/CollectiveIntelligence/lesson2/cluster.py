#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

def readfile(file):
    fd = open(file)
    lines = [line for line in fd.readlines()]

    clonames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []

    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])

    return rownames,clonames,data

if __name__ == '__main__':
    rownames,clonames,data = readfile('blog_data.txt')

    print rownames
    print clonames
    print data


