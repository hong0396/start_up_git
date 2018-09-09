import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import tushare as ts
from bs4 import BeautifulSoup
import time

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])

code=pd.read_csv('D:\\Git\\hk_stock\\basic\\hk_all_code.csv',encoding='gbk')
code['code']= code['code'].str.replace('hk','')
# print(code)                
li_code=code['code'].tolist()
# for i in range(len(li_code)):
#     li_code[i] = str(li_code[i]).replace('hk','')
li_pd=[]
for code  in li_code[:5]: 
    url='http://www.finet.hk/stock_quote_detail/financial_ratios/'+str(int(code))
    res=requests.get(url, headers=headers)
    a=res.text
    soup = BeautifulSoup(res.text,"lxml")
    year=soup.find("tr", "noMobile").find_all('th')[1:]
    count=len(year)
    # print(count)
    li=[]
    li_c=[]
    num=0
    for i in year:
	    li.append(i.string.replace('	','').replace('\n','').strip())
    con=soup.find("table", "financialRatiosTable withSubTitle withGroupName").find_all('td')
    for i in range(len(con)):
        tmp=con[i].string.replace('	','').replace('\n','').strip()
        if tmp == '股東權益回報 (%)':
            num=i

        if tmp == '總資產週轉率 (倍)':
            num2=i
        
    for i in range(num+1,num+count+1):
        tt=con[i].string.replace('	','').replace('\n','').strip()
        li_c.append(tt)
    # aa=dict(zip(li,li_c))
    pdds=pd.DataFrame([li,li_c],columns=li)
    li_pd.append(pdds)
for i in li_pd:
	print(i)


