#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import xml.dom.minidom
from functions import cutSentenceList

doc = xml.dom.minidom.Document()     #生成xml内存对象

root = doc.createElement('txt')

root.setAttribute('txt_ID','122')
root.setAttribute('source', 'https://book.shuyuzhe.com/')
root.setAttribute('title', '汤姆·索亚历险记 ')
root.setAttribute('author', '马克·吐温 ')

doc.appendChild(root)    #将根节点添加到文档对象中


with open(r"D:\software\pycharm\语料库\复述文本\TXT\61\汤姆·索亚历险记2.txt", 'r', encoding='utf-8') as f:
    Paragraph_ID = 1       #段落ID
    Sentence_ID = 1

    for paragraph in f:
        cut_sentence_list = cutSentenceList(paragraph)                     #句子列表

        nodeParagraph = doc.createElement('Paragraph')                     #段落父节点
        nodeParagraph.setAttribute('Paragraph_ID',str(Paragraph_ID))          #id属性
        Paragraph_ID += 1

        for sentence in cut_sentence_list:
            nodeSentence = doc.createElement('Sentence')                        #段落内容叶子节点
            nodeSentence.setAttribute('Sentence_ID',str(Sentence_ID))
            Sentence_ID += 1

            nodeText = doc.createElement('Text')
            nodeText.appendChild(doc.createTextNode(sentence.strip()))                 #添加句子内容

            nodeSentence.appendChild(nodeText)
            nodeParagraph.appendChild(nodeSentence)             #将叶子结点添加到段落父节点

        root.appendChild(nodeParagraph)



with open(r"D:\software\pycharm\语料库\复述文本\TXT\122.xml", 'w', encoding='utf-8') as f1:
    doc.writexml(f1,indent='\t', addindent='\t', newl='\n',encoding='utf-8')





