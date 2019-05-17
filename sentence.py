#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import chardet
import codecs
import jieba
import time
import os
"""
对复述段进行分句
"""
#计算杰卡德距离，参数为两个词语列表
def new_similarity(list1,list2):
    stop_words = ['是', '的', '好', '好的', '了', '吧', '嗯', '呢', ',', '，', '啊', '呀']
    if len(list1) == 0 or len(list2) == 0:
        sim = 0
    else:
        list1_copy = copy.copy(list1)     #浅拷贝
        list2_copy = copy.copy(list2)
        for i in list1_copy:
            if i in stop_words:
                list1.remove(i)
        for j in list2_copy:
            if j in stop_words:
                list2.remove(j)

        sum = set(list1 + list2)
        list11 = set(list1)
        list22 = set(list2)
        print(list1)
        print(list11)
        print(list2)
        print(list22)
        count = 0
        for word in list11:
            if word in list22:
                count += 1

        sim = count / len(sum)
    return sim
def similarity(list1,list2):
    if len(list1) == 0 or len(list2) == 0:
        sim = 0
    else:
        sum = set(list1 + list2)
        list11= set(list1)
        list22= set(list2)
        count = 0
        for word in list11:
            if word in list22:
                count += 1

        sim = count / len(sum)
    return sim

#全文进行分句，保存到列表
def sentences(filename) :
    with codecs.open(filename, 'rb') as f:
        txt = f.read()
        enc = chardet.detect(txt)['encoding']
        if enc == 'GB2312':
            enc = 'gbk'
    with codecs.open(filename, 'r', enc) as f:
        try:
            txt=""
            for line in f:
                # print(line)
                txt += line.strip()
        except UnicodeDecodeError:
            print("打开错误")


    txt = re.sub(r'["“”]', '', txt)
    txt = txt.replace('……','。')      #识别不出六个点的省略号

    # list1 = re.split(r'(。|？|！|……|；|;)\s*', txt)   #第一项为字符串，第二项为标点符号
    list1 = re.split(r'([.。？?！!；;])', txt)
    flag=0
    if(list1[-1]!=''):
        flag=1
    list1.append("")

    if flag==1:
        list1 = ["".join(i) for i in zip(list1[0::2],list1[1::2])]
    else:
        list1 = ["".join(i) for i in zip(list1[0::2], list1[1::2])][:-1]

    return list1


#好找相似的句子,参数为词语的列表的列表
def sim(list1,list2):
    count = 0  # 计数
    match_index = []  # 存放相似句子的索引值
    for sentence1 in list1:
        if len(set(sentence1)) > 8:
            n = list1.index(sentence1)  # 求索引值
            if n < 1000:  # 根据经验值找对应的额附近句子
                max = 0
                j = 0
                for i in range(0, n +1000):  # 第一个文件句子和第二个文件附近100个句子比较
                    if i < len(list2):
                        if len(set(list2[i])) >8:
                            sim = similarity(sentence1, list2[i])
                            if sim > max :
                                max = sim
                                j = i
                if len(set(sentence1)) < 14 or len(set(list2[j])) < 14 :
                    if abs(len(sentence1)-len(list2[j])) < 11 :
                        if 0.35 < max < 1:
                            count += 1
                            match_index.append([n, j])
                else:
                    if abs(len(sentence1) - len(list2[j])) < 11:
                        if 0.25 < max <1:
                            count += 1
                            match_index.append([n, j])

            else:
                max = 0
                j = 0
                for i in range(n - 1000, n + 1000):
                    if i < len(list2) :
                        if len(set(list2[i])) > 8:
                            sim = similarity(sentence1, list2[i])
                            if sim > max:
                                max = sim
                                j = i
                if len(set(sentence1)) < 14 or len(set(list2[j])) < 14:
                    if abs(len(sentence1) - len(list2[j])) < 11:
                        if 0.35 < max < 1:
                            count += 1
                            match_index.append([n, j])
                else:
                    if abs(len(sentence1) - len(list2[j])) < 11:
                        if 0.25 < max < 1:
                            count += 1
                            match_index.append([n, j])

    print('匹配的数量：',count)
    print('匹配的比例：',count/len(list1))
    return match_index

if __name__ == '__main__':
    print(time.ctime())

    filename1 = '物种起源1.txt'
    filename2 = '物种起源3.txt'

    sen_list1 = sentences(filename1)
    sen_list2 = sentences(filename2)

    print(len(sen_list1))
    print(len(sen_list2))

    sen_list1_cut = [jieba.lcut(sentence) for sentence in sen_list1]
    sen_list2_cut = [jieba.lcut(sentence) for sentence in sen_list2]

    index_list = sim(sen_list1_cut, sen_list2_cut)

    with open('句子_' + '物种起源13.txt', 'w', encoding='utf-8') as file:
        for indexes in index_list:
            file.write(sen_list1[indexes[0]].strip() + '\n' + sen_list2[indexes[1]].strip() + '\n\n')

    print(time.ctime())









