import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import tushare as ts
headers={'Host': 'xueqiu.com',
'Cookie': 'aliyungf_tc=AQAAABC8hwW8ngsAZ/2vtKIadPbejCVj; s=eh18k6ppna; xq_a_token=aef774c17d4993658170397fcd0faedde488bd20; xq_r_token=d694856665e58d9a55450ab404f5a0144c4c978e; Hm_lvt_1db88642e346389874251b5a1eded6e3=1532354581; __utmc=1; __utmz=1.1532354581.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; u=741532354581327; device_id=d27209e0e459010fe1ccadbc3ee683ab; _ga=GA1.2.680721423.1532354581; _gid=GA1.2.1042949822.1532354583; __utma=1.680721423.1532354581.1532354581.1532359117.2; __utmt=1; __utmb=1.3.10.1532359117; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1532359429',
'Referer': 'https://xueqiu.com/hq',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}

# https://xueqiu.com/hq#exchange=US&firstName=3&secondName=3_0
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])

url='https://xueqiu.com/stock/cata/stocklist.json?page=3&size=90&order=desc&orderby=percent&type=30&isdelay=1&_='+ti
res=requests.get(url, headers=headers).json()
print(res)