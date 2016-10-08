#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

def run():
    list = {
        71.5: 3,
        46.0: 1,
        35.0: 7,
        32.6: 7,
        17.5: 6,
        13.2: 63
    }



    for value,num in list.items():
        print '%f, %f' % (value,num)

if __name__ == '__main__':
    run()

