#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import sys
import xml.dom.minidom

filename1 = r"D:\software\pycharm\语料库\复述文本\1到31\9\巨人传1.txt"
filename2 = r"D:\software\pycharm\语料库\复述文本\1到31\9\巨人传1.txt"
filename3 = r"D:\software\pycharm\语料库\复述文本\1到31\段\9.txt"

#三个段落列表 去空行之类的操作    list1，list2，list3
with open(filename1,'r',encoding='utf-8') as f1:
    txt1 = f1.readlines()
    list1 = []
    for i in txt1:
        i = i.strip()
        if i:
            list1.append(i)
with open(filename2,'r',encoding='utf-8') as f2:
    txt2 = f2.readlines()
    list2 = []
    for i in txt2:
        i = i.strip()
        if i:
            list2.append(i)
with open(filename3,'r',encoding='utf-8') as f3:
    # 段落文本列表，去掉空行
    list3 = []
    txt3 = f3.readlines()[3:]
    for i in txt3:
        i = i.strip()
        if i:
            list3.append(i)

#根据文件路径的结构
filename1_ID = int(re.split(r'\\',os.path.split(filename1)[0])[-1])*2 - 1
filename2_ID = filename1_ID + 1
if list3[0] in list1:
    first_ID = filename1_ID
    second_ID = filename2_ID
elif list3[0] in list2:
    first_ID = filename2_ID
    second_ID = filename1_ID
else:
    sys.exit('又双叒有问题了')
print(first_ID)
print(len(list3)/2)
print(len(list3)/len(list1)/2)

doc = xml.dom.minidom.Document()
root = doc.createElement('Rehearsal-Paragraphs')
#设置根节点的一些属性
root.setAttribute('来源标题','巨人传')
root.setAttribute('来源ID',str(filename1_ID)+' and '+str(filename2_ID))
root.setAttribute('方法','杰卡德距离')
root.setAttribute('处理人员','王也')
root.setAttribute('处理时间','2018/6/21')
root.setAttribute('复述段数量',str(int(len(list3)/2)))
root.setAttribute('复述段比例',str(len(list3)/len(list1)/2))
doc.appendChild(root)  #将根节点添加到文档对象中

if first_ID == filename1_ID:
    for ID in range(0, len(list3) - 1, 2):
        paragraph1 = list3[ID]
        try:
            index1 = list1.index(paragraph1)
        except:
            index1 = -1

        paragraph2 = list3[ID + 1]
        try:
            index2 = list2.index(paragraph2)
        except:
            index2 = -1

        # 设置父节点
        nodePair = doc.createElement('Rehearsal-Paragraph')
        nodePair.setAttribute('Rehearsal-Paragraph_ID', str(int(ID / 2 + 1)))

        # 依次显示文本内容
        nodeParagraph1 = doc.createElement('Paragraph1')
        nodeParagraph1.setAttribute('ID', str(first_ID) + '-' + str(index1 + 1))
        nodeText1 = doc.createElement('Text1')
        nodeText1.appendChild(doc.createTextNode(paragraph1))

        nodeParagraph2 = doc.createElement('Paragraph2')
        nodeParagraph2.setAttribute('ID', str(second_ID) + '-' + str(index2 + 1))
        nodeText2 = doc.createElement('Text2')
        nodeText2.appendChild(doc.createTextNode(paragraph2))

        # 将叶子结点添加到父节点上
        # 最后将父节点添加到根节点上
        nodeParagraph1.appendChild(nodeText1)
        nodeParagraph2.appendChild(nodeText2)
        nodePair.appendChild(nodeParagraph1)
        nodePair.appendChild(nodeParagraph2)
        root.appendChild(nodePair)

if first_ID == filename2_ID:
    for ID in range(0, len(list3) - 1, 2):
        paragraph1 = list3[ID]
        try:
            index1 = list2.index(paragraph1)
        except:
            index1 = -1

        paragraph2 = list3[ID + 1]
        try:
            index2 = list1.index(paragraph2)
        except:
            index2 = -1

        # 设置父节点
        nodePair = doc.createElement('Rehearsal-Paragraph')
        nodePair.setAttribute('Rehearsal-Paragraph_ID', str(int(ID / 2 + 1)))

        # 依次显示文本内容
        nodeParagraph1 = doc.createElement('Paragraph1')
        nodeParagraph1.setAttribute('ID', str(first_ID) + '-' + str(index1 + 1))
        nodeText1 = doc.createElement('Text1')
        nodeText1.appendChild(doc.createTextNode(paragraph1))

        nodeParagraph2 = doc.createElement('Paragraph2')
        nodeParagraph2.setAttribute('ID', str(second_ID) + '-' + str(index2 + 1))
        nodeText2 = doc.createElement('Text2')
        nodeText2.appendChild(doc.createTextNode(paragraph2))

        # 将叶子结点添加到父节点上
        # 最后将父节点添加到根节点上
        nodeParagraph1.appendChild(nodeText1)
        nodeParagraph2.appendChild(nodeText2)
        nodePair.appendChild(nodeParagraph1)
        nodePair.appendChild(nodeParagraph2)
        root.appendChild(nodePair)


#生成xml文件
save_root = r"D:\software\pycharm\语料库\复述文本\1到31\段xml"
xml_name = re.split(r'\\',os.path.split(filename1)[0])[-1] + '.xml'
xml_path = os.path.join(save_root,xml_name)
with open(xml_path,'w',encoding='utf-8') as f:
    doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding='utf-8')

