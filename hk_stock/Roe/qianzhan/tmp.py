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


code=pd.read_csv('D:\\Git\\hk_stock\\basic\\hk_all_code.csv',encoding='gbk')
code['code']= code['code'].str.replace('hk','')
# print(code)                
li_code=code['code'].tolist()
for i in range(len(li_code)):
    li_code[i] = str(li_code[i]).replace('hk','')
# print(li_code)
n=1
lii=[]
# li=['2017年年报','2017年三季报','2017年中报','2017年一季报']
li=['2017年年报','2017年中报','2016年年报','2016年中报']
sum=pd.DataFrame()
for code_nm in li_code:
    print('----------------------------'+str(n)+'------------------------------------------')
    li_tmp=[]
    for i in li:
        url_pre='https://stock.qianzhan.com/hk/dubang?code='+code_nm+'.HK&time='+i+'&_='
        url=url_pre+ti
        time.sleep(0.5)
        res=requests.get(url, headers=headers)
        if res.status_code == 404:
            li_tmp.append('0')
        else:    
            a=res.text
            soup = BeautifulSoup(res.text, 'lxml')
            strr=soup.get_text()
            li_da=strr.split('\n')
            while '' in li_da:
                li_da.remove('')
            a=li_da[1:][::2]
            b=li_da[1:][1::2]
            if b:
                li_tmp.append(b[0])
            else:
                li_tmp.append('0')
    n=n+1
    print(li_tmp)
    lii.append(li_tmp)    
# print(lii)
pdd=pd.DataFrame(lii,columns=li)
pdd['code']=li_code
re=pd.merge(pdd,code,how='outer',on='code')
re.to_csv(date+"_all_roe_hk.csv", encoding='gbk')
