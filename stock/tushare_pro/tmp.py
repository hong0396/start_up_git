import tushare as ts

ts.set_token('f0bc92493f465175869d33171cddc83dd902fa77208342813a2245e4')
pro = ts.pro_api()
# df1 = pro.trade_cal(exchange_id='', start_date='20180101', end_date='', fields='pretrade_date', is_open='0')
# df2 = pro.query('trade_cal', exchange_id='', start_date='20180101', end_date='', fields='pretrade_date', is_open='0')
df = pro.fina_indicator(ts_code='600000.SH', start_date='20180101', end_date='20180820')
df = pro.income(ts_code='600000.SH', start_date='20180101', end_date='20180730')
# df = pro.query('fina_indicator', start_date='20180101', end_date='20180820')
print(df)
df.to_csv('tmp.csv',  encoding = 'gbk', index=False)

