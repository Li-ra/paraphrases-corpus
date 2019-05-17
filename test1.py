#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
import os
import sys







# print('目前系统的编码为：',sys.getdefaultencoding())
# name='小明'
# print(type(name))#首先我们来打印下转码前的name类型，因为它是str，所以可以通过encode来进行编码
# name1=name.encode('utf-8')
# print(type(name1))
# print(name1.decode('utf-8'))
#
# exit_code = os.system('ping www.baidu.com')
#
# if exit_code:
#     raise Exception('connect failed.')
url = "https://wenku.baidu.com/view/e16cdc166c175f0e7cd137ed.html?from=search###"
filename = "D:/abc.jpg"

kv = {"User-Agent":"Mozilla/5.0"}
r= requests.get(url,headers = kv)
r.raise_for_status()
print(r.headers)
print(r.request.headers)
with open(filename,"wb") as f:
     f.write(r.content)
#
#
# url = "http://o.obid.bid/"
# kv = {'key':'老人与海'}
# r= requests.get(url,params = kv)
# print(r.url)
# r.encoding = r.apparent_encoding
# print(r.text)
#
# import requests
# from bs4 import BeautifulSoup
#
# url = 'http://remoted.shuyuzhe.com/?filesize=1,233.49 KB&id=83&url=Y1gxOUtiYUU9bFZUPWUycWtnV3NDTW9WMU9vREVmengxTz1md3VpWjVkZ2duWjJVS00zc3ltQ1M9ZW1hNXhHZC1jNGdT'
# r = requests.get(url,timeout = 30)
# r.raise_for_status()
# r.encoding = r.apparent_encoding
# html = r.text
# soup = BeautifulSoup(html,'html.parser')
# download_tag = soup.find('a')
# download_cache = download_tag.get('href')
#
# base_url = 'http://remoted.shuyuzhe.com'
#
# download_url = base_url + download_cache.lstrip('.')
# filename = download_cache.split('/')[-1]
# try:
#     r = requests.get(download_url,timeout = 30)
#     r.raise_for_status()
#     with open(filename,'wb') as f:
#         f.write(r.content)
# except:
#     print('错误')
#
# a = 'jjjjjj.pdf'
# b = 'kkkkkk.txt'
# if a[-3:]!='txt' and
# if(re.search(r'[txt|pdf]$',a)):
#     print(a)
# a= ""
# if(not a):
#     print(44444444444)
# a = [66.25, 333, 333, 1, 1234.5]
# a.reverse()
# print(sorted(a))
# print(a)
# i = '我是（内容）(括号里的内容)后续'
# print(i)
#
# i = re.sub(r'\(.*\)|\（.*\）','',i)
# print(i)

# path = "D:/software/pycharm/sim1/测试/"
#
# txts = next(os.walk(path))[2]
# print(txts)
#
# path = "D:/software/pycharm/sim1/测试/"
#
# txts=next(os.walk(path))
# os.mkdir(path+'新建')
# flag = os.path.isdir(path+'新建')
#
# print(flag)
# print(os.listdir(path))
# for i in os.walk(path):
#     print(i)


