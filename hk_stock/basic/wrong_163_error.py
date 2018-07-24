import urllib.request
import re
import time
import requests
import csv
import pandas as pd
from sqlalchemy import create_engine
# import pymysql
import random
from  bs4 import BeautifulSoup
import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json

header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
# http://quotes.money.163.com/old/#query=hkmain
li_s=[]
for i in range(0,70):
    print('------------------------------'+str(i)+'------------------------------------------------')  
    url='http://quotes.money.163.com/hk/service/hkrank.php?host=/hk/service/hkrank.php&page={}&query=CATEGORY:MAIN;TYPE:1;EXCHANGE_RATE:_exists_true&fields=no,SYMBOL,NAME,PRICE,PERCENT,UPDOWN,OPEN,YESTCLOSE,HIGH,LOW,VOLUME,TURNOVER,EXCHANGE_RATE,ZF,PE,MARKET_CAPITAL,EPS,FINANCEDATA.NET_PROFIT,FINANCEDATA.TOTALTURNOVER_&sort=PERCENT&order=desc&count=24&type=query&callback=callback_1620346970&req=01649'
    html = requests.get(url.format(str(i)), headers=header).content
    html = html.decode()
    s = r'NAME":(.*?),"TURNOVER'
    pat = re.compile(s)
    code = pat.findall(html)
    for j in code:
        li=[]
        dic=eval('{"name":'+str(j)+'}') 
        name=dic.get('name')
        pe=dic.get('PE')
        code=str(dic.get('SYMBOL'))
        # pd_tmp=pd.Series(dic)
        # print(code)
        li.append('hk'+code)
        li.append(name)
        li.append(pe)
        li_s.append(li)
print(li_s)
df=pd.DataFrame(li_s,columns = ['code','name','pe'])
print(df)
df.to_csv('hk_all_code.csv', encoding='gbk', index=False)