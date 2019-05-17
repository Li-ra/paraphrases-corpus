#!/usr/bin/env python
#-*- conding:utf-8 -*-
import os
import chardet
import codecs
import re
import jieba
import copy

"""
对复述段进行分句
"""
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

def sentencesList(filename):
    txt = []             #复述段落的列表
    with open(filename,encoding='utf-8') as f:
        for line in f:
            if line.strip():
                line = line.replace('……', '。')  # 识别不出六个点的省略号
                line = re.sub(r'["“”]','',line)
                txt.append(line.strip())

    sentences_list = []
    for i in txt[2:]:
        list1 = re.split(r'([。？?！!；：:;])',i)

        flag = 0
        if (list1[-1] != ''):        #末尾没有标点符号 flag=1
            flag = 1
        list1.append("")

        if flag == 1:
            list1 = ["".join(i) for i in zip(list1[0::2], list1[1::2])]           #复述段落的开始两段不要
        else:
            list1 = ["".join(i) for i in zip(list1[0::2], list1[1::2])][:-1]

        sentences_list.append(list1)

    return sentences_list

def writeFinallist(txt_list):                        #txts 是名著的一个列表，遍历访问
    for txt in txt_list:
        sentences_list = sentencesList(os.path.join(source_path,txt))         #[[每个段落的句子]，[每个段落的句子]]
        final_list = []                                   #[句子+\n+句子]
        for i in range(0,len(sentences_list)-1,2):
            list1 = sentences_list[i]
            list2 = sentences_list[i+1]
            if len(list1) == len(list2):
                continue_flag = 1
                for t in range(0,len(list1)):
                    if len(list1[t]) > len(list2[t])*1.5 or len(list2[t]) > len(list1[t])*1.5  :
                        continue_flag = 0
                    if len(list1[t]) < 5 or len(list2[t]) < 5:
                        continue_flag = 0

                if continue_flag:
                    list3 = ['\n'.join(j) for j in zip(list1, list2)]
                    for j in list3:
                        final_list.append(j)

                else:                             #len(list1) ！= len(list2)
                    words_list1 = [jieba.lcut(sentence) for sentence in list1]
                    words_list2 = [jieba.lcut(sentence) for sentence in list2]

                    for m in range(0, len(words_list1)):
                        if len(list1[m]) > 5:
                            max = 0
                            k = 0
                            for n in range(0, len(words_list2)):
                                if len(list2[n]) > 5:
                                    sim = new_similarity(words_list1[m], words_list2[n])
                                    if sim > max:
                                        max = sim
                                        k = n

                            if 0.9 >max> 0.28 and len(list1[m])<len(list2[k])*1.5 and len(list2[k])<len(list1[m])*1.5:
                                final_list.append(list1[m] + '\n' + list2[k])


            else:
                words_list1 = [jieba.lcut(sentence) for sentence in list1]
                words_list2 = [jieba.lcut(sentence) for sentence in list2]

                for m in range(0,len(words_list1)):
                    if len(list1[m]) > 5:
                        max = 0
                        k = 0
                        for n in range(0,len(words_list2)):
                            if len(list2[n]) > 5:
                                sim = new_similarity(words_list1[m],words_list2[n])
                                if sim > max:
                                    max = sim
                                    k = n

                        if 0.9>max>0.28 and len(list1[m])<len(list2[k])*1.5 and len(list2[k])<len(list1[m])*1.5:
                            final_list.append(list1[m]+'\n'+list2[k])

        #写入文件
        new_file = os.path.join(save_path,'句子_'+txt)
        with open(new_file,'w',encoding='utf-8') as f:
            for i in final_list:
                f.write(i + '\n\n')

if __name__ == '__main__':

    source_path = r"D:\software\pycharm\sim\测试"
    save_path = r"D:\software\pycharm\sim\测试存放"
    txt_list = next(os.walk(source_path))[2]     #名著列表

    writeFinallist(txt_list)







