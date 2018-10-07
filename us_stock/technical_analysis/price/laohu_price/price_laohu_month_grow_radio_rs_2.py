
import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
from functools import reduce

def todate(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
# print(time.time())
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Authorization': 'Bearer gluCWKw06sXGLvRq1hsLaCd9vZRAUJ',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


code=pd.read_csv('D:\\Git\\us_stock\\analysis\\2018-10-07net.csv',encoding='gbk')
code_20=pd.read_csv('D:\\Git\\us_stock\\analysis\\pe20_net.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/laohu/basic_code/2018-08-25us_all_code.csv',encoding='gbk')
li_code=code['code'].tolist()        
li_code_20=code_20['code'].tolist()



dji=pd.read_csv('D:\\Git\\us_stock\\technical_analysis\\price\\laohu_price\\2018-10-07_dji_month.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
# djitime=dji['time'].tolist()
dji.rename(columns={'close':'close_dji'}, inplace = True)



def todate(tim):
    tim=int(tim)/1000
    return time.strftime('%Y-%m-%d',time.localtime(tim))




url='https://hq.itiger.com/stock_info/candle_stick/month/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'

# https://hq.itiger.com/stock_info/candle_stick/month/.DJI?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0

def get_laohu_price(url,li_cod):
    li=[]
    nu_nu=0
    for code_nm in li_cod:
        print('------------------------------------------'+str(nu_nu)+'----------------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header).json()
        time.sleep(0.1)
        # print(con)
            # a = str(con.decode())
            # print(con.get('items')[0].get('data'))
        # if period=="month"    
        li_data=con.get('items')
        dic_tmp={}
        dic_tmp['code']=str(code_nm)
        dic_tmp['count']=0
        dic_tmp['price']=0
        dic_tmp['max_price']=0
        dic_tmp['max_price_radio']=0
        dic_tmp['price_month_3']=0       
        dic_tmp['year']=0
        dic_tmp['grow_6']=0
        dic_tmp['grow_3']=0
        dic_tmp['grow_radio_6']=0
        dic_tmp['grow_radio_3']=0
        dic_tmp['month_3_rs']=0
        dic_tmp['month_6_rs']=0
        dic_tmp['volume_6']=0
        dic_tmp['volume_3']=0
        dic_tmp['vol_radio']=0
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            jo['grow']=jo['close']-jo['open']
            if len(jo['grow'].tolist())>6:
                jo_grow6=jo.sort_values(by="time", ascending=False)[3:6] 
                grow_6=jo_grow6['grow'].mean()
            if len(jo['grow'].tolist())>3:    
                jo_grow3=jo.sort_values(by="time", ascending=False)[:3]
                grow_3=jo_grow3['grow'].mean()

            jo['grow_radio']=(jo['close']-jo['open'])/jo['open']
            if len(jo['grow_radio'].tolist())>6:
                jo_radio_grow6=jo.sort_values(by="time", ascending=False)[3:6]            
                grow_radio_6=jo_radio_grow6['grow_radio'].mean()
            if len(jo['grow_radio'].tolist())>3:
                jo_radio_grow3=jo.sort_values(by="time", ascending=False)[:3]
                grow_radio_3=jo_radio_grow3['grow_radio'].mean()

            jo['time']=jo['time'].apply(todate)
            jo['close_pre_tmp'] = jo["close"].shift(1)
            jo['month_grow_tmp']=(jo["close"]-jo['close_pre_tmp'])/jo['close_pre_tmp']
            
            su=pd.merge(jo, dji, on='time',how='inner')
            su['month_rs']=su['month_grow_tmp']-su['month_grow']
            
            if len(su['month_rs'].tolist())>6:
                su_6_sort=su.sort_values(by="time", ascending=False)[3:6]   
                month_6_rs=su_6_sort['month_rs'].mean()
            if len(su['month_rs'].tolist())>3:
                su_3_sort=su.sort_values(by="time", ascending=False)[:3]
                month_3_rs=su_3_sort['month_rs'].mean()
            # print(jo)
            # for i in li_data:
            #     close_tmp=i.get('close')
            #     time_tmp=i.get('time')
            #     volume_tmp=i.get('volume')
            #     date_tmp=todate(time_tmp)
       
            count=jo.shape[0]
            year=int(count/12)
            startprice=jo['open'][0]
            price_endd=jo['close'][count-1]
            price_tmp=jo['close'].tolist()[0]
            

            price_month_3=jo['close'][count-3:].mean()    
            max_price=jo['close'].max()
            min_price=jo['close'].min()

            max_price_radio=(max_price-price_endd)/max_price
            price_start=jo[:int(count/3)]['close'].mean()
            price_middle=jo[int(count/3):int((count*2)/3)]['close'].mean()
            price_end=jo[int((count*2)/3):]['close'].mean()
            # vol_start=jo[:int(count/2)]['volume'].mean()
            # vol_end=jo[int(count/2):]['volume'].mean()
            if count>6:
            	vol_6=jo[(count-6):(count-3)]['volume'].mean()
            if count>3:
                vol_3=jo[(count-3):]['volume'].mean()
            if vol_6 !=0:    
                vol_radio=(vol_3-vol_6)/vol_6
            dic_tmp['count']=count
            dic_tmp['price']=price_endd
            dic_tmp['max_price']=max_price
            dic_tmp['max_price_radio']=max_price_radio
            dic_tmp['price_month_3']=price_month_3
            dic_tmp['month_6_rs']=month_6_rs
            dic_tmp['month_3_rs']=month_3_rs
            dic_tmp['year']=year
            dic_tmp['grow_6']=grow_6
            dic_tmp['grow_3']=grow_3
            dic_tmp['grow_radio_6']=grow_radio_6
            dic_tmp['grow_radio_3']=grow_radio_3
            dic_tmp['volume_6']=vol_6
            dic_tmp['volume_3']=vol_3
            dic_tmp['vol_radio']=vol_radio
            li.append(dic_tmp)
        nu_nu=nu_nu+1
    datatable=pd.DataFrame(li)
    return datatable

pan=get_laohu_price(url, li_code)
re=pd.merge(code, pan, how='outer',on='code')
re=re.drop_duplicates()
re.to_csv(date+'_Laohu_us_month_grow_radio_rs_2.csv', encoding = 'gbk',index=False)


# cn_us=get_laohu_code(url_us, [i for i in range(14)])
# cn_us.to_csv(date+'us_us_code.csv', index=False, encoding ='gbk')

# frames=[cn_nsdq,cn_ny,cn_us]
# sum=pd.concat(frames,ignore_index=True)
# sum.to_csv(date+'us_all_code.csv', index=False, encoding ='gbk')
