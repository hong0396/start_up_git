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


header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Authorization': 'Bearer xjUfeh4B6FC2irTORX0BeNqqY6nc0i',
'Connection': 'keep-alive',
'Host': 'hq.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

#标普500
url_bp500='https://hq.itiger.com/market/quote/package_indices_INX?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=1531838872042&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
#中概股
url_cn='https://hq.itiger.com/market/quote/package_china?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=1531838872042&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# url_cn='https://hq.itiger.com/market/quote/package_china?page=1&compare=changeRate&minMarketCap=0&order=desc&deviceId=1531838872042&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'


def get_laohu_code(url, num=[0]):
    li=[]
    for i in num: 
        con = requests.get(url.format(i), headers=header).json()
    # a = str(con.decode())
    # print(con.get('items')[0].get('data'))
        li_data=con.get('items')[0].get('data')
        for i in li_data:
            li_tmp=[]
            li_tmp.append(i.get('symbol'))
            li_tmp.append(i.get('nameCN'))
            li_tmp.append(i.get('peRate'))
            li_tmp.append(i.get('pbRate'))
            li_tmp.append(i.get('eps'))
            li.append(li_tmp)
    pdd=pd.DataFrame(li, columns= ['code','name','pe','pb','eps'])   
    return pdd

bp500=get_laohu_code(url_bp500, [0,1,2,3,4,5,6,7,8,9])
bp500.to_csv('us_bp500_code.csv', index=False, encoding ='gbk')


cn=get_laohu_code(url_cn, [0,1])
cn.to_csv('us_cn_code.csv', index=False, encoding ='gbk')
