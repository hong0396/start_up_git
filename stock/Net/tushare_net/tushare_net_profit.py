import tushare as ts
import pandas as pd
import time
from functools import *

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

hs300 = ts.get_hs300s()
# sz50 = ts.get_sz50s()
basic = ts.get_stock_basics()
# basic = basic.loc[:,['code','name','pb','pe','industry']]
basic['name']= basic['name'].map(str.strip)
basic['name']= basic['name'].str.replace(' ', '')
basic['name']= basic['name'].str.replace('Ａ', 'A')
basic['name']= basic['name'].map(str.strip)
#除去含义ST的股票
basic = basic[ ~ basic['name'].str.contains('ST') ]
basic = basic[ ~ basic['name'].str.contains('退市')]

hs300.describe()
print('ok1')


roe2017_4 = ts.get_profit_data(2017,4)
roe2017_3 = ts.get_profit_data(2017,3)
roe2017_2 = ts.get_profit_data(2017,2)
roe2017_1 = ts.get_profit_data(2017,1)
roe2018_1 = ts.get_profit_data(2018,1)
# roe2017_4.to_csv(date+'_net_profits201704.csv',  encoding = 'gbk', index=False)


# print(roe2017_4.columns)
li=[]
li=[roe2017_1, roe2017_2, roe2017_3, roe2017_4, roe2018_1]


def df_join(pd_li,col):
    for i in range(len(pd_li)):
        pd_li[i]=pd_li[i].loc[:,col]
        for j in range(len(col[1:])):
            pd_li[i].rename(columns={col[1:][j]:col[1:][j]+str(i)}, inplace = True)       	
    tmp=reduce(lambda x, y:pd.merge(x,y,how='outer',on=col[0]), pd_li)
    tmp = tmp.drop_duplicates()
    return tmp

def df_join_nm(pd_li,col,rename):
    for i in range(len(pd_li)):
        pd_li[i]=pd_li[i].loc[:,col]
        for j in range(len(col[1:])):
            pd_li[i].rename(columns={col[1:][j]:rename[i]}, inplace = True)       	
    tmp=reduce(lambda x, y:pd.merge(x,y,how='outer',on=col[0]), pd_li)
    tmp = tmp.drop_duplicates()
    return tmp


rename=['net2017_1','net2017_2','net2017_3','net2017_4','net2018_1']
net=df_join_nm(li, ['code', 'net_profits'], rename)

re=pd.merge(net,basic, how='inner',on='code')
re.to_csv(date+'_all_net_profits.csv',  encoding = 'gbk', index=False)































# roe2017_4 = roe2017_4.loc[:,['code','name','roe','bvps','net_profits']]
# roe2017_3 = roe2017_3.loc[:,['code','name','roe','bvps','net_profits']]
# roe2017_2 = roe2017_2.loc[:,['code','name','roe','bvps','net_profits']]
# roe2017_1 = roe2017_1.loc[:,['code','name','roe','bvps','net_profits']]

# profits_yoy




# net2017_4 = roe2017_4.loc[:,['code','name','net_profits']]
# net2017_3 = roe2017_3.loc[:,['code','name','net_profits']]
# net2017_2 = roe2017_2.loc[:,['code','name','net_profits']]
# net2017_1 = roe2017_1.loc[:,['code','name','net_profits']]
# net=pd.merge(net2017_2,net2017_4,how='outer',on='code')


# hs300_2017_4=pd.merge(hs300,roe2017_4,on=['code','name'])
# hs300_2017_3=pd.merge(hs300,roe2017_3,on=['code','name'])
# hs300_2017_2=pd.merge(hs300,roe2017_2,on=['code','name'])
# hs300_2017_1=pd.merge(hs300,roe2017_1,on=['code','name'])
# print('ok3')



# hs300_2017_4 = hs300_2017_4.loc[:,['code','name','roe','bvps','net_profits']]
# hs300_2017_3 = hs300_2017_3.loc[:,['code','name','roe','bvps','net_profits']]
# hs300_2017_2 = hs300_2017_2.loc[:,['code','name','roe','bvps','net_profits']]
# hs300_2017_1 = hs300_2017_1.loc[:,['code','name','roe','bvps','net_profits']]



# hs300_2017_4=hs300_2017_4.rename(index=str, columns={'roe' : 'roe_2017_4'})
# hs300_2017_3=hs300_2017_3.rename(index=str, columns={'roe' : 'roe_2017_3'})
# hs300_2017_2=hs300_2017_2.rename(index=str, columns={'roe' : 'roe_2017_2'})
# hs300_2017_1=hs300_2017_1.rename(index=str, columns={'roe' : 'roe_2017_1'})


# hs300_2017_4=hs300_2017_4.rename(index=str, columns={'bvps' : 'bvps_2017_4'})
# hs300_2017_3=hs300_2017_3.rename(index=str, columns={'bvps' : 'bvps_2017_3'})
# hs300_2017_2=hs300_2017_2.rename(index=str, columns={'bvps' : 'bvps_2017_2'})
# hs300_2017_1=hs300_2017_1.rename(index=str, columns={'bvps' : 'bvps_2017_1'})


# hs300_2017_4=hs300_2017_4.rename(index=str, columns={'net_profits' : 'net_profits_2017_4'})
# hs300_2017_3=hs300_2017_3.rename(index=str, columns={'net_profits' : 'net_profits_2017_3'})
# hs300_2017_2=hs300_2017_2.rename(index=str, columns={'net_profits' : 'net_profits_2017_2'})
# hs300_2017_1=hs300_2017_1.rename(index=str, columns={'net_profits' : 'net_profits_2017_1'})




# #print(hs300_2017_1)

# temp1=pd.merge(hs300_2017_1, hs300_2017_2,how='outer', on=['code','name'])
# #print(temp1)
# temp2=pd.merge(hs300_2017_3, hs300_2017_4,how='outer', on=['code','name'])
# #print(temp2)
# roe=pd.merge(temp1,temp2,how='outer',on=['code','name'])

# #print(roe)



# print('ok5')
# re=pd.merge(roe, basic, on='name')
# re=re.drop_duplicates()
# re.to_csv('D:/Git/stock/'+date+'_hs300_grow.csv', encoding='gbk')



