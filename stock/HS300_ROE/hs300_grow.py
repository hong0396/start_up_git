import tushare as ts
import pandas as pd
import time

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

hs300 = ts.get_hs300s()
sz50 = ts.get_sz50s()
basic = ts.get_stock_basics()


basic = basic.loc[:,['code','name','pb','pe','industry']]

hs300.describe()
print('ok1')

grow2017_4 = ts.get_growth_data(2017,4)
grow2017_3 = ts.get_growth_data(2017,3)
grow2017_2 = ts.get_growth_data(2017,2)
grow2017_1 = ts.get_growth_data(2017,1)


grow2017_4 = grow2017_4.loc[:,['code','name','mbrg','nprg','nav','targ']]
grow2017_3 = grow2017_3.loc[:,['code','name','mbrg','nprg','nav','targ']]
grow2017_2 = grow2017_2.loc[:,['code','name','mbrg','nprg','nav','targ']]
grow2017_1 = grow2017_1.loc[:,['code','name','mbrg','nprg','nav','targ']]
















roe2017_4 = ts.get_report_data(2017,4)
roe2017_3 = ts.get_report_data(2017,3)
roe2017_2 = ts.get_report_data(2017,2)
roe2017_1 = ts.get_report_data(2017,1)


roe2017_4 = roe2017_4.loc[:,['code','name','roe','bvps','net_profits']]
roe2017_3 = roe2017_3.loc[:,['code','name','roe','bvps','net_profits']]
roe2017_2 = roe2017_2.loc[:,['code','name','roe','bvps','net_profits']]
roe2017_1 = roe2017_1.loc[:,['code','name','roe','bvps','net_profits']]




hs300_2017_4=pd.merge(hs300,roe2017_4,on=['code','name'])
hs300_2017_3=pd.merge(hs300,roe2017_3,on=['code','name'])
hs300_2017_2=pd.merge(hs300,roe2017_2,on=['code','name'])
hs300_2017_1=pd.merge(hs300,roe2017_1,on=['code','name'])
print('ok3')



hs300_2017_4 = hs300_2017_4.loc[:,['code','name','roe','bvps','net_profits']]
hs300_2017_3 = hs300_2017_3.loc[:,['code','name','roe','bvps','net_profits']]
hs300_2017_2 = hs300_2017_2.loc[:,['code','name','roe','bvps','net_profits']]
hs300_2017_1 = hs300_2017_1.loc[:,['code','name','roe','bvps','net_profits']]



hs300_2017_4=hs300_2017_4.rename(index=str, columns={'roe' : 'roe_2017_4'})
hs300_2017_3=hs300_2017_3.rename(index=str, columns={'roe' : 'roe_2017_3'})
hs300_2017_2=hs300_2017_2.rename(index=str, columns={'roe' : 'roe_2017_2'})
hs300_2017_1=hs300_2017_1.rename(index=str, columns={'roe' : 'roe_2017_1'})


hs300_2017_4=hs300_2017_4.rename(index=str, columns={'bvps' : 'bvps_2017_4'})
hs300_2017_3=hs300_2017_3.rename(index=str, columns={'bvps' : 'bvps_2017_3'})
hs300_2017_2=hs300_2017_2.rename(index=str, columns={'bvps' : 'bvps_2017_2'})
hs300_2017_1=hs300_2017_1.rename(index=str, columns={'bvps' : 'bvps_2017_1'})


hs300_2017_4=hs300_2017_4.rename(index=str, columns={'net_profits' : 'net_profits_2017_4'})
hs300_2017_3=hs300_2017_3.rename(index=str, columns={'net_profits' : 'net_profits_2017_3'})
hs300_2017_2=hs300_2017_2.rename(index=str, columns={'net_profits' : 'net_profits_2017_2'})
hs300_2017_1=hs300_2017_1.rename(index=str, columns={'net_profits' : 'net_profits_2017_1'})




#print(hs300_2017_1)

temp1=pd.merge(hs300_2017_1, hs300_2017_2,how='outer', on=['code','name'])
#print(temp1)
temp2=pd.merge(hs300_2017_3, hs300_2017_4,how='outer', on=['code','name'])
#print(temp2)
roe=pd.merge(temp1,temp2,how='outer',on=['code','name'])

#print(roe)



print('ok5')
re=pd.merge(roe, basic, on='name')
re=re.drop_duplicates()
re.to_csv('D:/Git/stock/'+date+'_hs300_grow.csv')



