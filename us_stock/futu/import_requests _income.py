import requests
import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time

headers={
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Cookie': 'UM_distinctid=165fa9285fb762-07c06f613d5cac-8383268-e1000-165fa9285fc20a; cipher_device_id=1537507232150902; tgw_l7_route=8d34ab350eb9a9772a5a0c377f34d47d',
'Host': 'finance.futunn.com',
'Origin': 'https://www.futunn.com',
'Referer': 'https://www.futunn.com/quote/stock-info?m=us&code=CYTXW&type=finance_analyse',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'	
}

url='https://finance.futunn.com/api/finance/balance-sheet?code=CYTXW&label=us&quarter=0&page=0'
r = requests.get(url,headers=headers).json()
print(r.get("data").get("list").get('keys'))
print(r.get("data").get("list").get('title'))
print(r.get("data").get("list").get('values'))
print(r.get("data").get("pages"))

# df=pd.DataFrame(r.get("data").get("list"))
# print(df.columns)
