#!/usr/bin/env python
# -*- conding:utf-8 -*-
import re
import codecs
import chardet
import jieba
import time
import os
import copy

#两个词集合的杰卡德距离
def new_similarity(list1,list2):
    stop_words = ['是', '的', '好', '好的', '了', '吧', '嗯', '呢', ',', '，', '啊', '呀','.','。','、','；',';','得']

    list1_copy = copy.copy(list1)     #浅拷贝
    list2_copy = copy.copy(list2)
    for i in list1_copy:
        if i in stop_words:
            list1.remove(i)
    for j in list2_copy:
        if j in stop_words:
            list2.remove(j)

    if len(list1) == 0 or len(list2) == 0:
        sim = 0

    else:
        sum = list1 + list2
        count = 0
        if len(list1) < len(list2) :
            for word in list1:
                if word in list2:
                    count += 1
        else:
            for word in list2 :
                if word in list1:
                    count += 1

        sim = count / len(sum)
    return sim
def similarity(list1,list2):
    sum = set(list1 + list2)
    list11= set(list1)
    list22= set(list2)
    count = 0
    for word in list11:
        if word in list22:
            count += 1
    sim = count / len(sum)
    return sim

#计算相似度并写入文件
def p_sim(paragraph1_cut,paragraph2_cut):
    count = 0         #计数
    match_index = []  # 存放相似段落的索引值
    for paragraph1 in paragraph1_cut:
        if len(set(paragraph1)) > 13:
            n = paragraph1_cut.index(paragraph1)  # 求索引值
            if n < 100:  # 根据经验值找对应的额附近句子
                max = 0
                j = 0
                for i in range(0, n +50):
                    if i<len(paragraph2_cut):           # 第一个文件句子和第二个文件附近200个句子比较
                        if len(set(paragraph2_cut[i])) >13:
                            sim = new_similarity(paragraph1, paragraph2_cut[i])
                            if sim > max :
                                max = sim
                                j = i
                if len(set(paragraph1))<25 or len(set(paragraph2_cut[j]))<25:
                    if 0.30< max < 1:
                        count += 1
                        match_index.append([n, j])             #对应段落的索引记录到列表中，稍后统一写入文件
                else:
                    if 0.22< max <1:
                        count += 1
                        match_index.append([n,j])


            else:                       # 索引值n大于100
                max = 0
                j = 0
                for i in range(n - 100, n + 100):
                    if i < len(paragraph2_cut):
                        if len(set(paragraph2_cut[i])) >13:
                            sim = new_similarity(paragraph1, paragraph2_cut[i])
                            if sim > max:
                                max = sim
                                j = i
                if len(set(paragraph1))<25 or len(set(paragraph2_cut[j]))<25:
                    if 0.30< max < 1:
                        count += 1
                        match_index.append([n, j])             #对应段落的索引记录到列表中，稍后统一写入文件
                else:
                    if 0.22< max < 1:
                        count += 1
                        match_index.append([n,j])
        else:
            continue

    print("段对齐的数量:",count)
    print("对齐段的比例:",count/len(paragraph1_cut))

    with open(new_filename, 'w',encoding='utf-8') as file:
        file.write("复述段落的数量： " + str(count) + '\n')
        file.write("复述段落的比例： " + str(count / len(paragraph1_cut)) + '\n\n')
        for indexes in match_index:
            file.write(txt1[indexes[0]] + txt2[indexes[1]] + '\n')


#读全部段落readlines()，固定的一波代码(不用了)
def fixed_read(filename):
    with codecs.open(filename, 'rb') as f:
        txt = f.read()
        enc = chardet.detect(txt)['encoding']
        if enc == 'GB2312':
            enc = 'gbk'
    with codecs.open(filename, 'r', enc) as f:
        try:
            txt = f.readlines()
            return txt
        except UnicodeDecodeError:
            print("*********************打开错误")

if __name__ == '__main__':
    print(time.ctime())

    root = r"D:\software\pycharm\sim\复述文件"
    dir_list = next(os.walk(root))[1]

    count1 = 1 #新文件名
    for dir in dir_list:
        print(count1)
        path = os.path.join(root,dir)
        txt_list = next(os.walk(path))[2]
        filename1 = os.path.join(path,txt_list[0])
        filename2 = os.path.join(path,txt_list[1])
        new_filename = os.path.join(root,'段落'+str(count1)+'.txt')

        try:
            with open(filename1,'r',encoding='utf-8') as f1:
                txt1 = f1.readlines()
            with open(filename2,'r',encoding='utf-8') as f2:
                txt2 = f2.readlines()

            if len(txt1) < len(txt2):               #短的文件在前
                pass
            else:
                txt1,txt2 = txt2,txt1

            paragraph1_cut = [jieba.lcut(paragraph) for paragraph in txt1]
            paragraph2_cut = [jieba.lcut(paragraph) for paragraph in txt2]

            p_sim(paragraph1_cut, paragraph2_cut)
            count1 += 1
        except Exception as e:
            print(e)
            continue


    print(time.ctime())

# filename1 = '物种起源.txt'
# filename2 = '物种起源3.txt'
#
# txt1 = fixed_read(filename1)
# paragraph1_cut = [jieba.lcut(paragraph) for paragraph in txt1]
# print('第一篇长度',len(paragraph1_cut))
# txt2 = fixed_read(filename2)
# paragraph2_cut = [jieba.lcut(paragraph) for paragraph in txt2]
# print('第二篇长度',len(paragraph2_cut))
#
# p_sim(paragraph1_cut,paragraph2_cut)




