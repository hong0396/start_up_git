import numpy as np
import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
import os, sys
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.optimize import minimize, bracket, minimize_scalar
from matplotlib.pylab import date2num
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick_ohlc
import gc 
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import ip_te
ip_factory=ip_te.ip_get_test_save(1.5,1)

requests.packages.urllib3.disable_warnings()
path=os.getcwd()
def getmin(fun,xa,xb):
    res1 = bracket(fun, xa = xa, xb=xb)
    res = minimize_scalar(fun,  bounds=(res1[2],res1[1]),  method='bounded')
    return res.x

def pixo(useful_proxies,url):
    proxy = random.choice(list(useful_proxies.keys()))
    print ("change proxies: " + proxy)
    content = ''
    try:
        con = requests.get(url, proxies={"http": "http://" +proxy}, headers=header, verify=False,timeout=5).json()
        time.sleep(0.1)
    except OSError:
        # 超过3次则删除此proxy
        useful_proxies[proxy] += 1
        if useful_proxies[proxy] > 3:
            del useful_proxies[proxy]
        # 再抓一次
        proxy = random.choice(list(useful_proxies.keys()))
        # print('shengxia'+proxy)
        con = requests.get(url, proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()
    return con
def todate(timeStamp):
    timeArray = time.localtime(timeStamp/1000)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
# print(time.time())
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
my_headers = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']
header={'Accept': 'application/json, text/plain, */*', 
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Authorization': 'Bearer Vxe2C7g0gtyh2bLvjVTdkqIyuqhtLG',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
"User-Agent":random.choice(my_headers) }


code=pd.read_csv('last_us_all_code.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()
pe=code['pe'].tolist()
# li_code=li_code[:10]
# code=code[:10]


url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'




def get_grow_code(url,days, li_code,pe): 
    # fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    li_code_tmp=[]
    li_days_tmp=[]
    li_pe_tmp=[]
    li_num_tmp=[] 
    nu_nu=0
    nu_n=0 

    useful_proxies = {}
    max_failure_times = 3
    try:
    # 获取代理IP数据
        for ip in list(ip_factory):
            useful_proxies[ip] = 0
        print ("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！") 
    url_dji='https://hq.itiger.com/stock_info/candle_stick/week/.DJI?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'
    con =pixo(useful_proxies,url_dji)
 
    li_data=con.get('items')    
    if li_data is not None:
        dji_pd=pd.DataFrame(li_data)
        dji_pd['time']=dji_pd['time'].apply(todate)
        dji_pd['close_pre'] = dji_pd["close"].shift(1)
        dji_pd['week_grow']=(dji_pd["close"]-dji_pd['close_pre'])/dji_pd['close_pre']
        dji_pd=dji_pd[['time','week_grow']]
        


    for ii, code_nm in enumerate(li_code):
        print('-----------------------从第'+str(nu_nu)+'只股票提取------------------------------------')
        proxy = random.choice(list(useful_proxies.keys()))
        print ("change proxies: " + proxy)

        content = ''
        try:
            con = requests.get(url.format(str(code_nm)), proxies={"http": "http://" +proxy}, headers=header, verify=False,timeout=5).json()
            time.sleep(0.1)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                del useful_proxies[proxy]
            # 再抓一次
            proxy = random.choice(list(useful_proxies.keys()))
            # print('shengxia'+proxy)
            con = requests.get(url.format(str(code_nm)), proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()

      
        if con.get('error') is None:               
            li_data=con.get('items')
            # print(li_data)
            if li_data is not None:
                jo=pd.DataFrame(li_data)
                # jo=jo.sort_values(by="time", ascending=False)
                
           
                if len(jo.time.tolist()) > 60:
                    jo['close_pre_tmp'] = jo["close"].shift(1)
                    jo['week_grow_tmp']=(jo["close"]-jo['close_pre_tmp'])/jo['close_pre_tmp']
                 
                    # jo=jo.sort_values(by="time", ascending=False)[:15]
                    jo['time']=jo['time'].apply(todate)
                    
                  
                    su=pd.merge(jo, dji_pd, on='time',how='inner')
                    su['week_rs']=su['week_grow_tmp']-su['week_grow']
                    

                    zong=su.sort_values(by="time", ascending=False)
                    for i in range(days):
                        if zong.iloc[i]['week_rs'] >= 0:
                            if zong.iloc[i+1]['week_rs'] >= 0:
                                if zong.iloc[i+2]['week_rs'] >= 0:
                                    if zong.iloc[i+3]['week_rs'] >= 0:
                                        if zong.iloc[i+4]['week_rs'] >= 0:
                                            if zong.iloc[i+5]['week_rs'] >= 0:
                                                if zong.iloc[i+6]['week_rs'] >= 0:
                                                    if zong.iloc[i+7]['week_rs'] >= 0:
                                                        if zong.iloc[i+8]['week_rs'] >= 0:
                                                            if str(code_nm) not in li_code_tmp:
                                                                li_days_tmp.append(i)
                                                                li_code_tmp.append(str(code_nm))
                                                                li_pe_tmp.append(pe[ii])
                                                                nu_n=nu_n+1









                    # # 0个开盘价(涨)>1个收盘价(跌)
                    # # 1个开盘价(跌)>2个开盘价(涨)
                    # # 2个开盘价(涨)>3个开盘价(涨)
                    # # 3个开盘价(涨)>4个开盘价(涨)
                    # # 4个开盘价(涨)>5个开盘价(涨)
                    # # 0个开盘价(涨)>2个开盘价(涨)

                    # for i in range(days):

                    #     if round(zong.iloc[i]['open'],2) >= round(zong.iloc[i+1]['close'],2): 
                    #         if round(zong.iloc[i+1]['open'],2) >= round(zong.iloc[i+2]['open'],2):
                    #             if round(zong.iloc[i+2]['open'],2) >= round(zong.iloc[i+3]['open'],2): 
                    #                 if round(zong.iloc[i+3]['open'],2) >= round(zong.iloc[i+4]['open'],2):
                    #                     if round(zong.iloc[i+4]['open'],2) >= round(zong.iloc[i+5]['open'],2): 
                    #                         if round(zong.iloc[i]['open'],2) >= round(zong.iloc[i+2]['open'],2): 

                    #                             if (zong.iloc[i]['close'] - zong.iloc[i]['open'])/zong.iloc[i]['open'] > 0:
                    #                                 if (zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] <= 0:
                    #                                     if (zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] >= 0:
                    #                                         if (zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] >= 0:
                    #                                             if (zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] >= 0:
                    #                                                 if (zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] >= 0:
                    #                                                     if str(code_nm) not in li_code_tmp:
                    #                                                         li_days_tmp.append(i)
                    #                                                         li_code_tmp.append(str(code_nm))
                    #                                                         nu_n=nu_n+1
                    del jo, zong, su
                    gc.collect()
                    # if zong['open'].is_monotonic_decreasing:
                    
                    # 第0个开盘价(涨)>1个收盘价(跌)
                    # 1个开盘价(跌)>2个开盘价(涨)>3个开盘价(涨)>4个开盘价(涨)>5个开盘价(涨)

                    # if zong.iloc[0]['open'] > zong.iloc[1]['close'] and zong.iloc[1]['open'] > zong.iloc[2]['open']:
                    # # if zong.iloc[1]['open'] > zong.iloc[2]['open']:
                    #     if zong.iloc[2]['open'] > zong.iloc[3]['open'] and zong.iloc[3]['open'] > zong.iloc[4]['open'] and zong.iloc[4]['open'] > zong.iloc[5]['open']:    
                    #         if (first['close'] - first['open'])/first['open'] >= 0:
                    #             if (second['close'] - second['open'])/second['open'] <= 0:
                    #                 nuuu=0       
                    #                 for row in last.itertuples(): 
                    #                     if (getattr(row,'close') - getattr(row,'open'))/getattr(row,'open') >= 0:
                    #                         nuuu=nuuu+1
                    #                 if nuuu==4:
                    #                     li_code_tmp.append(str(code_nm))
                    #                     nu_n=nu_n+1
            nu_nu=nu_nu+1
            print('***********共提取'+str(nu_n)+'只股票符合条件***********')
        else:
            print(con.get('error'))
            print('下载数据错误')

                  
    tmp_df=pd.DataFrame({'days':li_days_tmp,'code':li_code_tmp,'pe':li_pe_tmp})    
    return tmp_df


def get_earn(li_code):

    nu_nuu=0
    liil=[]

    useful_proxies = {}
    max_failure_times = 3
    try:
    # 获取代理IP数据
        for ip in list(ip_factory):
            useful_proxies[ip] = 0
        print ("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！")


    for code_nm in li_code:
        print('-------------------------------'+str(nu_nuu)+'----------------------------------------')
        # print('-------------------------------'+str(code_nm)+'-------------------------------------')
        url='https://hq.itiger.com/fundamental/usstock/earnings/income/'+code_nm+'?type=income&symbol='+code_nm+'&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
        # time.sleep(0.1)
        proxy = random.choice(list(useful_proxies.keys()))
        print ("change proxies: " + proxy)

        content = ''
        try:
            res=requests.get(url, proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5)
            time.sleep(0.1)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                del useful_proxies[proxy]
            # 再抓一次
            proxy = random.choice(list(useful_proxies.keys()))
            # print('shengxia'+proxy)
            res=requests.get(url, proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5)
            

        if res.status_code == 200:
            a=res.json()
            li=a.get('data').get('page')
            li_h=a.get('data').get('header')
            # print(li)

            num=2018
            num_income=2018
            value='0'
            yoy='0'
            value_income='0'
            yoy_income='0'



            if not li_h is None:
                for h in range(len(li_h)):
                    if li_h[h].get('name') ==  "净利润":
                        num=h
                    if li_h[h].get('name') ==  "主营业务收入":
                        num_income=h

            if num != 2018: 
                if not li is None:
                        li=li[0]
                        if li.get('type') == '季报':
                            year_date=li.get('date')[:7]
                            tmmp=li.get('cell')
                            if num+1 < len(tmmp):
                                valu=tmmp[num].get('value')
                                yoy=tmmp[num].get('yoy')
                                if yoy is None:
                                    yoy='0'
                                if not valu is None:
                                    value=valu.replace(',','')
                                    if '千' in value:                                
                                        value=float(value.replace('千',''))*1000
                                    elif '万' in value:                             
                                        value=float(value.replace('万',''))*10000
                                    elif '亿' in value:                              
                                        value=float(value.replace('亿',''))*100000000
                                else:
                                    value='0'
                            else:
                                value='0'
                                yoy='0'


                            if num_income+1 < len(tmmp):
                                valu_income=tmmp[num_income].get('value')
                                yoy_income=tmmp[num_income].get('yoy')
                                if yoy_income is None:
                                    yoy_income='0'
                                if not valu_income is None:
                                    value_income=valu_income.replace(',','')
                                    if '千' in value_income:                                
                                        value_income=float(value_income.replace('千',''))*1000
                                    elif '万' in value_income:                             
                                        value_income=float(value_income.replace('万',''))*10000
                                    elif '亿' in value_income:                              
                                        value_income=float(value_income.replace('亿',''))*100000000
                                else:
                                    value_income='0'
                            else:
                                value_income='0'
                                yoy_income='0'
         
                            
            liil.append(str(value)+'_'+yoy+'_'+str(value_income)+'_'+yoy_income)              
        else:
            print('下载数据错误')
        nu_nuu=nu_nuu+1
    tmp_df=pd.DataFrame({'earn':liil,'code':li_code})    
    return tmp_df    
      
# def date_to_num(dates):
#     num_time = []
#     for date in dates:
#         date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
#         num_date = date2num(date_time)
#         num_time.append(num_date)
#     return num_time



def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.
    type is 'simple' | 'exponential'
    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a




def get_laohu_analysis(n, url, li_code,days,earn,pee): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))

    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    useful_proxies = {}
    max_failure_times = 3
    try:
    # 获取代理IP数据
        for ip in list(ip_factory):
            useful_proxies[ip] = 0
        print ("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！") 


    
    url_dji='https://hq.itiger.com/stock_info/candle_stick/week/.DJI?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'
    con =pixo(useful_proxies,url_dji)
 
    li_data=con.get('items')    
    if li_data is not None:
        dji_pd=pd.DataFrame(li_data)
        dji_pd['time']=dji_pd['time'].apply(todate)
        dji_pd['close_pre'] = dji_pd["close"].shift(1)
        dji_pd['volume_pre'] = dji_pd["volume"].shift(1)
        dji_pd['week_grow']=(dji_pd["close"]-dji_pd['close_pre'])/dji_pd['close_pre']
        dji_pd['vol_grow']=(dji_pd["volume"]-dji_pd['volume_pre'])/dji_pd['volume_pre'] 
        dji_pd=dji_pd[['time','week_grow','vol_grow']]
        



    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        proxy = random.choice(list(useful_proxies.keys()))
        print ("change proxies: " + proxy)

        content = ''
        try:
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header, verify=False,timeout=5).json()
            time.sleep(0.1)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                del useful_proxies[proxy]
            # 再抓一次
            proxy = random.choice(list(useful_proxies.keys()))
            # print('shengxia'+proxy)
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()

        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            quotes=jo.copy()
            
            quotes['close_pre_tmp'] = quotes["close"].shift(1)
            quotes['week_grow_tmp']=(quotes["close"]-quotes['close_pre_tmp'])/quotes['close_pre_tmp']
            quotes['volume_pre_tmp'] = quotes["volume"].shift(1)
            quotes['vol_grow_tmp']=(quotes["volume"]-quotes['volume_pre_tmp'])/quotes['volume_pre_tmp']
            

            quotes_part=quotes.sort_values(by="time", ascending=False)[:15]
            bio=round(((quotes_part.iloc[days[nmm]]['close'] - quotes_part.iloc[days[nmm]+5]['open'])/quotes_part.iloc[5]['open'])/5,2)
            # quotes=quotes.sort_values(by="time", ascending=True)

            # quotes['time']=quotes['time'].apply(todate)
            quotes=quotes.sort_values(by="time", ascending=False)[:15]
            quotes['time']=quotes['time'].apply(todate)
            
          
            su=pd.merge(quotes, dji_pd, on='time',how='inner')
            su['week_rs']=su['week_grow_tmp']-su['week_grow']
            su['vol_rs']=su['vol_grow_tmp']-su['vol_grow']
            quotes=su.copy()
            quotes['time']=pd.to_datetime(quotes['time'], format="%Y-%m-%d")

            x = jo['time'].values
            y = jo['close'].values
            vol = jo['volume'].values
            vol_li = jo['volume'].tolist()
            vol_min=min(vol_li)
            vol_max=max(vol_li)
            vol_up=(vol_max-vol_min)*0.3+vol_max
            z1 = np.polyfit(x, y, 4)#用3次多项式拟合
            p1 = np.poly1d(z1)
            # print(p1) #在屏幕上打印拟合多项式
            yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
            der=p1.deriv(m=2)
            dder=der(x)
            dder_list = dder.tolist()
            maxindex=dder_list.index(max(dder_list))
            # print(maxindex)
            time_max=jo['time'][maxindex]
            close_max=jo['close'][maxindex]
            p1_max=p1(time_max)



            # print(jo)
            # ax =fig.add_axes(axes[nu_nu//10, nu_nu%10])
            ax=axes[nu_nu//10, nu_nu%10]
            # count=quotes.shape[0]
            # year=int(count/48)
            # ax.set_title(str(li_code[nmm])+'('+str(year)+')',fontsize=18,fontweight='bold')    
            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)',fontsize=18,fontweight='bold')    
            if not '-' in str(earn[nmm]).split('_')[0]:
                ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str(pee[nmm]).split('.')[0]+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%'+'u',fontsize=18,fontweight='bold')        
            else:
                ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str(pee[nmm]).split('.')[0]+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%'+'d',fontsize=18,fontweight='bold',color="darkgreen")    

            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)_'+str(round(bio*100,0)),fontsize=18,fontweight='bold')    
            # plot1=ax.plot(x, y, marker=r'$\clubsuit$', color='goldenrod',markersize=15,label='original values')
            # plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')   
            
            # data_list=[]
            # for row in quotes.itertuples():
            #     date_time = datetime.datetime.strptime(getattr(row,'time'),'%Y-%m-%d')
            #     t = date2num(date_time)
            #     open_tmp = getattr(row,'open')
            #     high_tmp = getattr(row,'high')
            #     low_tmp  = getattr(row,'low')
            #     close_tmp = getattr(row,'close')
            #     datas = (t,open_tmp,high_tmp,low_tmp,close_tmp)
            #     data_list.append(datas)
            
            
            candlestick_ohlc(ax, zip(mdates.date2num(quotes['time'].dt.to_pydatetime()),
                         quotes['open'], quotes['high'],
                         quotes['low'], quotes['close']),
                 width=2,colordown='#53c156', colorup='#ff1717')
            

            # if len(quotes["close"].tolist()) >200:
            #     ma150 = moving_average(quotes["close"], 150, type='simple')
            #     ma200 = moving_average(quotes["close"], 200, type='simple')

            #     linema150, = ax.plot(quotes['time'], ma150, color='blue', lw=2, label='MA (150)')
            #     linema200, = ax.plot(quotes['time'], ma200, color='red', lw=2, label='MA (200)')


            # mpf.candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='green')
        
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)
            
 
            ax2t = ax.twinx()
            volume = (quotes.close * quotes.volume) / 1e6  # dollar volume in millions
            vmax = volume.max()
            fillcolor = 'darkgoldenrod'
            poly = ax2t.fill_between(quotes.time.values, volume, 0, label='Volume',
                         facecolor=fillcolor, edgecolor=fillcolor)
            
            ax2t.set_ylim(0, 20 * vmax)
            ax2t.set_yticks([])
            ax2t.set_xticks([])

            # ax3 =fig.add_axes(axes[nu_nu//10, nu_nu%10])
            ax3 = ax.twinx()
            ax3.plot(quotes.time.values,   quotes.week_rs.values, linewidth=1, marker='o')
            ax3.set_ylim(-0.1, 0.5)
            ax3.set_yticks([])
            ax3.set_xticks([])
            time_max=max(quotes.time.tolist())
            time_min=min(quotes.time.tolist())
            ax3.annotate(' ', xy=(time_min, 0), xytext=(time_max, 0),fontsize= 10,arrowprops=dict(arrowstyle='-'),)


            ax5 = ax.twinx()
            ax5.plot(quotes.time.values,   quotes.week_rs.values, color='goldenrod',linewidth=1, marker='o')
            ax5.set_ylim(-0.3, 0.8)
            ax5.set_yticks([])
            ax5.set_xticks([])
            time_max=max(quotes.time.tolist())
            time_min=min(quotes.time.tolist())
            ax5.annotate(' ', xy=(time_min, 0), xytext=(time_max, 0),fontsize= 10,arrowprops=dict(arrowstyle='-'),)


            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)
            


            del jo, quotes
            gc.collect()

            # mondays = WeekdayLocator(MONDAY)
            # ax.xaxis.set_major_locator(mondays)
            # daysFmt = DateFormatter("%m%d")
            # ax.xaxis.set_major_formatter(daysFmt)

            # ax2t.autoscale_view()
            # ax2 = ax.twinx()
            # plot3=ax2.plot(x, vol, zorder=0, c="g",linewidth=2,alpha=0.7)
            # ax2.set_zorder(0)
            # # ax2.set_ylabel('volume')
            # ax2.set_ylim(vol_min,vol_up) 
            # ax2.yaxis.set_major_locator(plt.NullLocator()) 
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig(path+'/up_data/'+date+"_week_up_"+str(n)+".png")
    # plt.show()
    





def get_laohu_analysis_rs(n, url, li_code,days,earn): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    useful_proxies = {}
    max_failure_times = 3
    try:
    # 获取代理IP数据
        for ip in list(ip_factory):
            useful_proxies[ip] = 0
        print ("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！") 




    url_dji='https://hq.itiger.com/stock_info/candle_stick/week/.DJI?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'
    con =pixo(useful_proxies,url_dji)
 
    li_data=con.get('items')    
    if li_data is not None:
        dji_pd=pd.DataFrame(li_data)
        dji_pd['time']=dji_pd['time'].apply(todate)
        dji_pd['close_pre'] = dji_pd["close"].shift(1)
        dji_pd['week_grow']=(dji_pd["close"]-dji_pd['close_pre'])/dji_pd['close_pre']
        dji_pd=dji_pd[['time','week_grow']]
        
    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        proxy = random.choice(list(useful_proxies.keys()))
        print ("change proxies: " + proxy)

        content = ''
        try:
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header, verify=False,timeout=5).json()
            time.sleep(0.1)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                del useful_proxies[proxy]
            # 再抓一次
            proxy = random.choice(list(useful_proxies.keys()))
            # print('shengxia'+proxy)
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()

        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            quotes=jo.copy()
            quotes['close_pre_tmp'] = quotes["close"].shift(1)
            quotes['week_grow_tmp']=(quotes["close"]-quotes['close_pre_tmp'])/quotes['close_pre_tmp']
            
            quotes_part=quotes.sort_values(by="time", ascending=False)[:15]
            bio=round(((quotes_part.iloc[days[nmm]]['close'] - quotes_part.iloc[days[nmm]+5]['open'])/quotes_part.iloc[5]['open'])/5,2)
            # quotes=quotes.sort_values(by="time", ascending=True)

            # quotes['time']=quotes['time'].apply(todate)
            quotes=quotes.sort_values(by="time", ascending=False)[:15]
            quotes['time']=quotes['time'].apply(todate)
            
          
            su=pd.merge(quotes, dji_pd, on='time',how='inner')
            su['week_rs']=su['week_grow_tmp']-su['week_grow']
           
            quotes=su.copy()
            quotes['time']=pd.to_datetime(quotes['time'], format="%Y-%m-%d")

            x = jo['time'].values
            y = jo['close'].values
            vol = jo['volume'].values
            vol_li = jo['volume'].tolist()
            vol_min=min(vol_li)
            vol_max=max(vol_li)
            vol_up=(vol_max-vol_min)*0.3+vol_max
            z1 = np.polyfit(x, y, 4)#用3次多项式拟合
            p1 = np.poly1d(z1)
            # print(p1) #在屏幕上打印拟合多项式
            yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
            der=p1.deriv(m=2)
            dder=der(x)
            dder_list = dder.tolist()
            maxindex=dder_list.index(max(dder_list))
            # print(maxindex)
            time_max=jo['time'][maxindex]
            close_max=jo['close'][maxindex]
            p1_max=p1(time_max)



            # print(jo)
            ax=axes[nu_nu//10, nu_nu%10]
            # count=quotes.shape[0]
            # year=int(count/48)
            # ax.set_title(str(li_code[nmm])+'('+str(year)+')',fontsize=18,fontweight='bold')    
            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)',fontsize=18,fontweight='bold')    
            if not '-' in str(earn[nmm]).split('_')[0]:
                ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%'+'u',fontsize=18,fontweight='bold')        
            else:
                ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%'+'d',fontsize=18,fontweight='bold',color="darkgreen")    

            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)_'+str(round(bio*100,0)),fontsize=18,fontweight='bold')    
            # plot1=ax.plot(x, y, marker=r'$\clubsuit$', color='goldenrod',markersize=15,label='original values')
            # plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')   
            
            # data_list=[]
            # for row in quotes.itertuples():
            #     date_time = datetime.datetime.strptime(getattr(row,'time'),'%Y-%m-%d')
            #     t = date2num(date_time)
            #     open_tmp = getattr(row,'open')
            #     high_tmp = getattr(row,'high')
            #     low_tmp  = getattr(row,'low')
            #     close_tmp = getattr(row,'close')
            #     datas = (t,open_tmp,high_tmp,low_tmp,close_tmp)
            #     data_list.append(datas)
            
            candlestick_ohlc(ax, zip(mdates.date2num(quotes['time'].dt.to_pydatetime()),
                         quotes['open'], quotes['high'],
                         quotes['low'], quotes['close']),
                 width=0.6,colordown='#53c156', colorup='#ff1717')
            

            # if len(quotes["close"].tolist()) >200:
            #     ma150 = moving_average(quotes["close"], 150, type='simple')
            #     ma200 = moving_average(quotes["close"], 200, type='simple')

            #     linema150, = ax.plot(quotes['time'], ma150, color='blue', lw=2, label='MA (150)')
            #     linema200, = ax.plot(quotes['time'], ma200, color='red', lw=2, label='MA (200)')


            # mpf.candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='green')
        
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)
            
 
            ax2t = ax.twinx()
            # volume = (quotes.close * quotes.volume) / 1e6  # dollar volume in millions
            # vmax = volume.max()
            # fillcolor = 'darkgoldenrod'
            # poly = ax2t.fill_between(quotes.time.values, volume, 0, label='Volume',
                         # facecolor=fillcolor, edgecolor=fillcolor)
            
            ax2t.plot(quotes.time.values,   quotes.week_rs.values, linewidth=1, marker='o')
            ax2t.set_ylim(-0.2, 0.8)
            ax2t.set_yticks([])
            ax2t.set_xticks([])
            time_max=max(quotes.time.tolist())
            time_min=min(quotes.time.tolist())
            ax2t.annotate(' ', xy=(time_min, 0), xytext=(time_max, 0),fontsize= 10,arrowprops=dict(arrowstyle='-'),)
            del jo, quotes,su,quotes_part
            gc.collect()

            # mondays = WeekdayLocator(MONDAY)
            # ax.xaxis.set_major_locator(mondays)
            # daysFmt = DateFormatter("%m%d")
            # ax.xaxis.set_major_formatter(daysFmt)

            # ax2t.autoscale_view()
            # ax2 = ax.twinx()
            # plot3=ax2.plot(x, vol, zorder=0, c="g",linewidth=2,alpha=0.7)
            # ax2.set_zorder(0)
            # # ax2.set_ylabel('volume')
            # ax2.set_ylim(vol_min,vol_up) 
            # ax2.yaxis.set_major_locator(plt.NullLocator()) 
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig(path+'/up_data/'+date+"_week_up_rs_"+str(n)+".png")
    # plt.show()


def get_laohu_analysis_all_rs(n, url, li_code,days,earn): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    useful_proxies = {}
    max_failure_times = 3
    try:
    # 获取代理IP数据
        for ip in list(ip_factory):
            useful_proxies[ip] = 0
        print ("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！") 

    url_dji='https://hq.itiger.com/stock_info/candle_stick/week/.DJI?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.2.0'
    con =pixo(useful_proxies,url_dji)
 
    li_data=con.get('items')    
    if li_data is not None:
        dji_pd=pd.DataFrame(li_data)
        dji_pd['time']=dji_pd['time'].apply(todate)
        dji_pd['close_pre'] = dji_pd["close"].shift(1)
        dji_pd['week_grow']=(dji_pd["close"]-dji_pd['close_pre'])/dji_pd['close_pre']
        dji_pd=dji_pd[['time','week_grow']]


    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        proxy = random.choice(list(useful_proxies.keys()))
        print ("change proxies: " + proxy)

        content = ''
        try:
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header, verify=False,timeout=5).json()
            time.sleep(0.1)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                del useful_proxies[proxy]
            # 再抓一次
            proxy = random.choice(list(useful_proxies.keys()))
            # print('shengxia'+proxy)
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()

        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            quotes=jo.copy()

            quotes_part=quotes.sort_values(by="time", ascending=False)[:15]
            bio=round(((quotes_part.iloc[days[nmm]]['close'] - quotes_part.iloc[days[nmm]+5]['open'])/quotes_part.iloc[5]['open'])/5,2)
            # quotes=quotes.sort_values(by="time", ascending=True)

            # quotes['time']=quotes['time'].apply(todate)

            quotes['time']=quotes['time'].apply(todate)
            quotes['close_pre_tmp'] = quotes["close"].shift(1)
            quotes['week_grow_tmp']=(quotes["close"]-quotes['close_pre_tmp'])/quotes['close_pre_tmp']
            
            su=pd.merge(quotes, dji_pd, on='time',how='inner')
            su['week_rs']=su['week_grow_tmp']-su['week_grow']

            quotes=su.copy()
            quotes['time']=pd.to_datetime(quotes['time'], format="%Y-%m-%d")

            x = jo['time'].values
            y = jo['close'].values
            vol = jo['volume'].values
            vol_li = jo['volume'].tolist()
            vol_min=min(vol_li)
            vol_max=max(vol_li)
            vol_up=(vol_max-vol_min)*0.3+vol_max
            z1 = np.polyfit(x, y, 4)#用3次多项式拟合
            p1 = np.poly1d(z1)
            # print(p1) #在屏幕上打印拟合多项式
            yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
            der=p1.deriv(m=2)
            dder=der(x)
            dder_list = dder.tolist()
            maxindex=dder_list.index(max(dder_list))
            # print(maxindex)
            time_max=jo['time'][maxindex]
            close_max=jo['close'][maxindex]
            p1_max=p1(time_max)



            # print(jo)
            ax=axes[nu_nu//10, nu_nu%10]
            # count=quotes.shape[0]
            # year=int(count/48)
            # ax.set_title(str(li_code[nmm])+'('+str(year)+')',fontsize=18,fontweight='bold')    
            
            if not '-' in str(earn[nmm]).split('_')[0]:
                ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%'+'u',fontsize=18,fontweight='bold')        
            else:
                ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%'+'d',fontsize=18,fontweight='bold',color="darkgreen")    
            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%',fontsize=18,fontweight='bold')    
            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)',fontsize=18,fontweight='bold')    
            # plot1=ax.plot(x, y, marker=r'$\clubsuit$', color='goldenrod',markersize=15,label='original values')
            # plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')   
            
            # data_list=[]
            # for row in quotes.itertuples():
            #     date_time = datetime.datetime.strptime(getattr(row,'time'),'%Y-%m-%d')
            #     t = date2num(date_time)
            #     open_tmp = getattr(row,'open')
            #     high_tmp = getattr(row,'high')
            #     low_tmp  = getattr(row,'low')
            #     close_tmp = getattr(row,'close')
            #     datas = (t,open_tmp,high_tmp,low_tmp,close_tmp)
            #     data_list.append(datas)
            
            candlestick_ohlc(ax, zip(mdates.date2num(quotes['time'].dt.to_pydatetime()),
                         quotes['open'], quotes['high'],
                         quotes['low'], quotes['close']),
                 width=0.6,colordown='#53c156', colorup='#ff1717')
            

            # if len(quotes["close"].tolist()) >200:
            #     ma150 = moving_average(quotes["close"], 150, type='simple')
            #     ma200 = moving_average(quotes["close"], 200, type='simple')

            #     linema150, = ax.plot(quotes['time'], ma150, color='blue', lw=2, label='MA (150)')
            #     linema200, = ax.plot(quotes['time'], ma200, color='red', lw=2, label='MA (200)')


            # mpf.candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='green')
        
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)
            
 
            ax2t = ax.twinx()
            # volume = (quotes.close * quotes.volume) / 1e6  # dollar volume in millions
            # vmax = volume.max()
            # fillcolor = 'darkgoldenrod'
            # poly = ax2t.fill_between(quotes.time.values, volume, 0, label='Volume',
                         # facecolor=fillcolor, edgecolor=fillcolor)
            
            ax2t.plot(quotes.time.values,   quotes.week_rs.values, linewidth=1, marker='o')
            ax2t.set_ylim(-0.2, 0.8)
            ax2t.set_yticks([])
            ax2t.set_xticks([])
            time_max=max(quotes.time.tolist())
            time_min=min(quotes.time.tolist())
            ax2t.annotate(' ', xy=(time_min, 0), xytext=(time_max, 0),fontsize= 10,arrowprops=dict(arrowstyle='-'),)
            del jo, quotes,su,quotes_part
            gc.collect()

            # mondays = WeekdayLocator(MONDAY)
            # ax.xaxis.set_major_locator(mondays)
            # daysFmt = DateFormatter("%m%d")
            # ax.xaxis.set_major_formatter(daysFmt)

            # ax2t.autoscale_view()
            # ax2 = ax.twinx()
            # plot3=ax2.plot(x, vol, zorder=0, c="g",linewidth=2,alpha=0.7)
            # ax2.set_zorder(0)
            # # ax2.set_ylabel('volume')
            # ax2.set_ylim(vol_min,vol_up) 
            # ax2.yaxis.set_major_locator(plt.NullLocator()) 
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig(path+'/up_data/'+date+"_week_up_all_rs_"+str(n)+".png")
    # plt.show()
 


def get_laohu_analysis_all(n, url, li_code,days,earn): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    useful_proxies = {}
    max_failure_times = 3
    try:
    # 获取代理IP数据
        for ip in list(ip_factory):
            useful_proxies[ip] = 0
        print ("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！") 

    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        proxy = random.choice(list(useful_proxies.keys()))
        print ("change proxies: " + proxy)

        content = ''
        try:
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header, verify=False,timeout=5).json()
            time.sleep(0.1)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                del useful_proxies[proxy]
            # 再抓一次
            proxy = random.choice(list(useful_proxies.keys()))
            # print('shengxia'+proxy)
            con = requests.get(url.format(str(li_code[nmm])), proxies={"http": "http://" +proxy}, headers=header,verify=False,timeout=5).json()

        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            quotes=jo.copy()
            
            quotes_part=quotes.sort_values(by="time", ascending=False)[:15]
            bio=round(((quotes_part.iloc[days[nmm]]['close'] - quotes_part.iloc[days[nmm]+5]['open'])/quotes_part.iloc[5]['open'])/5,2)
            # quotes=quotes.sort_values(by="time", ascending=True)

            quotes['time']=quotes['time'].apply(todate)
            quotes['time']=pd.to_datetime(quotes['time'], format="%Y-%m-%d")

            x = jo['time'].values
            y = jo['close'].values
            vol = jo['volume'].values
            vol_li = jo['volume'].tolist()
            vol_min=min(vol_li)
            vol_max=max(vol_li)
            vol_up=(vol_max-vol_min)*0.3+vol_max
            z1 = np.polyfit(x, y, 4)#用3次多项式拟合
            p1 = np.poly1d(z1)
            # print(p1) #在屏幕上打印拟合多项式
            yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
            der=p1.deriv(m=2)
            dder=der(x)
            dder_list = dder.tolist()
            maxindex=dder_list.index(max(dder_list))
            # print(maxindex)
            time_max=jo['time'][maxindex]
            close_max=jo['close'][maxindex]
            p1_max=p1(time_max)



            # print(jo)
            ax=axes[nu_nu//10, nu_nu%10]
            # count=quotes.shape[0]
            # year=int(count/48)
            # ax.set_title(str(li_code[nmm])+'('+str(year)+')',fontsize=18,fontweight='bold')    
            
            if not '-' in str(earn[nmm]).split('_')[0]:
                ax.set_title(str(li_code[nmm])+'_'+str(days[nmm])+'_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%',fontsize=18,fontweight='bold')        
            else:
                ax.set_title(str(li_code[nmm])+'_'+str(days[nmm])+'_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%',fontsize=18,fontweight='bold',color="darkgreen")    
            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+')_'+str(int(bio*100))+'_'+str((str(earn[nmm]).split('_')[1].strip('%')).split('.')[0].replace(',', ''))+'%',fontsize=18,fontweight='bold')    
            # ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)',fontsize=18,fontweight='bold')    
            # plot1=ax.plot(x, y, marker=r'$\clubsuit$', color='goldenrod',markersize=15,label='original values')
            # plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')   
            
            # data_list=[]
            # for row in quotes.itertuples():
            #     date_time = datetime.datetime.strptime(getattr(row,'time'),'%Y-%m-%d')
            #     t = date2num(date_time)
            #     open_tmp = getattr(row,'open')
            #     high_tmp = getattr(row,'high')
            #     low_tmp  = getattr(row,'low')
            #     close_tmp = getattr(row,'close')
            #     datas = (t,open_tmp,high_tmp,low_tmp,close_tmp)
            #     data_list.append(datas)
            
            candlestick_ohlc(ax, zip(mdates.date2num(quotes['time'].dt.to_pydatetime()),
                         quotes['open'], quotes['high'],
                         quotes['low'], quotes['close']),
                 width=0.6,colordown='#53c156', colorup='#ff1717')
            

            # if len(quotes["close"].tolist()) >200:
            #     ma150 = moving_average(quotes["close"], 150, type='simple')
            #     ma200 = moving_average(quotes["close"], 200, type='simple')

            #     linema150, = ax.plot(quotes['time'], ma150, color='blue', lw=2, label='MA (150)')
            #     linema200, = ax.plot(quotes['time'], ma200, color='red', lw=2, label='MA (200)')


            # mpf.candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='green')
        
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)
            
 
            ax2t = ax.twinx()
            volume = (quotes.close * quotes.volume) / 1e6  # dollar volume in millions
            vmax = volume.max()
            fillcolor = 'darkgoldenrod'
            poly = ax2t.fill_between(quotes.time.values, volume, 0, label='Volume',
                         facecolor=fillcolor, edgecolor=fillcolor)
            
            ax2t.set_ylim(0, 15 * vmax)
            ax2t.set_yticks([])
            ax2t.set_xticks([])

            del jo, quotes
            gc.collect()

            # mondays = WeekdayLocator(MONDAY)
            # ax.xaxis.set_major_locator(mondays)
            # daysFmt = DateFormatter("%m%d")
            # ax.xaxis.set_major_formatter(daysFmt)

            # ax2t.autoscale_view()
            # ax2 = ax.twinx()
            # plot3=ax2.plot(x, vol, zorder=0, c="g",linewidth=2,alpha=0.7)
            # ax2.set_zorder(0)
            # # ax2.set_ylabel('volume')
            # ax2.set_ylim(vol_min,vol_up) 
            # ax2.yaxis.set_major_locator(plt.NullLocator()) 
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig(path+'/up_data/'+date+"_week_up_all_"+str(n)+".png")
    # plt.show()
    

            
def write_li(fileName,li):
       fp = open(fileName,'w+')      
       for i in range(len(li)):
           fp.write(str(li[i])+'\n')
       fp.close()
       return True
def write_csv(fileName,df):
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    df.rename(columns={'days':str(date)+'_days','code':str(date)+'_code'},inplace=True) 
    if os.path.exists(fileName): 
        tmp_df=pd.read_csv(fileName)
        if str(date)+'_days' in tmp_df.columns.tolist() :
            tmp_df=tmp_df.drop(columns=[str(date)+'_days',str(date)+'_code'])  
            df=tmp_df.join(df, how='outer')
            df.to_csv(fileName,index=False)
        else:
            tmp_df=tmp_df.join(df, how='outer')
            tmp_df.to_csv(fileName,index=False)    
    else:
        df.to_csv(fileName,index=False)
    return True
        
days_df=get_grow_code(url_week, 5, li_code, pe)
days_sort_df=days_df.sort_values(by=['days','code'])
codee=days_sort_df.code.tolist()
days=days_sort_df.days.tolist()
pes=days_sort_df.pe.tolist()
# write_li('D:/Git/us_stock/technical_analysis/Main/up/4up1down1up_limit/up_data/'+date+'_up_code.txt',codee)
write_csv(path+'/up_data/record.csv',days_sort_df[['days','code']])
# codee=li_code[:1000]
# days_df[(days_df.code==tmp)].index.values
earn_df=get_earn(codee)
earn=earn_df.earn.tolist()


for i in range((len(codee)//100)+1):
    start=i*100 
    end=(i+1)*100
    if end >= len(codee):
        end = len(codee)  
    code_tmp=codee[start:end]
    days_tmp=days[start:end]
    earn_tmp=earn[start:end]
    pe_tmp=pes[start:end]
    get_laohu_analysis(i, url_week, code_tmp, days_tmp,earn_tmp,pe_tmp)
    # get_laohu_analysis_all_rs(i, url_week, code_tmp, days_tmp,earn_tmp)
    time.sleep(1)
    # get_laohu_analysis_all(i, url_week, code_tmp, days_tmp,earn_tmp)


















# def get_laohu_price(url,li_code):
#     li=[]
#     nu_nu=0
#     for code_nm in li_code:
#         print('------------------------------------------'+str(nu_nu)+'----------------------------------------------')
#         con = requests.get(url.format(str(code_nm)), headers=header).json()
#         time.sleep(0.1)
#         # print(con)
#             # a = str(con.decode())
#             # print(con.get('items')[0].get('data'))
#         # if period=="month"    
#         li_data=con.get('items')
#         dic_tmp={}
#         dic_tmp['code']=str(code_nm)
#         dic_tmp['count']=0
#         dic_tmp['mean']=0
#         dic_tmp['std']=0
#         dic_tmp['max']=0
#         dic_tmp['min']=0
#         dic_tmp['start']=0
#         dic_tmp['end']=0
#         dic_tmp['year']=0
#         dic_tmp['price_start']=0
#         dic_tmp['price_middle']=0
#         dic_tmp['price_end']=0
#         dic_tmp['volume_start']=0
#         dic_tmp['volume_end']=0
#         if li_data is not None:
#             jo=pd.DataFrame(li_data)
#             # print(jo)
#             # for i in li_data:
#             #     close_tmp=i.get('close')
#             #     time_tmp=i.get('time')
#             #     volume_tmp=i.get('volume')
#             #     date_tmp=todate(time_tmp)
#             count=jo.shape[0]
#             year=int(count/12)
#             startprice=jo['open'][0]
#             endd=jo['close'][count-1]
#             meam_tmp=jo['close'].mean()
#             std_tmp=jo['close'].std()    
#             max=jo['close'].max()
#             min=jo['close'].min()
#             price_start=jo[:int(count/3)]['close'].mean()
#             price_middle=jo[int(count/3):int((count*2)/3)]['close'].mean()
#             price_end=jo[int((count*2)/3):]['close'].mean()
#             vol_start=jo[:int(count/2)]['volume'].mean()
#             vol_end=jo[int(count/2):]['volume'].mean()
#             dic_tmp['count']=count
#             dic_tmp['mean']=meam_tmp
#             dic_tmp['std']=std_tmp
#             dic_tmp['max']=max
#             dic_tmp['min']=min
#             dic_tmp['start']=startprice
#             dic_tmp['end']=endd
#             dic_tmp['year']=year
#             dic_tmp['price_start']=price_start
#             dic_tmp['price_middle']=price_middle
#             dic_tmp['price_end']=price_end
#             dic_tmp['volume_start']=vol_start
#             dic_tmp['volume_end']=vol_end
#             li.append(dic_tmp)
#         nu_nu=nu_nu+1
#     datatable=pd.DataFrame(li)
#     return datatable






# re=pd.merge(code,pan,how='outer',on='code')
# re=re.drop_duplicates()
# re.to_csv(date+'_Laohu_us_analysis.csv', encoding = 'gbk',index=False)

