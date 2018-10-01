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
from bs4 import BeautifulSoup
from yahoo_fin.stock_info import *


 
header={'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'ApiKey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
'Connection': 'keep-alive',
'Cookie': r'__cfduid=d374f72b7e842bc1512728371c59006221535177605; _hp2_id.3435576498=%7B%22userId%22%3A%224644259421237253%22%2C%22pageviewId%22%3A%224282435037345011%22%2C%22sessionId%22%3A%226599725213866076%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga=GA1.2.2104883309.1537714039; _gid=GA1.2.218355779.1537714039; mid=14414344621903754759; __utmz=172984700.1537714129.1.1.utmcsr=investingengineer.com|utmccn=(referral)|utmcmd=referral|utmcct=/5-best-free-financial-data-websites/; fp=015153771413020561; _gcl_au=1.1.1418337664.1537714480; activeTab=0; s_pers=%20s_nr%3D1537714943980-New%7C1540306943980%3B%20s_lv%3D1537714943981%7C1632322943981%3B%20s_lv_s%3DFirst%2520Visit%7C1537716743981%3B; qs_wsid=7D55250CC11FDA252C5F0CD6D33555C0; __utma=172984700.2104883309.1537714039.1537714129.1537768227.2; __utmc=172984700; AMCVS_54E6587D53EB65370A490D4B%40AdobeOrg=1; AMCV_54E6587D53EB65370A490D4B%40AdobeOrg=1099438348%7CMCIDTS%7C17798%7CMCMID%7C62012994586085940540622446501872550049%7CMCAAMLH-1538319277%7C11%7CMCAAMB-1538373178%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1537775578s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C2.1.0; s_cc=true; JSESSIONID=8785DE7B7114BD8268897AD27951E87D; Hint=usw2e15; _parsely_visitor={%22id%22:%22pid=bd4c9407684de3caea2b58afad90af77%22%2C%22session_count%22:2%2C%22last_session_ts%22:1537768949242}; ScrollY=0; __utmt=1; s_sq=%5B%5BB%5D%5D; mbox=PC#43ea85e86ae145be827843decfcbaa53.24_11#1538980435|session#94c12d3bcb8d4da984d4c4c328683dd6#1537772695|disable#browser%20timeout#1537771218|check#true#1537770895; __utmb=172984700.34.10.1537768227',
'Host': 'api-global.morningstar.com',
'Origin': 'https://www.morningstar.com',
'Referer': 'https://www.morningstar.com/stocks/XNYS/KO/quote.html',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'X-API-REALTIME-E': 'eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.2Zug-k2AXyJpzaCMxrYuHsrGcAnkouyiMbSyYoAuCIFiwAj580i0bFIXliYN7xWVOLmB8H-VcBsePQvjr_3IQ5m8oo1pQsVOPVE5VTbO0l1iHEL328Qb7224A0SozdtUVkaAUFMrTAXmQL4C8yN0o-HbCXfp3ZCtNSVrVRzR_0s.7eHURjPkwC11sAoo.qlE-D2Z3pFuUvDF8ip5ekWOno4XUhZ_SKoyjHClKKS1vWj4qwHe5_O44IjQbF5F3Vv9hw-vs2xc32PzZHRIgLsd71B8g_EHtds2TbwvmDCTPTCI77mZluUCSncEv9BsNy2-LdRf5g86ZYr6WsNcjumCj7qVExXZVwb3imgI-KFQLEBEuxMZuz9OryRgkDWcsDNGEp06rh3xkRCfGFofRFjnIlw.GRYMb9h_uDSxtyQ4JPy_fA',
'X-API-RequestId': '5b03676b-dc69-cf53-6d82-519bb2d80fc0',
'X-SAL-ContentType': 'e7FDDltrTy+tA2HnLovvGL0LFMwT+KkEptGju5wXVTU='}

# https://www.morningstar.com/stocks/XNYS/KO/quote.html
url='https://api-global.morningstar.com/sal-service/v1/stock/morningstarTake/v3/ticker=KO/analysisData'

# http://financials.morningstar.com/valuation/price-ratio.html?t=KO
# url='https://morningstar-api.herokuapp.com/analysisData?ticker=GE'

# con=requests.get(url,headers=header)
# print(con.text)


tickers = tickers_nasdaq()
tickers_other = tickers_other()
tickers_all=tickers+tickers_other
print(tickers_all)
# tickers_all=tickers_all[:5]
# XNAS

# url='https://www.morningstar.com/stocks/XNYS/{}/quote.html'
url='https://www.morningstar.com/stocks/xnas/{}/quote.html'
li=[]
for i in range(len(tickers_all)):
    time.sleep(0.5)
    code_tmp='0'
    toker_tmp='0'
    print('------------------------'+str(i)+'-------------------------------------')
    con=requests.get(url.format(str(tickers_all[i])))
    print(con.status_code)
    if con.status_code==200:
        soup = BeautifulSoup(con.text,'lxml', from_encoding='utf-8')
        # print(soup.head.find_all('meta'))
        for link in soup.head.find_all('meta'):
            if link.get('name') == "performanceId" :
                code_tmp=link.get('content')

            if link.get('name') == "ticker" :
                toker_tmp=link.get('content')
    dic_tmp={'code':code_tmp,'toker':toker_tmp}
    li.append(dic_tmp)

# <meta content="0P000001BW" name="performanceId"/>
# <meta content="KO" name="ticker"/>

df_tmmp=pd.DataFrame(li)
df_tmmp.to_csv('code_toker.csv')


