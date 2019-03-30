import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool,freeze_support
import traceback,time,re
import pandas as pd
import xarray as xr
def get_soup(soup):
	date =[]
	open  =[]
	close =[]
	high  =[]
	low  =[]
	volumn =[]
	aa=soup.text.replace('monthly_data=','').replace('"','').replace(';','')
	bb=aa.replace("\\",'')
	for i in bb.split('n'):
		if i.strip().replace("\n",""):
			j = i.strip().replace("\n","").split(" ")
			# print(j)
			if len(j) == 6:
				date.append(j[0])
				open.append(j[1])
				close.append(j[2])
				high.append(j[3])
				low.append(j[4])
				volumn.append(j[5])
	df=pd.DataFrame({'date':date,"open":open, "close":close, "low":low,"high":high})
	return df








# http://data.gtimg.cn/flashdata/hushen/latest/daily/sz000002.js?maxage=43201
# http://data.gtimg.cn/flashdata/hushen/latest/weekly/sz000002.js?maxage=43201
# http://data.gtimg.cn/flashdata/hushen/latest/monthly/sz000002.js?maxage=43201
url_month = 'http://data.gtimg.cn/flashdata/hushen/monthly/{}.js?maxage=43201'
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
def get_data(url) :
	time.sleep(0.3)
	con=requests.get(url)
	soup = BeautifulSoup(con.content.decode('gbk'),'lxml') 
	# print(get_soup(soup))
	return get_soup(soup)

# 获取股票代码列表
code= pd.read_excel('Data20190311.xls',encoding='gbk')
# code = list(set(code))
listcode=code.code.tolist()
Code_List=[]
for item in listcode:
    if len(str(item)) == 6 and str(item)[0] == '6':
        Code_List.append('sh'+str(item))
    if len(str(item)) < 6:
        Code_List.append('sz'+(6-len(str(item)))*'0'+str(item))
    if len(str(item)) == 6 and str(item)[0] != '6':
        Code_List.append('sz'+str(item))
code.code=pd.Series(Code_List)

dic={}
for code in Code_List:
    print('----------------'+str(code)+'------------------')
    df=get_data(url_month.format(str(code)))
    if df is not None:
        dic.update({str(code): df })

ds=xr.Dataset(dic)  
ds.to_netcdf('E:/stock_data/'+date+'_stock_price_month_saved.nc')






