#!/usr/bin/env python
# -*- conding:utf-8 -*-
#两个字为元素成列表
def cut(str):
    list1 = list(str)
    new = []
    i = 1
    for word in list1:
        if i < len(list1):
            ele = word + list1[i]
            new.append(ele)
            i = i + 1
    #print(new)
    return new

#计算杰卡德距离的函数
def similarity(words1,words2):
    sum = list(set(words1+words2))
    count = 0
    for word in words1:
        if word in words2:
            count += 1

    for word in words2:
        if word in words1:
            count += 1

    sim = (count/len(sum))/2
    return sim

#两篇翻译句子大列表
filename1 = 'sen_wulao.txt'
filename2 = 'sen_zhang.txt'
with open(filename1) as a1:
    list1 = a1.readlines()
with open(filename2) as a2:
    list2 = a2.readlines()

#嵌套列表
list1_cut = [cut(sentence) for sentence in list1]
list2_cut = [cut(sentence) for sentence in list2]

count = 0                                        #计数
match_index = []                                 #存放相似句子的索引值
for words1 in list1_cut:
   if len(words1) > 12 :
        n = list1_cut.index(words1)                  #求索引值
        if n < 50 :                                  #根据经验值找对应的额附近句子
            for i in range(0,n+50):                  #第一个文件句子和第二个文件附近100个句子比较
                if i < len(list2_cut):
                    sim  = similarity(words1,list2_cut[i])
                    if 0.3 < sim < 1:
                        count += 1
                        #print('第{}句和第{}句的相似度为{}'.format(n,i,sim))
                        match_index.append([n,i])

        else:
            for i in range(n-50, n+50):
                if i < len(list2_cut):
                    sim = similarity(words1, list2_cut[i])
                    if 0.3 < sim < 1:
                        count += 1
                        #print('第{}句和第{}句的相似度为{}'.format(n,i,sim))
                        match_index.append([n,i])
#print(count)
#print(count/len(list1))
#print(list1)

#根据索引值将复述句子写入文件
with open('bi_rehearsal_sentences.txt','w') as file :
    file.write("找到复述句子的数量： " + str(count)+'\n')
    file.write("找到复述句子的比例： "+str(count/len(list1))+'\n\n')
    for indexes in match_index :
        file.write(list1[indexes[0]]+list2[indexes[1]]+'\n\n')

