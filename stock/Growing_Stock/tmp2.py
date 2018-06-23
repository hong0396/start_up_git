import tushare as ts
import pandas as pd
import numpy as np
import time
import math

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))


all_data=ts.get_stock_basics()


all_data = all_data.drop_duplicates()  
all_data['name']= all_data['name'].str.replace(r'*', 'ST')
indexs = list(all_data[(all_data['name'].str.contains('ST', na=False))|(all_data['name'].str.contains('退市', na=False))].index)
all_data = all_data.drop(indexs)
#all_data=all_data[all_data['name'].str.contains(r'*', na=False)]
all_data=all_data[all_data['pe']>0]
all_data=all_data[all_data['pb']>0]
all_data['name']= all_data['name'].map(str.strip)


all_data.to_csv(date+'basic_data.csv')


# small_data=all_data[all_data['mktcap']<1000000]

