#!/usr/bin/env python
# -*- conding:utf-8 -*-
from Levenshtein import *
filename1 = 'wulao.txt'
filename2 = 'zhang.txt'

with open(filename1) as txt1:
    contents1 = txt1.read()
with open(filename2) as txt2:
    contents2 = txt2.read()

list1 = list(contents1.strip())
list2 = list(contents2.strip())

a = "".join(list1[0:2000])
b = "".join(list2[0:2000])


def edit(str1, str2):
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    return matrix[len(str1)][len(str2)]

if __name__ == '__main__':
    print(edit(a,b))

