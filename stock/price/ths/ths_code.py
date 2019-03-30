import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast, os ,re
from functools import reduce
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine
import xarray as xr
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

#获取动态cookies
def get_cookie():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver=webdriver.Chrome(executable_path=chromedriver,chrome_options=options)
    url="http://q.10jqka.com.cn/index" #http://stock.10jqka.com.cn/
    driver.get(url)
    # 获取cookie列表
    cookie=driver.get_cookies()
    driver.close()
    # print(cookie)
    for i in cookie:
        if i.get('name') == 'v':
            cookie_v = i.get('value') 
    return cookie_v
cook=get_cookie()
# print(cook)
header ={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'v='+cook,
'Host': 'q.10jqka.com.cn',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
 }

# con=requests.get(url.format(i+1), headers=header)  p

# soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
# return soup.find('span',"page_info").text.split('/')[1]

url_ss='http://q.10jqka.com.cn/index/index/board/ss/field/zdf/order/desc/page/{}/ajax/1/'
url_hs='http://q.10jqka.com.cn/index/index/board/hs/field/zdf/order/desc/page/{}/ajax/1/'

def get_ths_code(url,i):
    time.sleep(0.5)
    global header
    # url='http://d.10jqka.com.cn/v6/line/hs_600196/21/all.js'
    con=requests.get(url.format(i+1), headers=header)
    soup = BeautifulSoup(con.content.decode('gbk'),'lxml') 
    time.sleep(0.5)
    while (con.status_code != 200) or ( soup.find('tbody') is None  ): 
        time.sleep(0.5)
        cook=get_cookie()
        time.sleep(0.5)
        header ={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'v='+cook,
        'Host': 'q.10jqka.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
         }
        print('------------------停--------------------')
        con=requests.get(url.format(i+1),headers=header)  
        soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
    print('------------------'+str(i)+'--------------------')
    # print(soup)
    li=[]
    
    # yema=soup.find('span',"page_info").text.split('/')[1]
    for i in soup.find('tbody').find_all('tr'):
        lio=[]
        for j in i.find_all('td'):
            lio.append(str(j.text))
        li.append(lio) 
    # print(li)       
    aa=pd.DataFrame(li, columns=['序号','代码' , '名称' , '现价' , '涨跌幅(%)' , '涨跌'  ,'涨速(%)','换手(%)','量比','振幅(%)','成交额','流通股','流通市值','市盈率','加自选'])
    return aa

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
num=71
ss=pd.DataFrame()
hs=pd.DataFrame()
for i in range(23):
    tmp=get_ths_code(url_ss,i)
    if len(ss) == 0:
        ss=tmp.copy()
    else:
        ss=ss.append(tmp,ignore_index=True)     
for i in range(71):
    tmp=get_ths_code(url_hs,i)
    if len(hs) == 0:
        hs=tmp.copy()
    else:
        hs=hs.append(tmp,ignore_index=True)

sum=ss.append(hs,ignore_index=True)
sum.to_csv(date+'_ths_code.csv',  encoding = 'gbk', index=False)
     

# for 
# if df is not None:
#     dic.update({str(code_nm): df })


# ds=xr.Dataset(dic)  
# ds.to_netcdf('E:/stock_data/'+date+'_stock_price_month_saved.nc')


# http://d.10jqka.com.cn/v6/line/hs_000757/21/all.js