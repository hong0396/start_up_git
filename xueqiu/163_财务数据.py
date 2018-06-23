import tushare as ts
import pandas as pd
import time
import requests
import json
import random
import ast

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

hs300 = ts.get_hs300s()

#print(hs300)


#df = pd.read_html('https://xueqiu.com/S/SZ300072/ZYCWZB')


df = pd.read_html('http://quotes.money.163.com/f10/zycwzb_600004.html#01c01')
rep1=df[4].T
col=['日期']+list(df[3].iloc[:,0])
rep1.columns=col
rep1=rep1.T

rep1.to_csv("a.csv")


print(df[3])
