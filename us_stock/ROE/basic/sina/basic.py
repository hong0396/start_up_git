import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json

li_code=[]
li_name=[]
li_category=[]
li_pe=[]
# http://finance.sina.com.cn/stock/usstock/sector.shtml        母URL
# url="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['f0j3ltzVzdo2Fo4p']/US_CategoryService.getList?page={}&num=60&sort=&asc=0&market=&id="

url="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['tUkf8x2DoimdDZGk']/US_CategoryService.getList?page={}&num=60&sort=&asc=0&market=O&id="
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

for i in range(1, 60):
    print("----------------------------------------------------"+str(i)+"---------------------------------------------------------")
    time.sleep(0.1)
    html = urllib.request.urlopen(url.format(i)).read()
    html = html.decode('gbk')
    s = r'cname(.*?)price'
    t = r'mktcap(.*?)market'
    pat = re.compile(s)
    code = pat.findall(html)
    for j in code: 
        # print(j)
        name=j.split('"')[1]
        cod=j.split('"')[-2]
        if 'null' in str(j) :
            category = ''
        else:
            category=j.split('"')[3]
        li_code.append(cod)
        li_name.append(name)
        li_category.append(category)
    pat = re.compile(t)
    pe = pat.findall(html)
    # print(html)
    for k in pe:
        pee=k.split(',')[1]
        if 'null' in  str(pee):
            pe_num=''
        else:
            pe_num=pee.split('"')[1]
        li_pe.append(pe_num)  
        # uscode.append(str(cod))

li=[]
li.append(li_code)
li.append(li_name)
li.append(li_category)
li.append(li_pe)
pdd=pd.DataFrame(li,index=['code','name','category','pe'])
pdd=pdd.T
pdd.to_csv(date+"_all_us_basic_N.csv", index=False, encoding = 'gbk')




