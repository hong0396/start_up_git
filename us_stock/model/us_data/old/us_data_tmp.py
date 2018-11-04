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
header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Authorization': 'Bearer Z89Q8bh5q4WSrYeLQhOUF2cyLHv7k3',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


code=pd.read_csv('2018-10-13us_all_code.csv',encoding='gbk')              
li_code=code['code'].tolist()
# li_code=li_code[:50]



url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=1251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=1251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'

li=[]
dic={}

nu_nu=0
for code_nm in li_code:
    print('------------------------从第'+str(nu_nu)+'只股票提取------------------------------------')
    con = requests.get(url_day.format(str(code_nm)), headers=header,verify=False).json()
    time.sleep(0.1) 
    li_data=con.get('items')
    if li_data is not None:
        jo=pd.DataFrame(li_data)
        dic.update({str(code_nm): jo })
    nu_nu=nu_nu+1


ds=xr.Dataset(dic)  
ds.to_netcdf('E:/'+date+'us_stock_day_saved.nc')



# ds_disk =xr.open_dataset('saved_on_disk.nc')


