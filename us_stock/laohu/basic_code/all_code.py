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
header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Authorization': 'Bearer TSPJVspkvvZovEJW1mYMhkc8zlBD90',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

#标普500
# url_bp500='https://hq2.itiger.com/market/quote/package_indices_INX?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180825_733367&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# #中概股
# url_cn='https://hq2.itiger.com/market/quote/package_china?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180825_733367&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# url_cn='https://hq.itiger.com/market/quote/package_china?page=1&compare=changeRate&minMarketCap=0&order=desc&deviceId=1531838872042&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_nsdq='https://hq2.itiger.com/market/quote/NASDAQ?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_ny='https://hq2.itiger.com/market/quote/NYSE?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_us='https://hq2.itiger.com/market/quote/AMEX?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
def get_laohu_code(url, num=[0]):
    li=[]
    for i in num:
        con = requests.get(url.format(i), headers=header).json()
        # print(con)
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

# bp500=get_laohu_code(url_bp500, [0,1,2,3,4,5,6,7,8,9])
# bp500.to_csv('us_bp500_code.csv', index=False, encoding ='gbk')


# cn=get_laohu_code(url_cn, [0,1])
# cn.to_csv('us_cn_code.csv', index=False, encoding ='gbk')

cn_nsdq=get_laohu_code(url_nsdq, [i for i in range(65)])
cn_nsdq.to_csv(date+'us_nsdq_code.csv', index=False, encoding ='gbk')


cn_ny=get_laohu_code(url_ny, [i for i in range(86)])
cn_ny.to_csv(date+'us_ny_code.csv', index=False, encoding ='gbk')


cn_us=get_laohu_code(url_us, [i for i in range(14)])
cn_us.to_csv(date+'us_us_code.csv', index=False, encoding ='gbk')

frames=[cn_nsdq,cn_ny,cn_us]
sum=pd.concat(frames,ignore_index=True)
sum.to_csv(date+'us_all_code.csv', index=False, encoding ='gbk')
