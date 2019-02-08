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
'Authorization': 'Bearer aAmt1vk9CI5QYnVMzRwXpfuvZmXmvo',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
requests.packages.urllib3.disable_warnings()
#标普500
# url_bp500='https://hq2.itiger.com/market/quote/package_indices_INX?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180825_733367&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# #中概股
# url_cn='https://hq2.itiger.com/market/quote/package_china?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180825_733367&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
# url_cn='https://hq.itiger.com/market/quote/package_china?page=1&compare=changeRate&minMarketCap=0&order=desc&deviceId=1531838872042&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_nsdq='https://hq2.itiger.com/market/quote/NASDAQ?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_ny='https://hq2.itiger.com/market/quote/NYSE?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_us='https://hq2.itiger.com/market/quote/AMEX?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_all='https://hq2.itiger.com/market/quote/ALL?page={}&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'

# url_all='https://hq.itiger.com/market/quote/ALL?page=4&compare=changeRate&minMarketCap=0&order=desc&deviceId=web20181118_904079&platform=desktop-app&env=TigerTrade&vendor=web&lang=&appVer=4.2.0'

def get_laohu_code(url, num=[0]):
    li=[]
    for i in num:
        print('--------------'+str(i)+'-----------------')
        con = requests.get(url.format(i), headers=header,verify=False).json()
        # print(con)
    # a = str(con.decode())
    # print(con.get('items')[0].get('data'))
        li_data=con.get('items')[0].get('data')
        for i in li_data:
            li_tmp=[]
            li_tmp.append(i.get('symbol'))
            li_tmp.append(i.get('nameCN'))
            li_tmp.append(i.get('open'))
            li_tmp.append(i.get('latestPrice'))
            li_tmp.append(i.get('volume'))
            li_tmp.append(i.get('volumeRatio'))
            li_tmp.append(i.get('peRate'))
            li_tmp.append(i.get('pbRate'))
            li_tmp.append(i.get('eps'))
            li.append(li_tmp)
    pdd=pd.DataFrame(li, columns= ['code','name','open','latestPrice','volume','volumeRatio','pe','pb','eps'])   
    return pdd

# cn_nsdq=get_laohu_code(url_nsdq, [i for i in range(65)])
# cn_ny=get_laohu_code(url_ny, [i for i in range(86)])
# cn_us=get_laohu_code(url_us, [i for i in range(14)])
# frames=[cn_nsdq,cn_ny,cn_us]
# sum=pd.concat(frames,ignore_index=True)
# sum.to_csv(date+'us_all_code.csv', index=False, encoding ='gbk')


cn_us=get_laohu_code(url_all, [i for i in range(167)])
cn_us.to_csv(date+'us_all_code.csv', index=False, encoding ='gbk')

