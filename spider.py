#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import time

"""获取一本书的所有版本HTML信息"""
def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except :
        return ""

"""将每个版本书的下载页面链接统一放在列表中"""
def fillLinksList(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('a')[4:]         # 每一个 a 标签的列表

    links = []                            # 每一本书的下载页面链接
    for i in tags:
        links.append(i.get('href'))

    return links

"""下载文件"""
def download(linkslist):
    global count            #修改全局变量来计数
    for link in linkslist:
        try:
            r = requests.get(link)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text

            soup = BeautifulSoup(html, 'html.parser')
            download_tag = soup.find('a')         #分析HTML，只有第一个a标签中有下载链接的缓存部分
            download_cache = download_tag.get('href')   #类似 ./download_cache/83-e8dcc1c14e3cb9c069e702b534d12383.azw3

            prefix_url = 'http://remoted.shuyuzhe.com'     #下载链接的前缀

            """下载链接的形式为 http://remoted.shuyuzhe.com/download_cache/83-e8dcc1c14e3cb9c069e702b534d12383.azw3"""
            if (re.search(r'[azw3|mobi|epub]$', download_cache)):
                download_url = prefix_url + download_cache.lstrip('.')
                filename = download_cache.split('/')[-1]

                r = requests.get(download_url, timeout=30)
                r.raise_for_status()

                with open('D:/software/pycharm/爬虫/爬取电子书/'+filename, 'wb') as f:
                    f.write(r.content)

                print("下载了{}本书，正在爬取中………………".format(count))
                count += 1
            else:
                continue
        except:
            continue



if __name__ == '__main__':
    print('起始时间: ',time.ctime())

    base_url = 'http://o.obid.bid/?key='

    name_list = []
    with open('新名著汇总.txt','r',encoding='utf-8') as f:
        for line in f:
            name_list.append(line.strip())                 #所有名著列表

    count = 1  # 计数下载的数量
    for name in name_list:
        try:
            url = base_url + name
            html = getHtmlText(url)
            linkslist = fillLinksList(html)
            download(linkslist)
        except:
            continue

    print('结束时间: ',time.ctime())
