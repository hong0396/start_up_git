import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import tushare as ts
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
ti=str(time.time()).replace('.','')[:13]
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
ddate=time.strftime('%Y%m%d',time.localtime(time.time()))
print(str(time.time()).replace('.','')[:13])
headers={
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Authorization': 'Bearer I9r5yBcnSp862cBaRXJOKiApzanXlp9rpU19PiRcBqGPhtjhTO',
'Connection': 'keep-alive',
'Host': 'hq.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quote/00700/finance',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# https://hq1.itiger.com/fundamental/usstock/earnings/cash/WFC?type=cash&symbol=WFC&deviceId=1531581656218&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0
# https://hq1.itiger.com/fundamental/usstock/earnings/balance/WFC?type=balance&symbol=WFC&deviceId=1531581656218&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0

# https://hq1.itiger.com/fundamental/usstock/earnings/balance/WFC?type=balance&symbol=WFC&deviceId=1531581656218&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0


code=pd.read_csv('D:\\Git\\hk_stock\\basic\\hk_all_code.csv',encoding='gbk')
code['code']= code['code'].str.replace('hk','')
# print(code)                
li_code=code['code'].tolist()
# for i in range(len(li_code)):
#     li_code[i] = str(li_code[i]).replace('hk','')



# url='https://hq1.itiger.com/fundamental/usstock/earnings/income/WFC?type=income&symbol=WFC&deviceId'+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# res=requests.get(url, headers=headers)
# a=res.json()
# li=a.get('data').get('page')
# for i in li:
#     if i.get('type') == '季报':
# 	    print(i.get('date'))
# 	    print(i.get('cell')[37])
#         # value=i.get('cell')[37].get('value')
#     if i.get('type') == '年报':
# 	    print(i.get('date'))
# 	    print(i.get('cell')[37].get('value'))

dic={}
codd=[]
roe2017 =[]
roe2016 =[]
roe2015 =[]
roe2014 =[]
li_sum=[roe2014,roe2015,roe2016,roe2017]
li_time=['2014-12-31','2015-12-31','2016-12-31','2017-12-31']
nu_nu=0
def get_roe(code):
    global nu_nu
    print('--------------------------'+str(nu_nu)+'--------------------------------')
    url='https://hq1.itiger.com/fundamental/hkstock/earnings/income/'+code+'?type=income&symbol='+code+'&deviceId=web20180729_724221&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
    res=requests.get(url, headers=headers)
    a=res.json()
    li=a.get('data').get('page')
    li_h=a.get('data').get('header')
    num=2018
    # print(li_h)
    if not li_h is None:
        for h in range(len(li_h)):
            if li_h[h].get('name') ==  "经营盈利":
                num=h
    time.sleep(0.5)
    url='https://hq1.itiger.com/fundamental/hkstock/earnings/balance/'+code+'?type=balance&symbol='+code+'&deviceId=web20180729_724221&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'  
    res=requests.get(url, headers=headers)
    a=res.json()
    li_s=a.get('data').get('page')
    li_s_h=a.get('data').get('header')
    num_s=2018
    if not li_s_h is None:
        for g in range(len(li_s_h)):
            if li_s_h[g].get('name') == "股东权益/亏损(合计)" :
                num_s=g
    li_di=[]
    
    for p in li_sum:
        p.append(0)

    if num != 2018 and  num_s != 2018:    
        if not li_s is None:
            for i in range(min(len(li_s),len(li))):
        # if i.get('type') == '季报':
    	   #  print(i.get('date'))
    	   #  print(i.get('cell')[59])
        #     # value=i.get('cell')[37].get('value')
                if li[i].get('type') == '年报':
                    if li_s[i].get('type') == '年报' :
                        if li[i].get('date') == li_s[i].get('date') :   
                            for m in range(len(li_time)):
                                if  li[i].get('date')[:4] == li_time[m][:4] :  
                                    if not li[i].get('cell')[num].get('value').replace(' ','').strip() is None:
                                        u_tmp=li[i].get('cell')[num].get('value').replace(',','').replace('人民币','').replace('港币','').replace('美元','').replace('加元','').replace('日元','').replace('新加坡元','').replace('欧元','').replace('\n','').replace(' ','').strip()                                              
                                        if '亿' in u_tmp:
                                            u_tmp=u_tmp.replace('亿','').replace(',','')
                                            u=float(u_tmp)*100000000
                                        elif '百万' in u_tmp:
                                            u_tmp=u_tmp.replace('百万','').replace(',','')
                                            u=float(u_tmp)*1000000
                                        elif '千' in u_tmp:
                                            u_tmp=u_tmp.replace('千','').replace(',','')
                                            u=float(u_tmp)*1000
                                        else:
                                            u=u_tmp.replace(',','')
                                        if not li_s[i].get('cell')[num_s].get('value').replace(' ','').strip() is None:  
                                            d_tmp=li_s[i].get('cell')[num_s].get('value').replace(',','').replace('人民币','').replace('港币','').replace('美元','').replace('加元','').replace('日元','').replace('新加坡元','').replace('欧元','').replace('\n','').replace(' ','').strip()                                                                                        
                                            if '亿' in d_tmp:
                                                d_tmp=d_tmp.replace('亿','').replace(',','')
                                                d=float(d_tmp)*100000000
                                            elif '百万' in d_tmp:
                                                d_tmp=d_tmp.replace('百万','').replace(',','')
                                                d=float(d_tmp)*1000000
                                            elif '千' in d_tmp:
                                                d_tmp=d_tmp.replace('千','').replace(',','')
                                                d=float(d_tmp)*1000
                                            else:
                                                d=d_tmp.replace(',','')
                                            # print(u)
                                            # print('---')
                                            print(d)
                                            # print('----')
                                            if str(d).replace(' ','').strip():
                                                if not str(d).replace(' ','').strip() is None:
                                                    if np.float64(d) != 0.0:     
                                                        li_sum[m][nu_nu]=round(float(u)/np.float64(d),4)
                                                    # print(li_sum[m][nu_nu])
    nu_nu=nu_nu+1
                    # print(result)
                    # if da in dic:
                    #     dic[da].append(result)
                    # else:
                    #     dic[da]=[]
                    #     dic[da].append(result)    


for k in li_code:
    get_roe(k)
print(li_sum)
pdd=pd.DataFrame(li_sum,   columns=li_code, index=[ '2014-12-31','2015-12-31','2016-12-31','2017-12-31'])
pan=pdd.T
pan['code'] = li_code
re=pd.merge(code,pan,how='outer',on='code')
re.to_csv(date+'Laohu_uk_roe.csv', encoding = 'gbk',index=False)

















































# url='https://hq1.itiger.com/fundamental/usstock/earnings/income/WFC?type=income&symbol=WFC&deviceId'+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# res=requests.get(url, headers=headers)
# a=res.json()
# li=a.get('data').get('page')
# time.sleep(0.2)
# url='https://hq1.itiger.com/fundamental/usstock/earnings/balance/WFC?type=balance&symbol=WFC&deviceId='+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# res=requests.get(url, headers=headers)
# a=res.json()
# li_s=a.get('data').get('page')

# li_di=[]
# for i in range(len(li)):
#     # if i.get('type') == '季报':
#        #  print(i.get('date'))
#        #  print(i.get('cell')[59])
#     #     # value=i.get('cell')[37].get('value')
#     if li[i].get('type') == '年报':
#         if li_s[i].get('type') == '年报' :
#             if li[i].get('date') == li_s[i].get('date') :
#                 da=li[i].get('date')

#                 u=li[i].get('cell')[37].get('value').replace('亿','').replace(',','')
#                 d=li_s[i].get('cell')[59].get('value').replace('亿','').replace(',','')
#                 if d!= 0:
#                     result=round(float(u)/float(d),4)
#                     # print(result)
#                 if da in dic:
#                     dic[da].append(result)
#                 else:
#                     dic[da]=[]
#                     dic[da].append(result)   