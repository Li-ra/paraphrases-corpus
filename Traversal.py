#!/usr/bin/env python
# -*- conding:utf-8 -*-
import time
import chardet
import os
import codecs
from Levenshtein import *

#最长公共子串
def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    #return s1[p - mmax:p], mmax  # 返回最长子串及其长度
    return  mmax

#根据文件名筛选
def txt_name(t1,t2):
    list1 = list(t1)                  #文件名拆分为单个字符   有点蠢
    list2 = list(t2)
    count = 0
    for i in list1:
        if i in list2:
             count += 1
    if count > 10:
        return True
    else :
        return False

def find_txt(filepath):

    for f in os.walk(filepath):
        txts = f[2]
        print(txts)

    for i in range(len(txts)-1):
        filename1 = filepath + txts[i]   #读取文件1
        with codecs.open(filename1, 'rb') as f1:
            contents1 = f1.read()
            enc1 = chardet.detect(contents1)['encoding']
            if enc1 == 'GB2312':
                enc1 = 'gbk'
        with codecs.open(filename1, 'r', enc1) as f11:
            try:
                txt1 = f11.read()
            except UnicodeDecodeError:
                continue

        for j in range(i+1,len(txts)):                                  #遍历后面的文件
            filename2 = filepath + txts[j]
            if txt_name(txts[i],txts[j]):
                with codecs.open(filename2, 'rb') as f2:
                    contents2 = f2.read()
                    enc2 = chardet.detect(contents2)['encoding']
                    if enc2 == 'GB2312':
                        enc2 = 'gbk'
                with codecs.open(filename2, 'r', enc2) as f22:
                    try:
                        txt2 = f22.read()
                    except UnicodeDecodeError:
                        continue

                a = txt1[0:3000]
                b = txt2[0:3000]

                len1 = distance(a, b)  # 编辑距离

                if len1 < 2800:
                    len2 = find_lcsubstr(a, b)
                    if len2 < 60:
                        print('{}和{}是复述文本'.format(txts[i], txts[j]))
                        break
            else :
                continue
if __name__ == '__main__':
    print(time.ctime())

    find_txt('D:/转成txt/')

    print(time.ctime())