import tushare as ts
import time

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

li=ts.get_today_all()

li.to_excel('D:/Git/stock/pb/'+date+'_pb.xlsx')