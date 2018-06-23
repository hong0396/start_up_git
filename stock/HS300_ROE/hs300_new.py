import tushare as ts
import pandas as pd
import time

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

hs300 = ts.get_hs300s()
##sz50 = ts.get_sz50s()

basic = ts.get_stock_basics()
basic = basic.loc[:,['code','name','pb','pe','industry']]
print('ok1')
#time.sleep(5)
roe2017_4 = ts.get_report_data(2017,4)
#time.sleep(5)
roe2017_3 = ts.get_report_data(2017,3)
#time.sleep(5)
roe2017_2 = ts.get_report_data(2017,2)
#time.sleep(5)
roe2017_1 = ts.get_report_data(2017,1)



#print(roe2017_3)

roe2017_4 = roe2017_4.loc[:,['code','name','roe','bvps']]
roe2017_3 = roe2017_3.loc[:,['code','name','roe','bvps']]
roe2017_2 = roe2017_2.loc[:,['code','name','roe','bvps']]
roe2017_1 = roe2017_1.loc[:,['code','name','roe','bvps']]

print(roe2017_1)


hs300_2017_4=pd.merge(hs300,roe2017_4,on=['code','name'])
hs300_2017_3=pd.merge(hs300,roe2017_3,on=['code','name'])
hs300_2017_2=pd.merge(hs300,roe2017_2,on=['code','name'])
hs300_2017_1=pd.merge(hs300,roe2017_1,on=['code','name'])
print('ok3')



hs300_2017_4 = hs300_2017_4.loc[:,['code','name','roe','bvps']]
hs300_2017_3 = hs300_2017_3.loc[:,['code','name','roe','bvps']]
hs300_2017_2 = hs300_2017_2.loc[:,['code','name','roe','bvps']]
hs300_2017_1 = hs300_2017_1.loc[:,['code','name','roe','bvps']]



hs300_2017_4=hs300_2017_4.rename(index=str, columns={'roe' : 'roe_2017_4'})
hs300_2017_3=hs300_2017_3.rename(index=str, columns={'roe' : 'roe_2017_3'})
hs300_2017_2=hs300_2017_2.rename(index=str, columns={'roe' : 'roe_2017_2'})
hs300_2017_1=hs300_2017_1.rename(index=str, columns={'roe' : 'roe_2017_1'})


hs300_2017_4=hs300_2017_4.rename(index=str, columns={'bvps' : 'bvps_2017_4'})
hs300_2017_3=hs300_2017_3.rename(index=str, columns={'bvps' : 'bvps_2017_3'})
hs300_2017_2=hs300_2017_2.rename(index=str, columns={'bvps' : 'bvps_2017_2'})
hs300_2017_1=hs300_2017_1.rename(index=str, columns={'bvps' : 'bvps_2017_1'})

print(hs300_2017_1)

temp1=pd.merge(hs300_2017_1, hs300_2017_2,how='outer', on=['code','name'])
#print(temp1)
temp2=pd.merge(hs300_2017_3, hs300_2017_4,how='outer', on=['code','name'])
#print(temp2)
roe=pd.merge(temp1,temp2,how='outer',on=['code','name'])



print(roe)

print('ok5')
re=pd.merge(roe, basic, on='name')
re=re.drop_duplicates()
re.to_excel('D:/Git/stock/'+date+'_hs300_new.xlsx')






