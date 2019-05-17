#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os

#将txt全部段落分句 返回句子的列表
def sentencesList(filename):
    txt = []             #复述段落的列表
    with open(filename,encoding='utf-8') as f:
        for line in f:
            if line.strip():
                line = line.replace('……', '。')  # 识别不出六个点的省略号
                line = re.sub(r'["“”]','',line)
                txt.append(line.strip())

    sentences_list = []
    for i in txt:
        list1 = re.split(r'([。？?！!；：:;])',i)

        flag = 0
        if (list1[-1] != ''):        #末尾没有标点符号 flag=1
            flag = 1
        list1.append("")

        if flag == 1:         #末尾无标点
            list1 = ["".join(i) for i in zip(list1[0::2], list1[1::2])]
        else:               #末尾有标点
            list1 = ["".join(i) for i in zip(list1[0::2], list1[1::2])][:-1]

        sentences_list.append(list1)

    return sentences_list

#将字符串切割成句子,返回列表
def cutSentenceList(str):
    str = str.replace('……', '。')
    str = re.sub(r'["“”]','',str)
    str = str.strip()
    list1 = re.split(r'([。？?！!；：:;])', str)

    flag = 0
    if (list1[-1] != ''):  # 末尾没有标点符号 flag=1
        flag = 1
    list1.append("")

    if flag == 1:  # 末尾无标点
        list2 = ["".join(i) for i in zip(list1[0::2], list1[1::2])]
    else:  # 末尾有标点
        list2 = ["".join(i) for i in zip(list1[0::2], list1[1::2])][:-1]

    return list2

#计算列表句子的平均长度,返回长度数字
def sentenceAvgLen(list1):
    all_length = 0
    for sentence in list1:
        all_length += len(sentence)
    avg_len = int(all_length/len(list1))
    return avg_len

if __name__ == '__main__':
    a = ['我知道','哈哈哈哈哈']
    b = sentenceAvgLen(a)
    print(b)