#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

def min_max_normalize(x, min, max, small_is_better=True):
    ''' Mix_Max归一化
    '''
    if x < min or x > max:
        raise Exception('x must between [min, max]')

    if min == max:
        return 0.0 if small_is_better else 1.0

    if small_is_better:
        return 1.0 - (float)(x - min) / (float)(max - min)
    else:
        return (float)(x - min) / (float)(max - min)

if __name__ == '__main__':
    print min_max_normalize(9, 1, 10, small_is_better=True)
    print min_max_normalize(9, 1, 10, small_is_better=False)
