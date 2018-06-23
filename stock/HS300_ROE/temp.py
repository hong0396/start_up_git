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


