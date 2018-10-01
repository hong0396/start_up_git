import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
from functools import reduce

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'globalquote.morningstar.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

url_quar = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=XNYS:VZ&region=usa&culture=en-US&version=SAL&cur=&reportType=is&period=3&dataType=A&order=desc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw'

li=[]
with requests.Session() as s:
    download = s.get(url_quar)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    # for row in my_list:
    #     print(row)
# lens=len(my_list[1])
# print(lens)
df=pd.DataFrame(my_list)
df=df.dropna(thresh=2)
print(df)
df.to_csv('tmp.csv')
