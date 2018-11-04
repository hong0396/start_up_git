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
'Authorization': 'Bearer Z89Q8bh5q4WSrYeLQhOUF2cyLHv7k3',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


code=pd.read_csv('2018-10-13us_all_code.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()

# li_code=li_code[:10]
# code=code[:10]


url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'




def get_grow_code(url, li_code): 
    # fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    li_code_tmp=[]
    li_num_tmp=[] 
    nu_nu=0
    nu_n=0 
    for code_nm in li_code:
        print('------------------------从第'+str(nu_nu)+'只股票提取-----------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header,verify=False).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            # jo=jo.sort_values(by="time", ascending=False)
            if len(jo.time.tolist()) > 30:
                zong=jo.sort_values(by="time", ascending=False)[:30]
                # # 0个开盘价(跌)<1个收盘价(涨)
                # # 1个开盘价(涨)<2个开盘价(跌)
                # 2个开盘价(跌)<3个开盘价(跌)
                # 3个开盘价(跌)<4个开盘价(跌)
                # 4个开盘价(跌)<5个开盘价(跌)
                # 0个开盘价(跌)<2个开盘价(跌)

                for i in range(5):
                    # if round(zong.iloc[i]['open'],2) <= round(zong.iloc[i+1]['close'],2): 
                    #     if round(zong.iloc[i+1]['open'],2) <= round(zong.iloc[i+2]['open'],2):
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
                                                                        li_code_tmp.append(str(code_nm))
                                                                        nu_n=nu_n+1
                del jo, zong
                gc.collect()
                
        nu_nu=nu_nu+1
        print('+++++共提取'+str(nu_n)+'只股票符合条件++++')            
    return li_code_tmp


            
      


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




def get_laohu_analysis(n, url, li_code): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame()   
    for code_nm in li_code:
        print('--------------------------------------'+str(nu_nu+(n*100))+'----------------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header,verify=False).json()
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


            ax=axes[nu_nu//10, nu_nu%10]
            count=quotes.shape[0]
            year=int(count/48)
            ax.set_title(str(code_nm)+'('+str(year)+')',fontsize=18,fontweight='bold')    
           
            
            candlestick_ohlc(ax, zip(mdates.date2num(quotes['time'].dt.to_pydatetime()),
                         quotes['open'], quotes['high'],
                         quotes['low'], quotes['close']),
                 width=0.6,colordown='#53c156', colorup='#ff1717')
            
        
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

        
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_no_limit/down_data/'+date+"_fig_down_price_"+str(n)+".png")
    # plt.show()
    
            
def write_li(fileName,li):
       fp = open(fileName,'w+')      
       for i in range(len(li)):
           fp.write(str(li[i])+'\n')
       fp.close()
       return True

        
codee=get_grow_code(url_day, li_code)
write_li('D:/Git/us_stock/technical_analysis/Main/down/4down1up1down_no_limit/down_data/'+date+'_down_code.txt',codee)
# codee=li_code[:1000]
for i in range((len(codee)//100)+1):
    start=i*100 
    end=(i+1)*100
    if end >= len(codee):
        end = len(codee)  
    tmp=codee[start:end]
    get_laohu_analysis(i, url_day, tmp)


















