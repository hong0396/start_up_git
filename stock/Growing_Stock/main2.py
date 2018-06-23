import tushare as ts
import pandas as pd
import time
# import jointable

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))


basic = ts.get_stock_basics()
basic['name']= basic['name'].map(str.strip)
basic['name']= basic['name'].str.replace(' ', '')
basic['name']= basic['name'].str.replace('Ａ', 'A')
basic['name']= basic['name'].map(str.strip)
#除去含义ST的股票
basic = basic[ ~ basic['name'].str.contains('ST') ]
basic = basic[ ~ basic['name'].str.contains('退市')]
basic = basic[ ~ basic['name'].str.contains('XD')]
basic = basic[ ~ basic['name'].str.contains('DR')]



roe2018_1 = ts.get_profit_data(2018,1)
roe2017_4 = ts.get_profit_data(2017,4)
roe2016_4 = ts.get_profit_data(2016,4)
roe2015_4 = ts.get_profit_data(2015,4)
roe2014_4 = ts.get_profit_data(2014,4)

# col=roe2018_1.columns.values.tolist()
# col.remove('code')
# col.remove('name')

#df1.dropna(how='any')
#df1.fillna(value=5)


roe2018_1=roe2018_1[roe2018_1>0]
roe2017_4=roe2017_1[roe2017_1>0]
roe2016_4=roe2016_4[roe2016_4>0]
roe2015_4=roe2015_4[roe2015_4>0]
roe2014_4=roe2014_4[roe2014_4>0]



# roe2018_1=roe2018_1[roe2018_1.iloc[:,2:]>0]
# roe2017_2=roe2017_2[roe2017_2.iloc[:,2:]>0]
# roe2017_3=roe2017_3[roe2017_3.iloc[:,2:]>0]
# roe2017_4=roe2017_4[roe2017_4.iloc[:,2:]>0]

# roe2017_1 = ts.get_profit_data(2017,1)
# roe2017_1.rename(columns={"esp":"每股收益_201701","eps_yoy":"每股收益同比(%)_201701",
# 	"bvps":"每股净资产_201701","roe":"净资产收益率(%)_201701","epcf":"每股现金流量(元)_201701",
# 	"net_profits":"净利润(万元)_201701",
# 	"profits_yoy":"净利润同比(%)_201701","distrib":"分配方案_201701"}, inplace = True)





roe2017_4.rename(columns={"roe":"roe_2017","net_profit_ratio":"净利率(%)_2017",
	"gross_profit_rate":"毛利率(%)_2017","net_profits":"净利润(万元)_2017",
	"eps":"每股收益_2017","business_income":"营业收入(百万元)_2017","bips":"每股主营业务收入(元)_2017"}, inplace = True)

roe2016_4.rename(columns={"roe":"roe_2016","net_profit_ratio":"净利率(%)_2016",
	"gross_profit_rate":"毛利率(%)_2016","net_profits":"净利润(万元)_2016",
	"eps":"每股收益_2016","business_income":"营业收入(百万元)_2016","bips":"每股主营业务收入(元)_2016"}, inplace = True)

roe2015_4.rename(columns={"roe":"roe_2015",
	"net_profit_ratio":"净利率(%)_2015","gross_profit_rate":"毛利率(%)_2015",
	"net_profits":"净利润(万元)_2015","eps":"每股收益_2015",
	"business_income":"营业收入(百万元)_2015","bips":"每股主营业务收入(元)_2015"}, inplace = True)

roe2014_4.rename(columns={"roe":"roe_2014","net_profit_ratio":"净利率(%)_2014",
	"gross_profit_rate":"毛利率(%)_2014","net_profits":"净利润(万元)_2014",
	"eps":"每股收益_2014","business_income":"营业收入(百万元)_2014","bips":"每股主营业务收入(元)_2014"}, inplace = True)

roe2018_1.rename(columns={"roe":"roe_201801","net_profit_ratio":"净利率(%)_201801",
	"gross_profit_rate":"毛利率(%)_201801","net_profits":"净利润(万元)_201801",
	"eps":"每股收益_201801","business_income":"营业收入(百万元)_201801","bips":"每股主营业务收入(元)_201801"}, inplace = True)




roe2017_4 = roe2017_4.loc[:,['code','name','roe_2017']]
roe2016_4 = roe2016_4.loc[:,['code','name','roe_2016']]
roe2015_4 = roe2015_4.loc[:,['code','name','roe_2015']]
roe2014_4 = roe2014_4.loc[:,['code','name','roe_2014']]
roe2018_1 = roe2018_1.loc[:,['code','name','roe_201801']]






temp1=pd.merge(roe2015, roe2016,how='outer', on=['code','name'])
temp1=pd.merge(roe2014, temp1,   how='outer', on=['code','name'])
#print(temp1)
temp2=pd.merge(roe2017, roe2018_1,how='outer', on=['code','name'])
#print(temp2)
roe=pd.merge(temp1,temp2,how='outer',on=['code','name'])
roe = roe.drop_duplicates()


# roe['roe_201704'] = roe['roe_201704']-roe['roe_201703']
# roe['roe_201703'] = roe['roe_201703']-roe['roe_201702']
# roe['roe_201702'] = roe['roe_201702']-roe['roe_201701']




roe = roe[ ~ roe['name'].str.contains('ST') ]
roe = roe[ ~ roe['name'].str.contains('退市')]
roe = roe[ ~ roe['name'].str.contains('XD')]
roe = roe[ ~ roe['name'].str.contains('DR')]


#增长数据处理

grow2018_1 = ts.get_growth_data(2018,1)
grow2017_4 = ts.get_growth_data(2017,4)
grow2017_3 = ts.get_growth_data(2017,3)
grow2017_2 = ts.get_growth_data(2017,2)



# grow2018_1[grow2018_1.iloc[:,2:]>0]
# grow2017_2[grow2017_2.iloc[:,2:]>0]
# grow2017_3[grow2017_3.iloc[:,2:]>0]
# grow2017_4[grow2017_4.iloc[:,2:]>0]



grow2018_1=grow2018_1[grow2018_1>0]
grow2017_2=grow2017_2[grow2017_2>0]
grow2017_3=grow2017_3[grow2017_3>0]
grow2017_4=grow2017_4[grow2017_4>0]










grow2018_1.rename(columns={ "mbrg":"主营业务收入增长率(%)_201801",
	"nprg":"净利润增长率(%)_201801","nav":"净资产增长率_201801",
	"targ":"总资产增长率_201801","epsg":"每股收益增长率_201801",
	"seg":"股东权益增长率_201801"}, inplace = True)

grow2017_4.rename(columns={"mbrg":"主营业务收入增长率(%)_201704",
	"nprg":"净利润增长率(%)_201704","nav":"净资产增长率_201704",
	"targ":"总资产增长率_201704","epsg":"每股收益增长率_201704",
	"seg":"股东权益增长率_201704" }, inplace = True)

grow2017_3.rename(columns={"mbrg":"主营业务收入增长率(%)_201703",
	"nprg":"净利润增长率(%)_201703","nav":"净资产增长率_201703",
	"targ":"总资产增长率_201703","epsg":"每股收益增长率_201703",
	"seg":"股东权益增长率_201703" }, inplace = True)

grow2017_2.rename(columns={"mbrg":"主营业务收入增长率(%)_201702",
	"nprg":"净利润增长率(%)_201702","nav":"净资产增长率_201702",
	"targ":"总资产增长率_201702","epsg":"每股收益增长率_201702",
	"seg":"股东权益增长率_201702" }, inplace = True)



grow2017_4 = grow2017_4.loc[:,['code','name','净利润增长率(%)_201704']]
grow2017_3 = grow2017_3.loc[:,['code','name','净利润增长率(%)_201703']]
grow2017_2 = grow2017_2.loc[:,['code','name','净利润增长率(%)_201702']]
grow2018_1 = grow2018_1.loc[:,['code','name','净利润增长率(%)_201801']]




temp3=pd.merge(grow2017_2, grow2017_3,how='outer', on=['code','name'])
temp4=pd.merge(grow2017_4, grow2018_1,how='outer', on=['code','name'])
grow=pd.merge(temp3,temp4,how='outer',on=['code','name'])

grow = grow[ ~ grow['name'].str.contains('ST') ]
grow = grow[ ~ grow['name'].str.contains('退市')]
grow = grow[ ~ grow['name'].str.contains('XD')]
grow = grow[ ~ grow['name'].str.contains('DR')]




roe_grow=pd.merge(roe,grow,how='outer',on=['code','name'])

re=pd.merge(roe_grow,basic,how='outer',on='name')
re = re.drop_duplicates()


re.to_excel(date+'_part2.xlsx', index=False)




