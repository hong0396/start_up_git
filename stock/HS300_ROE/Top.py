import tushare as ts
import time


date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

top=ts.top_list('2018-04-20')

print(top)




