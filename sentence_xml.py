#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import re
import xml.dom.minidom
from functions import cutSentenceList
from functions import sentenceAvgLen

filename1 = r"D:\software\pycharm\语料库\复述文本\42到61\61\汤姆·索亚历险记1.txt"
filename2 = r"D:\software\pycharm\语料库\复述文本\42到61\61\汤姆·索亚历险记2.txt"
filename3 = r"D:\software\pycharm\语料库\复述文本\段落句子\新句子\61.txt"

with open(filename1,'r',encoding='utf-8') as f1:
    sentence_list1 = []
    for line in f1:
        list1 = cutSentenceList((line))
        for i in list1:
            sentence_list1.append(i)

with open(filename2,'r',encoding='utf-8') as f2:
    sentence_list2 = []
    for line in f2:
        list2 = cutSentenceList((line))
        for i in list2:
            sentence_list2.append(i)

with open(filename3,'r',encoding='utf-8') as f3:
    sentence_list3 = []
    for line in f3:
        line = line.replace('……', '。')
        line = re.sub(r'["“”]', '', line)
        line = line.strip()
        if line:
            sentence_list3.append(line)

filename1_ID = int(re.split(r'\\',os.path.split(filename1)[0])[-1])*2 - 1
filename2_ID = filename1_ID + 1
if sentence_list3[0] in sentence_list1:
    first_ID = filename1_ID
    second_ID = filename2_ID
elif sentence_list3[0] in sentence_list2:
    first_ID = filename2_ID
    second_ID = filename1_ID
else:
    sys.exit('又双叒有问题了')

print(first_ID)

#来源的标题
title =re.split(r'\d\.txt|\.txt',os.path.split(filename1)[1])[0]
print(title)
# 复述句的平均长度
average_length = sentenceAvgLen(sentence_list3)

#创建xml文档树
doc = xml.dom.minidom.Document()
root = doc.createElement('Rehearsal-Sentences')
#设置根节点的一些属性
root.setAttribute('来源标题',title)
root.setAttribute('来源ID',str(filename1_ID)+' and '+str(filename2_ID))
root.setAttribute('方法','杰卡德距离')
root.setAttribute('处理人员','王也')
root.setAttribute('处理时间','2018/6/22')
root.setAttribute('复述句数量',str(int(len(sentence_list3)/2)))
root.setAttribute('句子平均长度',str(average_length))
doc.appendChild(root)  #将根节点添加到文档对象中

if first_ID == filename1_ID:
    for ID in range(0, len(sentence_list3) - 1, 2):
        sentence1 = sentence_list3[ID]
        try:
            index1 = sentence_list1.index(sentence1)
        except:
            index1 = -1

        sentence2 = sentence_list3[ID + 1]
        try:
            index2 = sentence_list2.index(sentence2)
        except:
            index2 = -1

        # 设置父节点
        nodePair = doc.createElement('Rehearsal-Sentence')
        nodePair.setAttribute('Rehearsal-Sentence_ID', str(int(ID / 2 + 1)))

        # 依次显示文本内容
        nodeSentence1 = doc.createElement('Sentence1')
        nodeSentence1.setAttribute('ID', str(first_ID) + '-' + str(index1 + 1))
        nodeText1 = doc.createElement('Text1')
        nodeText1.appendChild(doc.createTextNode(sentence1))

        nodeSentence2 = doc.createElement('Sentence2')
        nodeSentence2.setAttribute('ID', str(second_ID) + '-' + str(index2 + 1))
        nodeText2 = doc.createElement('Text2')
        nodeText2.appendChild(doc.createTextNode(sentence2))

        # 将叶子结点添加到父节点上
        # 最后将父节点添加到根节点上
        nodeSentence1.appendChild(nodeText1)
        nodeSentence2.appendChild(nodeText2)
        nodePair.appendChild(nodeSentence1)
        nodePair.appendChild(nodeSentence2)
        root.appendChild(nodePair)

if first_ID == filename2_ID:
    for ID in range(0, len(sentence_list3) - 1, 2):
        sentence1 = sentence_list3[ID]
        try:
            index1 = sentence_list2.index(sentence1)
        except:
            index1 = -1

        sentence2 = sentence_list3[ID + 1]
        try:
            index2 = sentence_list1.index(sentence2)
        except:
            index2 = -1

        # 设置父节点
        nodePair = doc.createElement('Rehearsal-Sentence')
        nodePair.setAttribute('Rehearsal-Sentence_ID', str(int(ID / 2 + 1)))

        # 依次显示文本内容
        nodeSentence1 = doc.createElement('Sentence1')
        nodeSentence1.setAttribute('ID', str(first_ID) + '-' + str(index1 + 1))
        nodeText1 = doc.createElement('Text1')
        nodeText1.appendChild(doc.createTextNode(sentence1))

        nodeSentence2 = doc.createElement('Sentence2')
        nodeSentence2.setAttribute('ID', str(second_ID) + '-' + str(index2 + 1))
        nodeText2 = doc.createElement('Text2')
        nodeText2.appendChild(doc.createTextNode(sentence2))

        # 将叶子结点添加到父节点上
        # 最后将父节点添加到根节点上
        nodeSentence1.appendChild(nodeText1)
        nodeSentence2.appendChild(nodeText2)
        nodePair.appendChild(nodeSentence1)
        nodePair.appendChild(nodeSentence2)
        root.appendChild(nodePair)


#生成xml文件
save_root = r"D:\software\pycharm\语料库\复述文本\1到31\句xml"
xml_name = re.split(r'\\',os.path.split(filename1)[0])[-1] + '.xml'
xml_path = os.path.join(save_root,xml_name)
with open(xml_path,'w',encoding='utf-8') as f:
    doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
