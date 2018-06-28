import urllib.request
import re
import time
import requests
import csv
import pandas as pd
from sqlalchemy import create_engine
# import pymysql
import random
from  bs4 import BeautifulSoup

header={'Host': 'quotes.money.163.com',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'ser-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'Province=021; City=021; UM_distinctid=15bfcbf263fa27-0d18b021b5dd1f-541a301f-100200-15bfcbf2640575; vjuids=-3f64a0445.15bfcbf2943.0.c0b020852df6d; _ntes_nnid=fc5b23d9b9f1dda9ae52d8c81a08529f,1494594038099; _ntes_nuid=fc5b23d9b9f1dda9ae52d8c81a08529f; usertrack=c+5+hVkV7kStRHqRA8MdAg==; _ga=GA1.2.163554575.1494609469; _gid=GA1.2.19604338.1494609469; ne_analysis_trace_id=1494683090432; _ntes_stock_recent_=0600000%7C0603180%7C0601857%7C1000627%7C0600004; _ntes_stock_recent_=0600000%7C0603180%7C0601857%7C1000627%7C0600004; _ntes_stock_recent_=0600000%7C0603180%7C0601857%7C1000627%7C0600004; NE_DANMAKU_USERID=353d1; vjlast=1494594038.1494605991.13; vinfo_n_f_l_n3=0c74f13321747664.1.4.1494594038107.1494683899963.1494690827745; s_n_f_l_n3=0c74f133217476641494687558835'
}



url = 'http://quotes.money.163.com/usstock/SEE_indicators.html?type=quarter'
current = time.strftime("%Y%m%d")


df = pd.read_html(url)
#df.to_excel("a.xlsx")

#df.to_csv()
#print(df)
res=requests.get(url, headers=header)
pdf=res.text
soup = BeautifulSoup(res.content, 'lxml')
#container
sou=soup.select('.liabilities_list')
sou=sou[0]
title=sou.select('.list_title')
title=title[0]
title=title.find_all('li')
date=sou.select('.list_table')
date=date[0]
date=date.find_all('li')
tr=sou.find_all('tr')
column=[]
for i in title[1:]:
    #print(i.text)
    column.append(i.text)
print(column)
dat=[]
for i in date:
    #print(i.text)
    dat.append(i.text)
print(dat)

datt=[]
for j in tr:
    tem=[]
    td=j.find_all('td')
    for k in td:
        if k.text:
            tem.append(k.text)
        else:
            tem.append(' ')
    datt.append(tem)
print(datt)
sum=pd.DataFrame(datt)
sumt=sum.T
sumt.columns = column
sums=sumt.T
sums.columns = dat
print(sums)
sums.to_csv("US.csv")
