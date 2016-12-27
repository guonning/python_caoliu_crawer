# -*-coding:utf-8 -*-

import requests
from logger import Logger
from lxml import etree
import sys
# 引入模块
import os
logger = Logger('collect.py')


def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    page = requests.get('http://www.cao2016ne.com/thread0806.php?fid=2',headers=headers)
    page.encoding = 'GBK'
    page = page.text
    ss = etree.HTML(page)
    list = ss.xpath('//tr[@align="center"]/td[2]/h3/a')
    t = 0
    for i in list:

        title = ''
        for n in i.xpath('text()'):
            title = n
        href = i.xpath('@href')[0]
        if title != '':
            logger.info('抓取帖子:'+title+'，链接为:http://www.cao2016ne.com/'+href)
            mkdir(str(t)+"/img")
            getzz("http://www.cao2016ne.com/"+href, str(t))
            t = t + 1


def getzz(url, title):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page.encoding = 'GBK'
    page = page.text
    ss = etree.HTML(page)
    imglist = ss.xpath('//img[@src]/@src')
    n = 0
    for i in imglist:
        try:
            ir = requests.get(i)
            if ir.status_code == 200:
                open( title+"/img/"+str(n)+'.jpg', 'wb').write(ir.content)
                n = n + 1
        except requests.RequestException as e:
            logger.error(e)


def mkdir(path):

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    path = sys.path[0]+"/"+path
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


if __name__ == '__main__':
    main()