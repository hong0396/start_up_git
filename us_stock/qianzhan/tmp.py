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
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

li=['2017年年报','2017年三季报','2017年中报','2017年一季报']
sum=pd.DataFrame()
for i in li:
    url_pre='https://stock.qianzhan.com/us/dubang?code=BABA.N&time='+i+'&_='
    url=url_pre+ti
    time.sleep(0.5)
    res=requests.get(url, headers=headers)
    a=res.text
    soup = BeautifulSoup(res.text, 'lxml')
    str=soup.get_text()
    li_da=str.split('\n')
    while '' in li_da:
        li_da.remove('')
    a=li_da[1:][::2]
    b=li_da[1:][1::2]
    data=pd.Series(b,index=a)
    sum[i] = data    
print(sum)
sum.to_csv(date+"sum_us.csv", encoding='gbk')