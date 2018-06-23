import tushare as ts
import pandas as pd
import time

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

hs300 = ts.get_hs300s()
sz50 = ts.get_sz50s()
basic = ts.get_stock_basics()

hs300.describe()
print('ok1')

#获取2017年四季度的roe数据
roe2017_4 = ts.get_profit_data(2017,4)
roe2017_3 = ts.get_profit_data(2017,3)
roe2017_2 = ts.get_profit_data(2017,2)
roe2017_1 = ts.get_profit_data(2017,1)

#获取2016年四季度的roe数据
roe2016_4 = ts.get_profit_data(2016,4)
roe2016_3 = ts.get_profit_data(2016,3)
roe2016_2 = ts.get_profit_data(2016,2)
roe2016_1 = ts.get_profit_data(2016,1)

#获取2017年四季度的roe数据（只取三列）
roe2017_4 = roe2017_4.loc[:,['code','name','roe']]
roe2017_3 = roe2017_3.loc[:,['code','name','roe']]
roe2017_2 = roe2017_2.loc[:,['code','name','roe']]
roe2017_1 = roe2017_1.loc[:,['code','name','roe']]

#获取2016年四季度的roe数据（只取三列）
roe2016_4 = roe2016_4.loc[:,['code','name','roe']]
roe2016_3 = roe2016_3.loc[:,['code','name','roe']]
roe2016_2 = roe2016_2.loc[:,['code','name','roe']]
roe2016_1 = roe2016_1.loc[:,['code','name','roe']]


#获取2017年四季度的roe数据（只取三列）（只选取hs300的股票）
hs300_2017_4=pd.merge(hs300,roe2017_4,on=['code','name'])
hs300_2017_3=pd.merge(hs300,roe2017_3,on=['code','name'])
hs300_2017_2=pd.merge(hs300,roe2017_2,on=['code','name'])
hs300_2017_1=pd.merge(hs300,roe2017_1,on=['code','name'])

#获取2016年四季度的roe数据（只取三列）（只选取hs300的股票）
hs300_2016_4=pd.merge(hs300,roe2016_4,on=['code','name'])
hs300_2016_3=pd.merge(hs300,roe2016_3,on=['code','name'])
hs300_2016_2=pd.merge(hs300,roe2016_2,on=['code','name'])
hs300_2016_1=pd.merge(hs300,roe2016_1,on=['code','name'])


print('ok3')



hs300_2017_4 = hs300_2017_4.loc[:,['code','name','roe']]
hs300_2017_3 = hs300_2017_3.loc[:,['code','name','roe']]
hs300_2017_2 = hs300_2017_2.loc[:,['code','name','roe']]
hs300_2017_1 = hs300_2017_1.loc[:,['code','name','roe']]


hs300_2016_4 = hs300_2016_4.loc[:,['code','name','roe']]
hs300_2016_3 = hs300_2016_3.loc[:,['code','name','roe']]
hs300_2016_2 = hs300_2016_2.loc[:,['code','name','roe']]
hs300_2016_1 = hs300_2016_1.loc[:,['code','name','roe']]


#更改列名
hs300_2017_4=hs300_2017_4.rename(index=str, columns={'roe' : 'roe_2017_4'})
hs300_2017_3=hs300_2017_3.rename(index=str, columns={'roe' : 'roe_2017_3'})
hs300_2017_2=hs300_2017_2.rename(index=str, columns={'roe' : 'roe_2017_2'})
hs300_2017_1=hs300_2017_1.rename(index=str, columns={'roe' : 'roe_2017_1'})


hs300_2016_4=hs300_2016_4.rename(index=str, columns={'roe' : 'roe_2016_4'})
hs300_2016_3=hs300_2016_3.rename(index=str, columns={'roe' : 'roe_2016_3'})
hs300_2016_2=hs300_2016_2.rename(index=str, columns={'roe' : 'roe_2016_2'})
hs300_2016_1=hs300_2016_1.rename(index=str, columns={'roe' : 'roe_2016_1'})


temp1_2016=pd.merge(hs300_2016_1, hs300_2016_2,how='outer', on=['code','name'])
temp2_2016=pd.merge(hs300_2016_3, hs300_2016_4,how='outer', on=['code','name'])
roe_2016=pd.merge(temp1_2016,temp2_2016,how='outer',on=['code','name'])



temp1_2017=pd.merge(hs300_2017_1, hs300_2017_2,how='outer', on=['code','name'])
temp2_2017=pd.merge(hs300_2017_3, hs300_2017_4,how='outer', on=['code','name'])
roe_2017=pd.merge(temp1_2017,temp2_2017,how='outer',on=['code','name'])


roe=pd.merge(roe_2016,roe_2017,how='outer',on=['code','name'])



print('ok5')


re=pd.merge(roe, basic, on='name')
re=re.drop_duplicates()
re.to_excel('D:/Git/stock/hs300/'+date+'_hs300_two.xlsx')






