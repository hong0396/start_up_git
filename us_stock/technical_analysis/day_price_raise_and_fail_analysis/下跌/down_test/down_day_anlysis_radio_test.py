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


# code=pd.read_csv('2018-10-21us_all_code.csv',encoding='gbk')              
# li_code=code['code'].tolist()
# li_code=li_code[:50]



url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'




def get_grow_code(url, li_code): 
    # fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    li_code_tmp=[]
    li_num_tmp=[]
    li_0_tmp=[]  
    li_5_tmp=[]
    li_10_tmp=[]
    li_5_radio=[]
    li_10_radio=[]
    nu_nu=0
    nu_n=0 
    for code_nm in li_code:
        print('------------------------从第'+str(nu_nu)+'只股票提取-----------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            x = jo['time'].apply(todate).tolist()
            y_close = jo['close'].tolist()
            y_open = jo['open'].tolist()

            if len(jo.time.tolist()) > 250:
                zong=jo.sort_values(by="time", ascending=False)[:250]
                # 第0个开盘价(涨)>1个收盘价(跌)
                # 1个开盘价(跌)>2个开盘价(涨)>3个开盘价(涨)>4个开盘价(涨)>5个开盘价(涨)

                for i in range(0, 210):
                    # if round(zong.iloc[i]['open'],2) >= round(zong.iloc[i+1]['close'],2): 
                    # if round(zong.iloc[i+1]['open'],2) >= round(zong.iloc[i+2]['open'],2):
                    # if round(zong.iloc[i]['close'],2) >= round(zong.iloc[i+2]['close'],2):
                        # if round(zong.iloc[i]['open'],2) <= round(zong.iloc[i+2]['open'],2):
                            if round(zong.iloc[i+1]['open'],2) <= round(zong.iloc[i+2]['open'],2):
                                if round(zong.iloc[i+2]['open'],2) <= round(zong.iloc[i+3]['open'],2):
                                    if round(zong.iloc[i+3]['open'],2) <= round(zong.iloc[i+4]['open'],2):      
                                        
                                        if (zong.iloc[i]['close'] - zong.iloc[i]['open'])/zong.iloc[i]['open'] >= 0:
                                            if (zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] <= 0:
                                                if (zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] <= 0:
                                                    if (zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] <= 0:
                                                        if (zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] <= 0:
                               
                                                                
                                                                li_code_tmp.append(str(code_nm))
                                                                li_num_tmp.append(zong.iloc[i+4]['time'])
                                                                li_0_tmp.append(zong.iloc[i]['close'])
                                                                if zong.iloc[i-5]['close']:
                                                                    li_5_tmp.append(zong.iloc[i-5]['close'])
                                                                    li_567_avg=(zong.iloc[i-2]['close']+zong.iloc[i-3]['close']+zong.iloc[i-4]['close'])/3
                                                                    # li_5_radio.append((zong.iloc[i-5]['close']-zong.iloc[i]['close'])/zong.iloc[i]['close'])
                                                                    li_5_radio.append((li_567_avg - zong.iloc[i]['close'])/zong.iloc[i]['close'])
                                                                else:
                                                                    li_5_tmp.append(0)
                                                                    li_5_radio.append(0)
                                                                if zong.iloc[i-10]['close']:
                                                                    li_10_tmp.append(zong.iloc[i-10]['close'])
                                                                    li_10_radio.append((zong.iloc[i-10]['close']-zong.iloc[i]['close'])/zong.iloc[i]['close'])
                                                                else:
                                                                    li_10_tmp.append(0)
                                                                    li_10_radio.append(0)
                                                                # li_10_tmp.append(zong.iloc[i-10]['close']) 
                                                                # li_10_radio.append((zong.iloc[i-10]['close']-zong.iloc[i]['close'])/zong.iloc[i]['close'])   
                                                                nu_n=nu_n+1
                del jo, zong
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
        print('+++++共提取'+str(nu_n)+'只股票符合条件++++') 
       
    tmp_df=pd.DataFrame({'code': li_code_tmp ,  'starttime': li_num_tmp,'li_0_tmp':li_0_tmp, 'li_5_tmp':li_5_tmp,'li_10_tmp':li_10_tmp,'li_5_radio':li_5_radio,'li_10_radio' :li_10_radio })               
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




def get_laohu_analysis(n, url, pd_code,name): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0
    jo=pd.DataFrame()
    quotes=pd.DataFrame() 
    li_code_tmp=pd_code.code.tolist()
    li_starttime_tmp=pd_code.starttime.tolist()    
    for num in range(len(li_code_tmp)):
        print('--------------------------------------'+str(nu_nu+(n*100))+'----------------------------------------------')
        time.sleep(0.1) 
        con = requests.get(url.format(str(li_code_tmp[num])), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            
            time_tmpp=li_starttime_tmp[num]
            quotes=jo[jo.time>=time_tmpp][:31]

            


            quotes['time']=quotes['time'].apply(todate)
            quotes['time']=pd.to_datetime(quotes['time'], format="%Y-%m-%d")

            


            # x = jo['time'].values
            # y = jo['close'].values
            # vol = jo['volume'].values
            # vol_li = jo['volume'].tolist()
            # vol_min=min(vol_li)
            # vol_max=max(vol_li)
            # vol_up=(vol_max-vol_min)*0.3+vol_max
            # z1 = np.polyfit(x, y, 4)#用3次多项式拟合
            # p1 = np.poly1d(z1)
            # # print(p1) #在屏幕上打印拟合多项式
            # yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
            # der=p1.deriv(m=2)
            # dder=der(x)
            # dder_list = dder.tolist()
            # maxindex=dder_list.index(max(dder_list))
            # # print(maxindex)
            # time_max=jo['time'][maxindex]
            # close_max=jo['close'][maxindex]
            # p1_max=p1(time_max)



            # print(jo)
            ax=axes[nu_nu//10, nu_nu%10]
            count=quotes.shape[0]
            year=int(count/48)
            ax.set_title(str(li_code_tmp[num])+'('+str(year)+')',fontsize=18,fontweight='bold')    
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
                         width=0.65,colorup='red',colordown='darkgreen')
            

            # if len(quotes["close"].tolist()) >200:
            #     ma150 = moving_average(quotes["close"], 150, type='simple')
            #     ma200 = moving_average(quotes["close"], 200, type='simple')

            #     linema150, = ax.plot(quotes['time'], ma150, color='blue', lw=2, label='MA (150)')
            #     linema200, = ax.plot(quotes['time'], ma200, color='red', lw=2, label='MA (200)')


            # mpf.candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='green')
        
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            # ax.set_xlabel(' ', fontsize=0.01)
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
    plt.savefig(date+"_"+name+"_"+str(n)+".png")
    # plt.show()
    
            
def write_li(fileName,li):
       fp = open(fileName,'w+')      
       for i in range(len(li)):
           fp.write(str(li[i])+'\n')
       fp.close()
       return True


def get_picture(url_day,select_code,name):
	codee=select_code.code.tolist()
	for i in range((len(codee)//100)+1):
	    start=i*100 
	    end=(i+1)*100
	    if end >= len(codee):
	        end = len(codee)  
	    tmp=select_code[start:end]
	    time.sleep(0.1) 
	    get_laohu_analysis(i, url_day, tmp,name)


def hist(series):
    # ax = sns.distplot(series,rug=True, hist=False)
    ax = sns.distplot(series)
    plt.show()

code=pd.read_csv('2018-10-13us_all_code_2.csv',encoding='gbk')              
li_code=code['code'].tolist()
nq=500
li_code=random.sample(li_code, nq)
       
select_code=get_grow_code(url_day, li_code)
# codee=select_code.code.tolist()
# select=select_code.copy()
# select['starttime']=select['starttime'].apply(todate)
# select.to_csv(date+'_up_code_date_radio_test.csv')
# select_code.to_csv(date+'_up_code_time_radio_test.csv')
up_5_num=len(select_code[select_code['li_5_radio']>0].li_5_radio.tolist())
down_5_num=len(select_code[select_code['li_5_radio']<0].li_5_radio.tolist())


hist(select_code.li_5_radio)

print('上涨的数目为'+str(up_5_num))
print('下跌的数目为'+str(down_5_num))
print('下跌比例为'+ '%.6f%%' % (down_5_num/(up_5_num+down_5_num)))

file = r'test_log.txt'
with open(file, 'a+') as f:
    f.write('----------------------------------------'+'\n')
    f.write('4跌1涨1跌  5跌开盘价递减：'+'\n') 
    f.write('测试样本'+str(nq)+'\n')  
    f.write('上涨的数目为'+str(up_5_num)+'\n') 
    f.write('下跌的数目为'+str(down_5_num)+'\n')
    f.write('下跌比例为'+ '%.6f%%' % (down_5_num/(up_5_num+down_5_num))+'\n')
    f.write('----------------------------------------'+'\n') 
# get_picture(url_day,select_code[select_code['li_5_radio']>0],'fig_5up_radio_test')
# time.sleep(0.1) 
# get_picture(url_day,select_code[select_code['li_5_radio']<0],'fig_5down_radio_test')





































































































































































# re=pd.merge(code,pan,how='outer',on='code')
# re=re.drop_duplicates()
# re.to_csv(date+'_Laohu_us_analysis.csv', encoding = 'gbk',index=False)

