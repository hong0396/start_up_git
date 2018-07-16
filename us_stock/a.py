import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import tushare as ts
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# https://hq1.itiger.com/fundamental/usstock/earnings/cash/WFC?type=cash&symbol=WFC&deviceId=1531581656218&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0
# https://hq1.itiger.com/fundamental/usstock/earnings/balance/WFC?type=balance&symbol=WFC&deviceId=1531581656218&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0

# https://hq1.itiger.com/fundamental/usstock/earnings/balance/WFC?type=balance&symbol=WFC&deviceId=1531581656218&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0

url='https://hq1.itiger.com/fundamental/usstock/earnings/income/WFC?type=income&symbol=WFC&deviceId'+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
res=requests.get(url, headers=headers)
a=res.json()
li=a.get('data').get('page')
# for i in li:
#     if i.get('type') == '季报':
# 	    print(i.get('date'))
# 	    print(i.get('cell')[37])
#         # value=i.get('cell')[37].get('value')
#     if i.get('type') == '年报':
# 	    print(i.get('date'))
# 	    print(i.get('cell')[37].get('value'))

url='https://hq1.itiger.com/fundamental/usstock/earnings/balance/WFC?type=balance&symbol=WFC&deviceId='+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
res=requests.get(url, headers=headers)
a=res.json()
li_s=a.get('data').get('page')


dic={}
li_di=[]
for i in range(len(li)):
    # if i.get('type') == '季报':
	   #  print(i.get('date'))
	   #  print(i.get('cell')[59])
    #     # value=i.get('cell')[37].get('value')
    if li[i].get('type') == '年报':
        if li_s[i].get('type') == '年报' :
            if li[i].get('date') == li_s[i].get('date') :
                da=li[i].get('date')

                u=li[i].get('cell')[37].get('value').replace('亿','').replace(',','')
                d=li_s[i].get('cell')[59].get('value').replace('亿','').replace(',','')
                if d!= 0:
                	result=round(float(u)/float(d),4)
                    # print(result)
                if da in dic:
                    dic[da].append(result)
                else:
                    dic[da]=[]
                    dic[da].append(result)    
print(dic)
code=pd.read_csv('2018-06-24us_code.csv')                
print(code.tolist())