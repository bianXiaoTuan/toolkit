#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import unittest
from kclusters import *
sys.path.append('..')
from common.similarity import *

class ClusterTest(unittest.TestCase):

    def setUp(self):
        ''' 初始化
        '''
        self.rows = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]]
        self.mid_points = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]]
        self.best_macthes = [[0, 1], [0], [0, 1, 2, 3], [1, 2]]

        self.k = 2

    def tearDown(self):
        ''' 清理
        '''
        pass

    def test_get_point_position_range(self):
        ''' 测试get_point_position_range
        '''
        point_position_range = get_point_position_range(self.rows)
        self.assertEqual(point_position_range, [(1, 4), (2, 5), (3, 6), (4, 7)], 'get_point_position_range fail')

    def test_get_random_mid_points(self):
        ''' 测试get_random_points
        '''
        random_mid_points = get_random_mid_points(self.rows, self.k)
        point_position_range = get_point_position_range(self.rows)

        self.assertEqual(len(random_mid_points), self.k, 'get_random_points fail')

        # 产生的坐标值必须在(min, max)之间
        for mid_point in random_mid_points:
            for i in range(len(mid_point)):
                position = mid_point[i]

                self.assertGreater(position, point_position_range[i][0], 'get_random_points fail')
                self.assertLess(position, point_position_range[i][1], 'get_random_points fail')

    def test_get_closest_mid_point(self):
        ''' 测试get_closest_mid_point
        '''
        closest_indexes = []
        for row in self.rows:
            closest_index = get_closest_mid_point(row, self.mid_points, distance=sim_pearson)
            closest_indexes.append(closest_index)

        self.assertEqual(closest_indexes, [3, 3, 3, 3], 'get_closest_mid_point fail')

    def test_get_mid_point(self):
        ''' 测试get_mid_point
        '''
        mid_point = get_mid_point(self.rows)
        self.assertEqual(mid_point, [2.5, 3.5, 4.5, 5.5], 'get_mid_point fail')

    def test_get_mid_poins(self):
        ''' 测试get_mid_points
        '''
        mid_points = get_mid_points(self.rows, self.best_macthes)

        self.assertEqual(mid_points[0], [1.5, 2.5, 3.5, 4.5], 'get_mid_points fail')
        self.assertEqual(mid_points[1], [1, 2, 3, 4], 'get_mid_points fail')
        self.assertEqual(mid_points[2], [2.5, 3.5, 4.5, 5.5], 'get_mid_points fail')
        self.assertEqual(mid_points[3], [2.5, 3.5, 4.5, 5.5], 'get_mid_points fail')

    def test_get_clusters(self):
        ''' 测试get_clusters
        '''
        clusters = get_clusters(self.rows, self.mid_points, distance=sim_pearson)

        self.assertEqual(clusters, [[], [], [], [0, 1, 2, 3]], 'get_clusters fail')

if __name__ == '__main__':
    unittest.main()
