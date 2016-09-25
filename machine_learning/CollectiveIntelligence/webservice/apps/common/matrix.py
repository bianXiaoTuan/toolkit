#!/usr/bin/env python
#_*_ encoding=utf-8 _*_

def rotate_matrix(data):
    '''矩阵转置
    '''
    new_data = []
    for i in range(len(data[0])):
        new_row = [data[j][i] for j in range(len(data))]
        new_data.append(new_row)
    return new_data

if __name__ == '__main__':
    data = [
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5]
    ]

    print rotate_matrix(data)
