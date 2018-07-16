
import tushare as ts
import pandas as pd
import time
import time, datetime
import calendar
import urllib.request
import urllib.error
import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import tushare as ts
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
ti=str(time.time()).replace('.','')[:13]
print(ti)
df = ts.get_stock_basics()
df = df[ ~ df['name'].str.contains('ST') ]
df = df[ ~ df['name'].str.contains('退市')]
# df = df[df['timeToMarket']<20180101 ]
# date = df.ix['600848']['timeToMarket']
# da= df.iloc(:,['code', 'name'])
code=df.index.tolist()
name=df['name'].tolist()
bvps=df['bvps'].tolist()
timeToMarket=df['timeToMarket'].tolist()
# print(len(code))
# print(len(name))
# print(len(bvps))
a=[]
a.append(code)
a.append(name)
a.append(bvps)
a.append(timeToMarket)
dd=pd.DataFrame(a)
# print(dd.T)
dff=dd.T
dff.columns=["code","name","bvps","timeToMarket"]

for i in dff["code"].index:
	if(str(dff.ix[i, "code"])[:2]=='60'):
	    dff.ix[i, "code"]='sh'+str(dff.ix[i, "code"])
	else:
		dff.ix[i, "code"]='sz'+str(dff.ix[i, "code"])
	# print(str(dff.ix[i, "code"]))

url_pre='https://gupiao.baidu.com/api/stocks/stockmonthbar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code={}&step=3&start=&count=320&fq_type=front&timestamp='
       # 'https://gupiao.baidu.com/api/stocks/stockmonthbar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=sz000651&step=3&start=20040930&count=160&fq_type=front&timestamp='
url=url_pre+ti


li_s=[]
for i in dff["code"].index.tolist():
    print('-------------------------------------'+str(i)+'-----------------------------------------------------')
    time.sleep(0.3)
    res=requests.get(url.format(str(dff.ix[i, "code"])), headers=headers)
    a=res.json()
    li=[]
    if a.get("errorMsg") == 'SUCCESS':
        # print(a.get('mashData'))
        if not a.get('mashData') is None:
            lis=a.get('mashData')
            start=a.get('mashData')[-1]
            close_start=start.get('kline').get('close')
            date_start=start.get('date')
            li.append(date_start)
            li.append(close_start)
            end=a.get('mashData')[0]
            close_end=end.get('kline').get('close')
            date_end=end.get('date')            
            grow=(close_end-close_start)/close_start
            li.append(date_end)
            li.append(close_end)
            li.append(grow)


            for j in lis[0:-1:12][::-1]:
                close_end=j.get('kline').get('close')
                date_end=j.get('date')
                li.append(date_end)
                li.append(close_end)

            
            
    else:
        pass
    li_s.append(li)
print(li_s)
pd_li=pd.DataFrame(li_s)
result = pd.concat([dff, pd_li], axis=1)
result.to_csv(date+'baidu_result_tmp1.csv', encoding='gbk')

# print(a)


#     url=url_pre+ti
#     time.sleep(0.5)
#     res=requests.get(url, headers=headers)
#     a=res.text
#     soup = BeautifulSoup(res.text, 'lxml')
#     str=soup.get_text()
#     li_da=str.split('\n')
#     while '' in li_da:
#         li_da.remove('')
#     a=li_da[1:][::2]
#     b=li_da[1:][1::2]
#     data=pd.Series(b,index=a)
#     sum[i] = data    
# print(sum)
