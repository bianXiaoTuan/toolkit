#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

import unittest
from similarity import *

class SimilarityTest(unittest.TestCase):

    def setUp(self):
        ''' 初始化
        '''
        pass

    def tearDown(self):
        ''' 清理
        '''
        pass

    def test_sim_pearson(self):
        ''' 测试sim_pearson
        '''
        vec1s = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
        vec2s = [[0, 1, 2, 3], [0, 1, 2, 4], [0, 1, 2, 4.1], [0, 1, 2, 5]]

        sims = []
        length = len(vec1s)
        for i in range(length):
            sims.append(sim_pearson(vec1s[i], vec2s[i]))

        self.assertLess(sims[0], sims[1])
        self.assertLess(sims[1], sims[2])
        self.assertLess(sims[2], sims[3])
        self.assertEqual(round(sims[3], 3), 0.044)

if __name__ == '__main__':
    unittest.main()
