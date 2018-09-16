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
# import io  
# import sys 

# #改变标准输出的默认编码 
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

ti=str(time.time()).replace('.','')[:13]
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_ga=GA1.2.1014337857.1535199318; _gid=GA1.2.1673177870.1536338616; verification="2|1:0|10:1536383158|12:verification|88:NGM1ODI5NzljNTljMjE3MmNjMjU4OWJiYjZlMTE0YzFiODQ0MzJjZTU0ZTYxZWFkM2VlNjZjM2E4ZDZhNjY0MA==|6bc528d48cdf19be96286bed4de903355fb4891e3119f7f0486676a746ca270d"; session_id="2|1:0|10:1536383158|10:session_id|88:MGM0OGVlNjIzY2NjMGIzMWI4YzZlNzY0OWYzMjgxNDc4Zjg5MDdlZjM5OGMxMGU0NjYwNzY4ZTc3MmZkN2NhYw==|8a07424b6fceb557e00b0deb86816d854048a514515a3f69a73cbef846df8627"; ngxid=fPoiPluTWLYPZSM6JRvsAg==; _gat=1; Hm_lvt_aec1ec63a0f76f572b0928df8b4b8211=1535199318,1536338616,1536383152; Hm_lpvt_aec1ec63a0f76f572b0928df8b4b8211=1536383152',
'Host': 'www.tigerbbs.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

# https://www.tigerbbs.com/hq/s/SFUN
code=pd.read_csv('D:/Git/us_stock/laohu/basic_code/2018-08-25us_all_code.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()



# url='https://hq1.itiger.com/stock_info/profile/EVRI?deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'

li=[]
nu_nu=0
for code_nm in li_code:
    print('------------------------------------------'+str(nu_nu)+'----------------------------------------------')
    url='https://www.tigerbbs.com/api/v1/stock/publicity?_s='+ti+'&symbol='+code_nm
    con = requests.get(url, headers=header).json()
    time.sleep(1)
    try:
        description=con.get('data').get('profile').get('items')[0].get('description').encode('GBK','ignore').decode('GBk')
    except:
        description=0    
    # websiteUrl=con.get('data').get('profile').get('items')[0].get('websiteUrl')
    # table=con.get('data').get('publicity').get('data').get('earnings').get('table')
    li.append(0)
    li[nu_nu]=description
    nu_nu=nu_nu+1


# code=code[:1000]
code['description'] =li
code.to_csv(date+'_Laohu_us_basic_description.csv', encoding ='gbk', index=False)



# frames=[cn_nsdq,cn_ny,cn_us]
# sum=pd.concat(frames,ignore_index=True)
# sum.to_csv(date+'us_all_code.csv', index=False, encoding ='gbk')


