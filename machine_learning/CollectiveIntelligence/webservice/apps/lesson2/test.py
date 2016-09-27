#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

from clusters import *

sys.path.append('..')
from common.similarity import *

def test_get_mid_point():
    rows = [[1, 2, 3, 4], [2, 4, 5, 6], [3, 3, 1, -1]]
    best_match = [0, 1, 2]

    mid_point = get_mid_point(rows, best_match)
    assert mid_point == [2, 3, 3, 3]

def test_get_new_clusters():
    rows = [[1, 2, 3, 4], [2, 4, 5, 6], [3, 3, 1, -1]]
    best_matches = [[0, 1], [0, 2], [1,2]]

    clusteres = get_new_clusters(rows, best_matches)
    assert clusteres == [[1.5, 3, 4, 5], [2, 2.5, 2, 1.5], [2.5, 3.5, 3, 2.5]]

def test_get_closest_mid_point():
    row = [1, 2, 3, 4]
    best_matches = [[3, 1, 1, 1], [2, 3, 2, 2], [1, 2, 3, 4]]

    clusteres = get_closest_mid_point(row, best_matches)

    assert clusteres == 2

if __name__ == '__main__':
    test_get_mid_point()
    test_get_new_clusters()
    test_get_closest_mid_point()



