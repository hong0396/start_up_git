
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


code=pd.read_csv('D:\\Git\\us_stock\\analysis\\net.csv',encoding='gbk')
code_20=pd.read_csv('D:\\Git\\us_stock\\analysis\\pe20_net.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/laohu/basic_code/2018-08-25us_all_code.csv',encoding='gbk')
li_code=code['code'].tolist()        
li_code_20=code_20['code'].tolist()



dji=pd.read_csv('D:\\Git\\us_stock\\technical_analysis\\price\\laohu_price\\2018-09-13_dji_month.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
# djitime=dji['time'].tolist()
dji.rename(columns={'close':'close_dji'}, inplace = True)



def todate(tim):
    tim=int(tim)/1000
    return time.strftime('%Y-%m-%d',time.localtime(tim))




url='https://hq.itiger.com/stock_info/candle_stick/month/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'

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
        dic_tmp['year']=0
        dic_tmp['grow_6']=0
        dic_tmp['grow_3']=0
        dic_tmp['grow_3_1']=0
        dic_tmp['grow_3_2']=0
        dic_tmp['grow_3_3']=0
        dic_tmp['month_six_rs']=0
        dic_tmp['year_rs']=0
        dic_tmp['volume_start']=0
        dic_tmp['volume_end']=0
        dic_tmp['vol_radio']=0
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            jo['grow']=(jo['close']-jo['open'])/jo['open']
            jo_grow6=jo.sort_values(by="time", ascending=False)[:6]
            
            grow_6=jo_grow6['grow'].mean()
            jo_grow3=jo.sort_values(by="time", ascending=False)[:3]
            
            grow3list=jo_grow3['grow'].tolist()
            if len(grow3list) ==3:
                grow_3_1=jo_grow3['grow'].tolist()[0]
                grow_3_2=jo_grow3['grow'].tolist()[1]
                grow_3_3=jo_grow3['grow'].tolist()[2]

            grow_3=jo_grow3['grow'].mean()


            jo['time']=jo['time'].apply(todate)
            jo['close_pre_tmp'] = jo["close"].shift(1)
            jo['month_grow_tmp']=(jo["close"]-jo['close_pre_tmp'])/jo['close_pre_tmp']
            
            su=pd.merge(jo, dji, on='time',how='inner')
            su['month_rs']=su['month_grow_tmp']-su['month_grow']
            su_sort=su.sort_values(by="month_rs", ascending=False)[:6]   
            month_six_rs=su_sort['month_rs'].mean()
            su_sort=su.sort_values(by="month_rs", ascending=False)[:12]
            year_rs=su_sort['month_rs'].mean()
            # print(jo)
            # for i in li_data:
            #     close_tmp=i.get('close')
            #     time_tmp=i.get('time')
            #     volume_tmp=i.get('volume')
            #     date_tmp=todate(time_tmp)

       
            count=jo.shape[0]
            year=int(count/12)
            startprice=jo['open'][0]
            endd=jo['close'][count-1]
            meam_tmp=jo['close'].mean()
            std_tmp=jo['close'].std()    
            max=jo['close'].max()
            min=jo['close'].min()
            price_start=jo[:int(count/3)]['close'].mean()
            price_middle=jo[int(count/3):int((count*2)/3)]['close'].mean()
            price_end=jo[int((count*2)/3):]['close'].mean()
            vol_start=jo[:int(count/2)]['volume'].mean()
            vol_end=jo[int(count/2):]['volume'].mean()
            vol_radio=(vol_end-vol_start)/vol_start
            dic_tmp['count']=count
            dic_tmp['price']=meam_tmp
            dic_tmp['month_six_rs']=month_six_rs
            dic_tmp['year_rs']=year_rs
            dic_tmp['year']=year
            dic_tmp['grow_6']=grow_6
            dic_tmp['grow_3']=grow_3
            dic_tmp['grow_3_1']=grow_3_1
            dic_tmp['grow_3_2']=grow_3_2
            dic_tmp['grow_3_3']=grow_3_3
            dic_tmp['volume_start']=vol_start
            dic_tmp['volume_end']=vol_end
            dic_tmp['vol_radio']=vol_radio
            li.append(dic_tmp)
        nu_nu=nu_nu+1
    datatable=pd.DataFrame(li)
    return datatable

pan=get_laohu_price(url, li_code)
re=pd.merge(code, pan, how='outer',on='code')
re=re.drop_duplicates()
re.to_csv(date+'_Laohu_us_rs.csv', encoding = 'gbk',index=False)


# cn_us=get_laohu_code(url_us, [i for i in range(14)])
# cn_us.to_csv(date+'us_us_code.csv', index=False, encoding ='gbk')

# frames=[cn_nsdq,cn_ny,cn_us]
# sum=pd.concat(frames,ignore_index=True)
# sum.to_csv(date+'us_all_code.csv', index=False, encoding ='gbk')
