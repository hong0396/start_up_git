
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

url='https://androidinvest.com/Stock/HistoryNetProfit/SH600000/'

res=requests.get(url, headers=headers)
# print(res.text)
soup=BeautifulSoup(res.text,'html.parser')
chart1=soup.find_all(id="chart1")[0].contents[0].split('@')
chart2=soup.find_all(id="chart2")[0].contents[0].split('@')
print(chart1[0].replace("'",'').replace('[','').replace(']','').replace(' ','').split(','))
print(chart1[1].replace("'",'').replace('[','').replace(']','').replace(' ','').split(','))
print(chart1[2].replace("'",'').replace('[','').replace(']','').replace(' ','').split(','))

da=chart1[0].replace("'",'').replace('[','').replace(']','').replace(' ','').split(',')
env=chart1[1].replace("'",'').replace('[','').replace(']','').replace(' ','').split(',')
price=chart1[2].replace("'",'').replace('[','').replace(']','').replace(' ','').split(',')

li=[]
li.append(da)
li.append(env)
li.append(price)
pd=pd.DataFrame(li)
print(pd.T)

