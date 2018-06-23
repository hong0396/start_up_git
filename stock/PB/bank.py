import tushare as ts
import pandas as pd
import numpy as np
import time
import math

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

basic = ts.get_stock_basics()
basic['name']= basic['name'].map(str.strip)
basic['name']= basic['name'].str.replace(' ', '')
basic['name']= basic['name'].str.replace('Ａ', 'A')
basic['name']= basic['name'].map(str.strip)


bank=basic[basic['industry'] == '银行']
bank['esp'].astype(float)
bank['bvps'].astype(float)
pb=np.array(bank['pb']).astype(np.float64)
esp=np.array(bank['esp']).astype(np.float64)
bvps=np.array(bank['bvps']).astype(np.float64)
su=esp/bvps
su=su.tolist()
pb=pb.tolist()
year_two=[]
if  len(pb) == len(su):
    for i in range(len(pb)):
        temp=math.log(pb[i]*2, su[i]+1)
        year_two.append(temp)
else:
    print('列数错误')


#print(year_two)
bank.insert(len(bank.columns),'收益率',su)
bank.insert(len(bank.columns),'两倍收益率年数',year_two)



#bank['2pei_year'] = math.log(bank['pb']*2,  bank['收益率']+1)

print(bank)

bank.to_excel(date+'_bank.xlsx', index=False)



