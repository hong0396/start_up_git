import tushare as ts

ts.set_token('f0bc92493f465175869d33171cddc83dd902fa77208342813a2245e4')
pro = ts.pro_api()

data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data.to_csv('code.csv',  encoding = 'gbk', index=False)
df = pro.weekly(ts_code='600000.SH', start_date='20180101',  fields='ts_code,trade_date,open,high,low,close,vol,amount')
print(df)

