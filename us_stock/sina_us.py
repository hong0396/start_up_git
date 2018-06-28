import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json

uscode=[]
# http://finance.sina.com.cn/stock/usstock/sector.shtml        母URL
url="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['f0j3ltzVzdo2Fo4p']/US_CategoryService.getList?page={}&num=60&sort=&asc=0&market=&id="

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

for i in range(1, 146):
    print("----------------------------------------------------"+str(i)+"---------------------------------------------------------")
    time.sleep(0.1)
    html = urllib.request.urlopen(url.format(i)).read()
    html = html.decode('gbk')
    s = r'symbol(.*?)price'
    pat = re.compile(s)
    code = pat.findall(html)
    for j in code: 
        cod=j.replace(":","").replace(r'"',"").replace(",","")
        uscode.append(str(cod))
print(uscode)
pdd=pd.Series(uscode)
pdd.to_csv(date+"us_code.csv", index=False)






# print(html)
# s = r'\(\((.*?)\)\)'
# pat = re.compile(s)
# code = pat.findall(html)
# for item in code:



# test=re.sub('\'','\"',test) 
# test=re.sub('count','"count"',test)
# test=re.sub('data','"data"',test)
# test=re.sub('name','"name"',test)

# print(dic)
# year_du=dic.get('nd')