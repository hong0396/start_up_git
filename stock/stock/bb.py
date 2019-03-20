# -*- coding: utf-8 -*-

import requests
import traceback
import re
import os
from bs4 import BeautifulSoup


# 获取网页内容
def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


# 获取股票代码列表
def get_stock_list(url):
    # 获取股票列表网页
    html = get_html_text(url)
    # 解析
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有超链接a标签
    a = soup.find_all('a')
    # 提取a标签中的股票代码
    lst = []
    for i in a:
        try:
            href = i.attrs['href']
            # 捕捉股票代码
            lst.append(re.findall(r'[s][hz]\d{6}', href)[0])
        except:
            continue
    return lst


# 获取并写入每只个股的信息
def get_and_write_stock_info(lst):
    desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
    # 获取每只股票的信息
    for i, stock in enumerate(lst):
        try:
            url = STOCK_URL + stock + '.html'
            html = get_html_text(url)
            if html == '':
                continue
            soup = BeautifulSoup(html, 'html.parser')
            stock_info = soup.find('div', attrs={'class': 'stock-bets'})
            info_dict = {}
            # 获取股票名称
            info_dict.update({'股票代码': stock})
            name = stock_info.find_all(attrs={'class': 'bets-name'})[0]
            info_dict.update({'股票名称': name.text.split()[0]})
            # 获取其他股票信息
            key_list = stock_info.find_all('dt')
            value_list = stock_info.find_all('dd')
            if len(key_list) == 0:
                continue
            for k, v in zip(key_list, value_list):
                info_dict[k.text] = v.text
            # 每只个股的信息写入文件
            with open(desktop + '\\' + SAVE_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(str(info_dict) + '\n')
                print("\r当前进度: {:.2f}%".format(i * 100 / len(lst)), end="")
        except:
            continue


# 主函数
if __name__ == '__main__':
    # 东方财富网股票代码链接
    STOCK_LIST_URL = 'http://quote.eastmoney.com/stocklist.html'
    # 百度股票的每只个股的信息
    STOCK_URL = 'https://gupiao.baidu.com/stock/'
    # 保存路径
    SAVE_FILE_PATH = '股票信息.txt'
    # 获取股票代码列表
    stock_list = get_stock_list(STOCK_LIST_URL)
    get_and_write_stock_info(stock_list)

