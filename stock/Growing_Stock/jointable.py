import tushare as ts
import pandas as pd
import time






def join_table(roe2017_2,roe2017_3,roe2017_4,roe2018_1,forcol)
    roe2017_4 = roe2017_4.loc[:,['code','name', forcol+'_201704']]
    roe2017_3 = roe2017_3.loc[:,['code','name', forcol+'_201703']]
    roe2017_2 = roe2017_2.loc[:,['code','name', forcol+'_201702']]
    roe2018_1 = roe2018_1.loc[:,['code','name', forcol+'_201801']]

    temp1=pd.merge(roe2017_2, roe2017_3,how='outer', on=['code','name'])
    temp2=pd.merge(roe2017_4, roe2018_1,how='outer', on=['code','name'])
    roe=pd.merge(temp1,temp2,how='outer',on=['code','name'])
    roe = roe[ ~ roe['name'].str.contains('ST') ]
    roe = roe[ ~ roe['name'].str.contains('退市')]
    roe = roe[ ~ roe['name'].str.contains('XD')]
    roe = roe[ ~ roe['name'].str.contains('DR')]
    roe = roe.drop_duplicates()
    return roe



