import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json


# http://finance.sina.com.cn/stock/usstock/sector.shtml        母URL
# url="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['f0j3ltzVzdo2Fo4p']/US_CategoryService.getList?page={}&num=60&sort=&asc=0&market=&id="
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
url_o="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['tUkf8x2DoimdDZGk']/US_CategoryService.getList?page={}&num=60&sort=&asc=0&market=O&id="
url_n="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['tUkf8x2DoimdDZGk']/US_CategoryService.getList?page={}&num=60&sort=&asc=0&market=N&id="
nn=1
def get_code(url,page,sign):
    global  nn
    li_code=[]
    li_name=[]
    li_category=[]
    li_pe=[]
    for i in range(1, page):
        print("--------------------------------------------"+str(nn)+"---------------------------------------------------------")
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
        nn=nn+1
        # uscode.append(str(cod))
    li=[]
    li.append(li_code)
    li.append(li_name)
    li.append(li_category)
    li.append(li_pe)
    pdd=pd.DataFrame(li,index=['code','name','category','pe'])
    pdd=pdd.T
    pdd['code']=[ i +sign for i in pdd["code"]]
    
    return pdd


n=get_code(url_n,74,'.N')
o=get_code(url_o,60,'.O')

result =n.append(o, ignore_index=True)

result = result[ ~ result['category'].str.contains('股权') ]
result.to_csv(date+"_all_us_basic.csv", index=False, encoding = 'gbk')







