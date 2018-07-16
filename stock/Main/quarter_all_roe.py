import tushare as ts
import pandas as pd
import time
from functools import *

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))





roe2018_1 = ts.get_profit_data(2018,1)
roe2017_4 = ts.get_profit_data(2017,4)
roe2017_3 = ts.get_profit_data(2017,3)
roe2017_2 = ts.get_profit_data(2017,2)
roe2017_1 = ts.get_profit_data(2017,1)
roe2016_4 = ts.get_profit_data(2016,4)
roe2016_3 = ts.get_profit_data(2016,3)
roe2016_2 = ts.get_profit_data(2016,2)


li=[]
li=[roe2016_2, roe2016_3, roe2016_4, roe2017_1, roe2017_2, roe2017_3, roe2017_4,  roe2018_1]

for i in range(len(li)):
	li[i]['name']= li[i]['name'].map(str.strip)
    li[i] = li[i][ ~ li[i]['name'].str.contains('ST','退市') ]


def df_join_nm(pd_li,col,rename):
    for i in range(len(pd_li)):
        pd_li[i]=pd_li[i].loc[:,col]
        for j in range(len(col[1:])):
            pd_li[i].rename(columns={col[1:][j]:rename[i]}, inplace = True)       	
    tmp=reduce(lambda x, y:pd.merge(x,y,how='outer',on=col[0]), pd_li)
    tmp = tmp.drop_duplicates()
    return tmp




rename=['roe2016_2','roe2016_3','roe2016_4','roe2017_1','roe2017_2','roe2017_3','roe2017_4','roe2018_1']
roe=df_join_nm(li, ['name', 'roe'], rename)


basic = ts.get_stock_basics()
basic['name']= basic['name'].map(str.strip)
basic['name']= basic['name'].str.replace(' ', '')
basic['name']= basic['name'].str.replace('Ａ', 'A')
basic['name']= basic['name'].map(str.strip)
basic = basic[ ~ basic['name'].str.contains('ST') ]
basic = basic[ ~ basic['name'].str.contains('退市')]



re=pd.merge(roe,basic,how='outer',on='name')


re.to_csv(date+'_quarter_all_roe.csv',  encoding = 'gbk', index=False)

