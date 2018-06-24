import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
import stock_code as sc
from functools import reduce
#总网址
#http://emweb.securities.eastmoney.com/f10_v2/FinanceAnalysis.aspx?type=web&code=sz300612#dbfx-0


# all=ts.get_stock_basics()
# listcode=all.index.tolist()
# print(listcode)

# 获取股票代码列表
code=sc.tu_code_fore()
code = list(set(code))
#print(code)
my_headers = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
# header={"User-Agent":random.choice(my_headers)}
header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
# http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?ctype=4&type=0&code=sz300612
# url='http://emweb.securities.eastmoney.com/NewFinanceAnalysis/DubangAnalysisAjax?code=sz300612'
url='http://emweb.securities.eastmoney.com/NewFinanceAnalysis/DubangAnalysisAjax?code={}'
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
num=0
ab=pd.DataFrame()
pd_list=[]
for i in code:
    time.sleep(0.2)
    con = requests.get(url.format(i), headers=header).content
    a = str(con.decode())
    num=num+1
    print("----------------------------------------"+str(num)+"---"+i+"--------------------------------------------------------")
    li= []
    dic = json.loads(a)
    #dic=ast.literal_eval(a)
    year_du=dic.get('nd')
    for year in year_du:
        tmp=[]
        date =year.get('date')
        roe =year.get('jzcsyl')
        # lrl =year.get('yyjlrl')
        # zz =year.get('zzczzl')
        # fz =year.get('zcfzl')
        tmp.append('roe_'+date)
        tmp.append(roe)
        li.append(tmp)
    for year in year_du:
        tmp=[]
        date =year.get('date')
        # roe =year.get('jzcsyl')
        # lrl =year.get('yyjlrl')
        # zz =year.get('zzczzl')
        fz =year.get('zcfzl')
        tmp.append('fz_'+date)
        tmp.append(fz)
        li.append(tmp)
    for year in year_du:
        tmp=[]
        date =year.get('date')
        # roe =year.get('jzcsyl')
        # lrl =year.get('yyjlrl')
        zz =year.get('zzczzl')
        # fz =year.get('zcfzl')
        tmp.append('zz_'+date)
        tmp.append(zz)
        li.append(tmp)
    for year in year_du:
        tmp=[]
        date =year.get('date')
        # roe =year.get('jzcsyl')
        lrl =year.get('yyjlrl')
        # zz =year.get('zzczzl')
        # fz =year.get('zcfzl')
        tmp.append('lrl_'+date)
        tmp.append(lrl)
        li.append(tmp)

    zz=list(zip(*li))
    #print(zz)
    zz=[ [row[col] for row in li] for col in range(len(list(max(li))))] 
    #print(zz)
    pd_roe=pd.DataFrame(zz, columns=zz[0], index=[0, i])
    pd_roe=pd_roe.drop(0, axis=0)
    pd_roe = pd_roe.loc[:,~pd_roe.columns.duplicated()]
    pd_list.append(pd_roe)
    # print(pd_roe)
    ab=ab.append(pd_roe)
# def f(x, y):
#     z=pd.concat([x,y])
#     return z
# zong=reduce(f, pd_list)
#print(zong)
# zong=pd.concat(pd_list)
zong=ab
t = zong.loc[:,~zong.columns.duplicated()]
# t=zong.drop(0,axis=0)
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
t.to_csv(date+'_year_all_roe.csv')
print(t)