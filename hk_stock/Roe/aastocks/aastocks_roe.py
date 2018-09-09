import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import re
import tushare as ts
from bs4 import BeautifulSoup
import time


date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
hee=['2013', '2014', '2015', '2016', '2017', '2018']
roe2013=[]
roe2014=[]
roe2015=[]
roe2016=[]
roe2017=[]
roe2018=[]
li=[roe2013,roe2014,roe2015,roe2016,roe2017,roe2018]
n=0

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])



code=pd.read_csv('D:\\Git\\hk_stock\\basic\\hk_all_code.csv',encoding='gbk')
code['code']= code['code'].str.replace('hk','')
# print(code)                
li_code=code['code'].tolist()




for co in li_code:
    print('--------------------------'+str(n)+'--------------------------------')
    url='http://www.aastocks.com/tc/stocks/analysis/company-fundamental/financial-ratios?symbol='+str(co)
    res=requests.get(url, headers=headers)
    html=res.text
    # print(a)
    s = r'截止日期(.*?)走勢'
    pat = re.compile(s)
    cod = pat.findall(html)
    s = r'">(.*?)</td>'
    pat = re.compile(s)
    code_year = pat.findall(cod[0])
    # print(code_year)
    coun=len(code_year)
    s = r'股東權益回報率(.*?)資本運用回報率'
    pat = re.compile(s)
    codd = pat.findall(html)
    if  codd:
        if not codd is None:
            s = r'">(.*?)</td>'
            pat = re.compile(s)
            code_value = pat.findall(codd[0])
            print(code_value[:coun])

    for i in li:
        i.append('0')

    for i in range(coun):
        for j in range(len(hee)):
            if code_year[i][:4]==hee[j]:
                li[j][n]=code_value[i]

    n=n+1

pdd=pd.DataFrame(li,   columns=li_code, index=[ 'roe2013','roe2014','roe2015','roe2016','roe2017','roe2018'])
pan=pdd.T
pan['code'] = li_code
re=pd.merge(code,pan,how='outer',on='code')
re.to_csv(date+'_aastocks_uk_roe.csv', encoding = 'gbk',index=False)




