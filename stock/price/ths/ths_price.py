import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast, os ,re
from functools import reduce
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine
import xarray as xr
from fake_useragent import UserAgent


ua = UserAgent()
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
def get_date(soup):
    aa =re.findall(r'[^()]+', soup.text)[1]
    dictinfo = json.loads(aa) 
    date=[]
    for i in dictinfo.get('sortYear'):
        li=[]
        li.append(str(i[0]))
        li_tmp=li*i[1]
        # print(li_tmp)
        date.extend(li_tmp)
    # print(date)    
    if len(date) == len(list(dictinfo.get('dates').split(','))):
        date_new=map(lambda x, y: x + y, date, list(dictinfo.get('dates').split(',')))
        date_new =list(date_new)
    else:
        print('数据有误')
    a=list(dictinfo.get('price').split(','))
    b=[]
    for i in range(0, len(a), 4):
        b.append(a[i:i+4])
    open=[]
    close=[]
    low=[]
    high=[]
    for i in b:
        low.append(int(i[0])/100)
        open.append((int(i[0])+int(i[1]))/100)
        high.append((int(i[0])+int(i[2]))/100)
        close.append((int(i[0])+int(i[3]))/100)     
    p=pd.DataFrame({'date':date_new, 'low':low,'close':close, 'high':high,'open':open, 'volumn': list(dictinfo.get('volumn').split(','))  })
    return p

user_agent = [ 
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", 
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50", 
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0", 
"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko", 
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)", 
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)", 
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)", 
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", 
"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1", 
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11", 
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11", 
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)", 
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)", 
"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5", 
"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5", 
"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5", 
"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1", 
"MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1", 
"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10", 
"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13", 
"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+", 
"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0", 
"Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124", 
"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)", 
"UCWEB7.0.2.37/28/999", 
"NOKIA5700/ UCWEB7.0.2.37/28/999", 
"Openwave/ UCWEB7.0.2.37/28/999", 
"Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999", 
] 






#获取动态cookies
def get_cookie():
    global cookie_v
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('--proxy-server='+str(PROXY))
    chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver=webdriver.Chrome(executable_path=chromedriver,chrome_options=options)
    url="http://stockpage.10jqka.com.cn/HQ_v4.html" #http://stock.10jqka.com.cn/
    driver.get(url)
    # 获取cookie列表
    cookie=driver.get_cookies()
    # print(cookie)
    for i in cookie:
        if i.get('name') == 'v':
            cookie_v = i.get('value') 
    driver.close()        
    return cookie_v


url_month='http://d.10jqka.com.cn/v6/line/{}/21/all.js'
url_week='http://d.10jqka.com.cn/v6/line/{}/11/all.js'
url_day='http://d.10jqka.com.cn/v6/line/{}/01/all.js'


def get_df(url):
    # time.sleep(0.5)
    global header, cook

    cook=get_cookie()
    header ={
    'Referer': 'http://stockpage.10jqka.com.cn/HQ_v4.html',
    'User-Agent': random.choice(user_agent),
    'Cookie': 'v='+cook
     }
    # print(cook)
    # url='http://d.10jqka.com.cn/v6/line/hs_600196/21/all.js'
    con=requests.get(url, headers=header) 
    soup = BeautifulSoup(con.content.decode('gbk'),'lxml') 
    time.sleep(0.5)
    while (con.status_code != 200) or (len(re.findall(r'[^()]+', soup.text)) <= 1 ): 
        time.sleep(0.5)
       
        cook=get_cookie()
        # print(cook)
        header ={
        'Referer': 'http://stockpage.10jqka.com.cn/HQ_v4.html',
        'User-Agent': random.choice(user_agent),
        'Cookie': 'v='+cook
         }
        # print(header)
        time.sleep(0.5)
        print('------------------停--------------------')
        
        con=requests.get(url, headers=header)  
        soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
    # url='http://d.10jqka.com.cn/v6/line/hs_600196/21/all.js'
    # con=requests.get(url,headers=header)  
    # soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
    df=get_date(soup)
    return df

# 获取股票代码列表
code= pd.read_excel('Data20190311.xls',encoding='gbk')
# code = list(set(code))
listcode=code.code.tolist()
Code_List=[]
for item in listcode:
    if len(str(item)) == 6 and str(item)[0] == '6':
        Code_List.append('sh_'+str(item))
    if len(str(item)) < 6:
        Code_List.append('sz_'+(6-len(str(item)))*'0'+str(item))
    if len(str(item)) == 6 and str(item)[0] != '6':
        Code_List.append('sz_'+str(item))
code.code=pd.Series(Code_List)

dic={}

for code in Code_List:
    print('----------------'+str(code)+'------------------')
    df=get_df(url_month.format(str(code)))
    if df is not None:
        dic.update({str(code): df })

ds=xr.Dataset(dic)  
ds.to_netcdf('E:/stock_data/'+date+'_stock_price_month_saved.nc')


# http://d.10jqka.com.cn/v6/line/hs_000757/21/all.js