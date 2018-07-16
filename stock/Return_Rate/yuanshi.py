
import tushare as ts
import pandas as pd
import time
import time, datetime
import calendar
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
df = ts.get_stock_basics()
# date = df.ix['600848']['timeToMarket']
# da= df.iloc(:,['code', 'name'])
code=df.index.tolist()
name=df['name'].tolist()
bvps=df['bvps'].tolist()
timeToMarket=df['timeToMarket'].tolist()
# print(len(code))
# print(len(name))
# print(len(bvps))
a=[]
a.append(code)
a.append(name)
a.append(bvps)
a.append(timeToMarket)
dd=pd.DataFrame(a)
# print(dd.T)
dff=dd.T
dff.columns=["code","name","bvps","timeToMarket"]
# df_li=dff.values.tolist()
# print(df_li)
li=[]
for row in dff.itertuples():
    print("--------------------------------------"+row[1]+"-------------------------------------------")
    litmp=[]
    
    # timeTuple = datetime.datetime.strptime(str(row[4]), '%Y%m%d')
    # first_day = datetime.date(timeTuple.year, timeTuple.month, 1)
    # days_num = calendar.monthrange(first_day.year, first_day.month)[1]
    # first_day_of_next_month = timeTuple + datetime.timedelta(days = days_num)
    tmp=ts.get_hist_data(row[1], ktype='M')
    
    # timeTuple = datetime.datetime.strptime(str(date)[:10], '%Y-%m-%d')
    # first_day = datetime.date(timeTuple.year, timeTuple.month, 1)
    # pre_month = first_day - datetime.timedelta(days = 1)
    # first_day_of_pre_month = datetime.date(pre_month.year, pre_month.month, timeTuple.day)

    # tmp_end=ts.get_h_data(row[1],start=str(first_day_of_pre_month)[:10], end=str(date)[:10])



    # print(tmp)
    if not tmp_per is  None:
    # if not tmp.empty:
        if tmp.values.any():
        # if not tmp_end is  None:
            index=tmp.index.tolist()
            first=tmp.ix[index[0],'close']
            last=tmp.ix[index[-1],'close']
            # first=tmp_per['close'].mean()
            # last=tmp_end['close'].mean()
            grow=(last-first)/first
            litmp.append(first)
            litmp.append(last)
            litmp.append(grow)
            li.append(litmp)
print(li)
pd_li=pd.DataFrame(li)
result = pd.concat([dff, pd_li], axis=1)
result.to_csv(date+'result1.csv', encoding='gbk')
