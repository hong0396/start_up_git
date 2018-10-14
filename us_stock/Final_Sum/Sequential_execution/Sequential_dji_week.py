
import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
from functools import reduce
import globalvar

signnn=globalvar.glo_signnn
Authorization= globalvar.glo_Authorization


def todate(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
print(time.time())
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Authorization': Authorization,
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def todate(tim):
    tim=int(tim)/1000
    return time.strftime('%Y-%m-%d',time.localtime(tim))

url='https://hq.itiger.com/stock_info/candle_stick/week/.DJI?beginTime=-1&endTime=-1&right=br&limit=251&deviceId='+signnn+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'

con = requests.get(url, headers=header).json()  
li_data=con.get('items')    
if li_data is not None:
    jo=pd.DataFrame(li_data)
    jo['time']=jo['time'].apply(todate)
    jo['close_pre'] = jo["close"].shift(1)
    jo['week_grow']=(jo["close"]-jo['close_pre'])/jo['close_pre']
    jo['close_pre_month'] = jo["close"].shift(4)
    jo['month_grow']=(jo["close"]-jo['close_pre_month'])/jo['close_pre_month']
    # time=jo['time'].tolist()
    # for i in time:
    #     time.strftime('%Y-%m-%d',time.localtime(time.time()))
    jo.to_csv(date+'_dji_week.csv')


    