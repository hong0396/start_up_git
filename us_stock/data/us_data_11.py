import numpy as np
import urllib.request
import re
import random
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.optimize import minimize, bracket, minimize_scalar
from matplotlib.pylab import date2num
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick_ohlc
import gc 
import xarray as xr
import ip_te

ip_factory=ip_te.ip_get_test_save(1.5,1)
requests.packages.urllib3.disable_warnings()


def getmin(fun,xa,xb):
    res1 = bracket(fun, xa = xa, xb=xb)
    res = minimize_scalar(fun,  bounds=(res1[2],res1[1]),  method='bounded')
    return res.x


def todate(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
# print(time.time())
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
my_headers = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']
header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Authorization': 'Bearer Vxe2C7g0gtyh2bLvjVTdkqIyuqhtLG',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
"User-Agent":random.choice(my_headers) }


code=pd.read_csv('2019-03-03us_all_code.csv',encoding='gbk')              
li_code=code['code'].tolist()
# li_code=li_code[:50]



url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=1251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=1251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_month='https://hq.itiger.com/stock_info/candle_stick/month/{}?beginTime=-1&endTime=-1&right=br&limit=1251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'

li=[]
dic={}
useful_proxies = {}
max_failure_times = 3
try:
# 获取代理IP数据
    for ip in list(ip_factory):
        useful_proxies[ip] = 0
    print ("总共：" + str(len(useful_proxies)) + 'IP可用')
except OSError:
    print ("获取代理ip时出错！") 
nu_nu=0
for code_nm in li_code:
    print('------------------------从第'+str(nu_nu)+'只股票提取------------------------------------')
    proxy = random.choice(list(useful_proxies.keys()))
    print ("change proxies: " + proxy)
    content = ''
    
    try:
        con = requests.get(url_week.format(str(code_nm)),proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()
        time.sleep(0.1)
    except OSError:
        # 超过3次则删除此proxy
        useful_proxies[proxy] += 1
        if useful_proxies[proxy] > 3:
            del useful_proxies[proxy]
        # 再抓一次
        proxy = random.choice(list(useful_proxies.keys()))
        # print('shengxia'+proxy)


        con = requests.get(url_month.format(str(code_nm)),proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()
        # print(con)






    # con = requests.get(url_day.format(str(code_nm)), headers=header, verify=False ).json()
    # time.sleep(0.1) 
    li_data=con.get('items')
    if li_data is not None:
        jo=pd.DataFrame(li_data)
        dic.update({str(code_nm): jo })
    nu_nu=nu_nu+1


ds=xr.Dataset(dic)  
ds.to_netcdf('E:/us_data/'+date+'us_stock_month_saved.nc')



# ds_disk =xr.open_dataset('saved_on_disk.nc')


