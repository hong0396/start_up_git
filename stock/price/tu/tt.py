import tushare as ts
import sqlite3
import pandas as pd

con = sqlite3.connect('test.db')
conn = sqlite3.connect('D:\\Git\\stock\\price\\163\\test.db')
aa=pd.read_sql_query('select * from stockcode', con=conn)
aa.reset_index(drop = True)
li=aa.copy()
for index, i in aa.iterrows():
    print(i["stockcode"])
    if i["stockcode"]:
        t=ts.get_hist_data(str(i["stockcode"]), ktype='W')
        # print(t)
    if t is not None:
        t.to_sql(i["stockcode"], con=con, if_exists='replace')
    