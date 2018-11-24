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

requests.packages.urllib3.disable_warnings()

def getmin(fun,xa,xb):
    res1 = bracket(fun, xa = xa, xb=xb)
    res = minimize_scalar(fun,  bounds=(res1[2],res1[1]),  method='bounded')
    return res.x


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
'Authorization': 'Bearer aAmt1vk9CI5QYnVMzRwXpfuvZmXmvo',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


code=pd.read_csv('last_us_all_code.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()

# li_code=li_code[:10]
# code=code[:10]


url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_5day='https://hq.itiger.com/stock_info/time_trend/5day/{}?beginTime=-1&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'

requests.packages.urllib3.disable_warnings()


def get_grow_code(url, nm,li_code): 
    # fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    li_code_tmp=[]
    li_days_tmp=[]
    li_num_tmp=[] 
    nu_nu=0
    nu_n=0 
    for code_nm in li_code:
        print('-----------------------从第'+str(nu_nu)+'只股票提取------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header, verify=False).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            # print(jo)
            # jo=jo.sort_values(by="time", ascending=False)
            if len(jo.time.tolist()) > 30:
                zong=jo.sort_values(by="time", ascending=False)[:30]
                # 0个开盘价(跌)<1个收盘价(涨)
                # 1个开盘价(涨)<2个开盘价(跌)
                # 2个开盘价(跌)<3个开盘价(跌)
                # 3个开盘价(跌)<4个开盘价(跌)
                # 4个开盘价(跌)<5个开盘价(跌)
                # 0个开盘价(跌)<2个开盘价(跌)

                for i in range(nm):
                    if round(zong.iloc[i]['open'],2) <= round(zong.iloc[i+1]['close'],2): 
                        if round(zong.iloc[i+1]['open'],2) <= round(zong.iloc[i+2]['open'],2):
                            if round(zong.iloc[i+2]['open'],2) <= round(zong.iloc[i+3]['open'],2): 
                                if round(zong.iloc[i+3]['open'],2) <= round(zong.iloc[i+4]['open'],2) :
                                    if round(zong.iloc[i+4]['open'],2) <= round(zong.iloc[i+5]['open'],2):      
                                        if round(zong.iloc[i]['open'],2) <= round(zong.iloc[i+2]['open'],2): 

                                            if (zong.iloc[i]['close'] - zong.iloc[i]['open'])/zong.iloc[i]['open'] <= 0:
                                                if (zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] >= 0:
                                                    if (zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] <= 0:
                                                        if (zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] <= 0:
                                                            if (zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] <= 0:
                                                                if (zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] <= 0:
                                                                    if str(code_nm) not in li_code_tmp:
                                                                        li_days_tmp.append(i)
                                                                        li_code_tmp.append(str(code_nm))
                                                                        nu_n=nu_n+1
                del jo, zong
                gc.collect()
                
        nu_nu=nu_nu+1
        print('############共提取'+str(nu_n)+'只股票符合条件############')
    tmp_df=pd.DataFrame({'days':li_days_tmp,'code':li_code_tmp})                 
    return tmp_df

       
def get_5day_picture(n, url, li_code): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        con = requests.get(url.format(str(li_code[nmm])), headers=header, verify=False).json()
        time.sleep(0.1)
        # print(json.dumps(con, sort_keys=True, indent=2))
        li_data=con.get('items')[0].get("items")
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            # jo=jo.sort_values(by="time", ascending=False)
            # print(jo)
            # jo=jo[1:]
            # jo.reset_index(drop = True, inplace=True)
            jo['time']=jo['time']-jo['time'][0]
            quotes=jo.copy()
            
            # quotes=quotes.sort_values(by="time", ascending=False)[:15]
            quotes=quotes.sort_values(by="time", ascending=True)

            quotes['time']=quotes['time'].apply(todate)
            quotes['time']=pd.to_datetime(quotes['time'], format="%Y-%m-%d")

            x = jo['time'].values
            y = jo['price'].values
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
            price_max=jo['price'][maxindex]
            p1_max=p1(time_max)



            # print(jo)
            ax=axes[nu_nu//10, nu_nu%10]
            # count=quotes.shape[0]
            # year=int(count/48)
            # ax.set_title(str(li_code[nmm])+'('+str(year)+')',fontsize=18,fontweight='bold')    
            ax.set_title(str(li_code[nmm]),fontsize=18,fontweight='bold')    
            # plot1=ax.plot(x, y, marker=r'$\clubsuit$', color='goldenrod',markersize=15,label='original values')
            # plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')   
            
            # data_list=[]
            # for row in quotes.itertuples():
            #     date_time = datetime.datetime.strptime(getattr(row,'time'),'%Y-%m-%d')
            #     t = date2num(date_time)
            #     open_tmp = getattr(row,'open')
            #     high_tmp = getattr(row,'high')
            #     low_tmp  = getattr(row,'low')
            #     price_tmp = getattr(row,'price')
            #     datas = (t,open_tmp,high_tmp,low_tmp,price_tmp)
            #     data_list.append(datas)
            
            
            # plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')   
            plot1=ax.plot(jo['time'], jo['price'], 'o', color='goldenrod')#,markersize=10,label='original values')   
            # print(jo)
            # plot=ax.plot(x= 'time', y='price' , data=jo, s=75,  ax=ax)


            # candlestick_ohlc(ax, zip(mdates.date2num(quotes['time'].dt.to_pydatetime()),
            #              quotes['open'], quotes['high'],
            #              quotes['low'], quotes['price']),
            #      width=0.6,colordown='#53c156', colorup='#ff1717')
            

            # if len(quotes["price"].tolist()) >200:
            #     ma150 = moving_average(quotes["price"], 150, type='simple')
            #     ma200 = moving_average(quotes["price"], 200, type='simple')

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
            volume = (quotes.price * quotes.volume) / 1e6  # dollar volume in millions
            vmax = volume.max()
            fillcolor = 'darkgoldenrod'
            poly = ax2t.fill_between(quotes.time.values, volume, 0, label='Volume',
                         facecolor=fillcolor, edgecolor=fillcolor)
            
            ax2t.set_ylim(0, 20 * vmax)
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
    plt.savefig('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_limit/down_data/'+date+"_fig_5day_down_"+str(n)+".png")
    

            
      


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




def get_day_picture(n, url, li_code,days,name): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        con = requests.get(url.format(str(li_code[nmm])), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            quotes=jo.copy()
            
            quotes=quotes.sort_values(by="time", ascending=False)[:15]
            quotes=quotes.sort_values(by="time", ascending=True)

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
            ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)',fontsize=18,fontweight='bold')    
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
            
            ax2t.set_ylim(0, 20 * vmax)
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
    plt.savefig('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_limit/down_data/'+date+"_fig_"+name+"_down_"+str(n)+".png")
    # plt.show()
    












def get_week_picture(n, url, li_code,days,name): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()

    for nmm in range(len(li_code)):
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        con = requests.get(url.format(str(li_code[nmm])), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            quotes=jo.copy()
            
            quotes=quotes.sort_values(by="time", ascending=False)[:15]
            quotes=quotes.sort_values(by="time", ascending=True)

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
            ax.set_title(str(li_code[nmm])+'('+str(days[nmm])+'days)',fontsize=18,fontweight='bold')    
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
                 width=0.9,colordown='#53c156', colorup='#ff1717')
            

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
    plt.savefig('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_limit/down_data/'+date+"_fig_"+name+"_down_"+str(n)+".png")
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
            tmp_df=tmp_df.join(df, how='outer')
            tmp_df.to_csv(fileName,index=False)
        else:
            tmp_df=tmp_df.join(df, how='outer')
            tmp_df.to_csv(fileName,index=False)    
    else:
        df.to_csv(fileName,index=False)
    return True


        
days_df=get_grow_code(url_day,5, li_code)
days_df=days_df.sort_values(by=['days','code'])
codee=days_df.code.tolist()
days=days_df.days.tolist()
# write_li('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_limit/down_data/'+date+'_down_code.txt',codee)
write_csv('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_limit/down_data/record.csv',days_df)

# codee=li_code[:1000]
for i in range((len(codee)//100)+1):
    start=i*100 
    end=(i+1)*100
    if end >= len(codee):
        end = len(codee)  
    code_tmp=codee[start:end]
    days_tmp=days[start:end]
    get_day_picture(i, url_day, code_tmp, days_tmp,'day')
    time.sleep(0.2)
    # get_week_picture(i, url_week, code_tmp, days_tmp,'week')
    get_5day_picture(i, url_5day, code_tmp)

















