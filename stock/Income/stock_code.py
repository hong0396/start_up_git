import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
import tushare as ts


def tu_code():
    all=ts.get_stock_basics()
    #print(all)
    listcode=all.index.tolist()
    print('Stock number is'+len(listcode))
    return listcode
def tu_code_fore():
    all=ts.get_stock_basics()
    #print(all)
    Code_List=[]
    listcode=all.index.tolist() 
    print('Stock number is '+str(len(listcode)))
    for item in listcode:
        if item[0] == '6':
            Code_List.append('sh'+item)
        else:
            Code_List.append('sz'+item)
    return Code_List

# stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
current = time.strftime("%Y%m%d")

# 获取股票代码列表（带前缀）
def urlTolist_fore():
    CodeList=[]
    url = 'http://quote.eastmoney.com/stocklist.html'
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)   
    for item in code:
        if item[2] == '6' or item[2] == '3' or item[2] == '0':
            CodeList.append(item)
    return CodeList

# 获取股票代码列表(不带前缀)

def urlTolist():
    url = 'http://quote.eastmoney.com/stocklist.html'
    allCodeList = []
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    
    for item in code:
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodeList.append(item)
    return allCodeList