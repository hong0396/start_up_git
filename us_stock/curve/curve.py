import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
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
'Authorization': 'Bearer gluCWKw06sXGLvRq1hsLaCd9vZRAUJ',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}



url='https://hq.itiger.com/stock_info/candle_stick/week/BIO?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'

con = requests.get(url, headers=header).json()
time.sleep(0.1)
li_data=con.get('items')
if li_data is not None:
    df=pd.DataFrame(li_data)
    


def gettime(tss1):
    return int(time.mktime(time.strptime(tss1, "%Y-%m-%d")))

x = df['time'].values
y = df['close'].values
z1 = np.polyfit(x, y, 4)#用3次多项式拟合
p1 = np.poly1d(z1)
print(p1) #在屏幕上打印拟合多项式
yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
der=p1.deriv(m=2)
dder=der(x)



dder_list = dder.tolist()
maxindex=dder_list.index(max(dder_list))
print(maxindex)
time_max=df['time'][maxindex]
close_max=df['close'][maxindex]

def getmax(x, y):
    return ABS(x-y)
# li=li.tolist()
# print(li)
# aa=pd.Series(li)
# aa.to_csv('tm.csv')
# print(list(map(lambda x,y: ABS(x-y), li,li)))

plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, 'r',label='polyfit values')
plt.annotate(' ', xy=(time_max, close_max), xytext=(time_max, close_max),arrowprops=dict(facecolor='red', shrink=0.05),)

# plot1=plt.plot(x, y, '*',label='original values')
# plot2=plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('polyfitting')
plt.show()
plt.savefig('p1.png')



