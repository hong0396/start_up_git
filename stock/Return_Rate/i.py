import time, datetime
import calendar
import pandas as pd
timeTuple = datetime.datetime.strptime("20180215", '%Y%m%d')




date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
first_day = datetime.date(timeTuple.year, timeTuple.month, 1)
pre_month = first_day - datetime.timedelta(days = 1)
first_day_of_pre_month = datetime.date(pre_month.year, pre_month.month, timeTuple.day)
print(timeTuple)
print(str(first_day_of_pre_month))





days_num = calendar.monthrange(first_day.year, first_day.month)[1]
first_day_of_next_month = timeTuple + datetime.timedelta(days = days_num)
print(str(first_day_of_next_month))




pp=pd.read_csv("result1.csv",encoding='gbk')
print(pp['bvps'].mean())
