import baostock as bs
import pandas as pd
import tushare as ts


df = ts.get_stock_basics()
df = df[ ~ df['name'].str.contains('ST') ]
df = df[ ~ df['name'].str.contains('退市')]
# df = df[df['timeToMarket']<20180101 ]
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

for i in dff["code"].index:
	if(str(dff.ix[i, "code"])[:2]=='60'):
	    dff.ix[i, "code"]='sh.'+str(dff.ix[i, "code"])
	else:
		dff.ix[i, "code"]='sz.'+str(dff.ix[i, "code"])
	# print(str(dff.ix[i, "code"]))








#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节



rs = bs.query_history_k_data("sh.000581",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2014-01-01', end_date='2014-02-01',
    frequency="d", adjustflag="2")

print(type(rs))


print('query_history_k_data respond error_code:'+rs.error_code)
print('query_history_k_data respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

#### 结果集输出到csv文件 ####   
# result.to_csv("history_A_stock_k_data.csv", index=False)
print(result)

#### 登出系统 ####
bs.logout()