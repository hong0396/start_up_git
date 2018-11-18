import requests
import pandas as pd
import time
import gc 
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

def todate(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))

headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
,'Accept-Encoding': 'gzip, deflate, br'
,'Accept-Language': 'zh-CN,zh;q=0.9'
,'Cache-Control': 'max-age=0'
,'Cookie': r'FUTU_TOOL_STAT_UNIQUE_ID=15424227214619448; UM_distinctid=1671f8ef5bed2-0b4123a4c75918-3a3a5c0e-1fa400-1671f8ef5bf87a; cipher_device_id=1542422722481133; uid=2266118; web_sig=64Clg85dHGv2H6ss1mfeF2iUkRavkfjn6Utnt35KOOJ5mkSnat%2B6QS9xkqFAJprPyy%2FhP3RpB8Fe%2BVjMFYoCQqcYiXSAC%2FsB2rVmlUDaKvbhYHCuDfKeTXRg57RjVtYI; ci_sig=2gpjUN0tSSdeshqJPH1VwBamzOJhPTEwMDAwNTM4JmI9MjAxMTM2Jms9QUtJRENXblN2cWJ4UDkza3lYdW55ZTNNYXVJUWp2angydFlEJmU9MTU0NTAxOTM4NSZ0PTE1NDI0MjczODUmcj0yODAxNTIxODUmdT0mZj0%3D; PHPSESSID=dk2dnae18t0ii72iu79ibij9p6; CNZZDATA1256186977=1776778979-1542421393-https%253A%252F%252Fwww.futu5.com%252F%7C1542426793; tgw_l7_route=7587343559275141d1207d24944b360a'
,'Host': 'www.futunn.com'
,'Upgrade-Insecure-Requests': '1'
,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

allcol=pd.read_csv('all.csv', encoding='GB18030')
code=allcol.loc[:,['security_id','security_code']]
# code=code[100:200]

print(code)

url='https://www.futunn.com/quote/kline-v2?security_id={}&type=2&from=&_=1542429895594'
def get_grow_code(url, code): 
    li=[]
    li_code_tmp=[]
    li_days_tmp=[]
    li_id_tmp=[]
    li_num_tmp=[] 
    nu_nu=0
    nu_n=0 
    for row in code.itertuples():
        r = requests.get(url.format(str(getattr(row, 'security_id'))),headers=headers,verify=True).json()
        print('-----------------------从第'+str(nu_nu)+'只股票提取------------------------------------')
        time.sleep(0.15)
        df=pd.DataFrame(r.get("data").get("list"))
        if 'c' in df.columns.tolist():
            df.rename(columns={'c':'close','o':'open','h':'high','l':'low','k':'time','v':'volume'}, inplace=True)    
            df['close']=df['close']/1000
            df['open']=df['open']/1000
            df['high']=df['high']/1000
            df['low']=df['low']/1000
            df['volume']=df['volume']/10000
            # print(df['time'])
            # df.to_csv('tmp.csv',index=False, encoding='gbk')
            jo=df.copy()
            if len(jo.time.tolist()) > 30:
                zong=jo.sort_values(by="time", ascending=False)[:30]
                # 0个开盘价(涨)>1个开盘价(涨)
                # 1个开盘价(涨)>2个开盘价(涨)
                # 2个开盘价(涨)>3个开盘价(涨)
                
                # 0个最低价(涨)>1个最低价(涨)
                # 1个最低价(涨)>2个最低价(涨)
                # 2个最低价(涨)>3个最低价(涨)              

                for i in range(5):
                    if round(zong.iloc[i]['open'],2) >= round(zong.iloc[i+1]['open'],2): 
                        if round(zong.iloc[i+1]['open'],2) >= round(zong.iloc[i+2]['open'],2):
                            if round(zong.iloc[i+2]['open'],2) >= round(zong.iloc[i+3]['open'],2): 
                                
                                if round(zong.iloc[i]['low'],2) >= round(zong.iloc[i+1]['low'],2):
                                    if round(zong.iloc[i+1]['low'],2) >= round(zong.iloc[i+2]['low'],2): 
                                        if round(zong.iloc[i+2]['low'],2) >= round(zong.iloc[i+3]['low'],2): 

                                            if (zong.iloc[i]['close'] - zong.iloc[i]['open'])/zong.iloc[i]['open'] > 0:
                                                if (zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] > 0:
                                                    if (zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] > 0:
                                                        if (zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] > 0:
                                                            # if (zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] >= 0:
                                                            #     if (zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] >= 0:
                                                                    if str(getattr(row, 'security_code')) not in li_code_tmp:
                                                                        li_days_tmp.append(i)
                                                                        li_id_tmp.append(str(getattr(row, 'security_id')))
                                                                        li_code_tmp.append(str(getattr(row, 'security_code')))
                                                                        nu_n=nu_n+1
                del jo, zong
                gc.collect()
            del df
            gc.collect()
            

            nu_nu=nu_nu+1
            print('***********共提取'+str(nu_n)+'只股票符合条件***********')  
    tmp_df=pd.DataFrame({'code_id':li_id_tmp,'days':li_days_tmp,'code':li_code_tmp})    
    return tmp_df

def get_picture(n, url, code): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    # jo=pd.DataFrame()
    quotes=pd.DataFrame()
   
    for row in code.itertuples():
        r = requests.get(url.format(str(getattr(row, 'code_id'))),headers=headers,verify=True).json()
        print('------------------------------------'+str(nu_nu+(n*100))+'------------------------------------------')
        time.sleep(0.15)
        df=pd.DataFrame(r.get("data").get("list"))
        if 'c' in df.columns.tolist():
            df.rename(columns={'c':'close','o':'open','h':'high','l':'low','k':'time','v':'volume'}, inplace=True)    
            df['close']=df['close']/1000
            df['open']=df['open']/1000
            df['high']=df['high']/1000
            df['low']=df['low']/1000
            df['volume']=df['volume']/10000
            # df.to_csv('tmp.csv',index=False, encoding='gbk')
            jo=df.copy()
            quotes=df.copy()
            
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
            ax.set_title(str(getattr(row, 'code'))+'('+str(getattr(row, 'days'))+'days)',fontsize=18,fontweight='bold')    
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
    plt.savefig(date+"_fig_up_"+str(n)+".png")
    # plt.show()
 

days_df=get_grow_code(url, code)
# print(days_df)
days_sort_df=days_df.sort_values(by=['days','code'])

for i in range((len(days_sort_df)//100)+1):
    start=i*100 
    end=(i+1)*100
    if end >= len(days_sort_df):
        end = len(days_sort_df)  
    code_tmp=days_sort_df[start:end]
    get_picture(i, url, code_tmp)




