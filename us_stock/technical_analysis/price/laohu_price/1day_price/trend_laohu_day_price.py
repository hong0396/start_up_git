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
'Authorization': 'Bearer Wl5MAbeUAUWRMACTKF2s1a9uwOPlqp',
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


url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20181013_838484&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20181013_838484&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'




def get_grow_code(url, li_code): 
    # fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    li_code_tmp=[] 
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
            if '2018-10-10' in x: 
                index_x=x.index('2018-10-10')
                if y_open[index_x] >0:
                    if (y_close[index_x] - y_open[index_x])/y_open[index_x] >0.01:
                        li_code_tmp.append(str(code_nm))
                        nu_n=nu_n+1
        #     z1 = np.polyfit(x, y, 4)#用3次多项式拟合
        #     p1 = np.poly1d(z1)
        #     # print(p1) #在屏幕上打印拟合多项式
        #     yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
        #     der1=p1.deriv(m=1)
        #     der2=p1.deriv(m=2)
        #     dder1=der1(x)
        #     dder1_list = dder1.tolist()
        #     if dder1_list[-1]>0 and dder1_list[-2]  > 0:
        #         li_code_tmp.append(str(code_nm))
        #         print(code_nm)
        #         # print(dder1_list[-5:])
        #         nu_n=nu_n+1
        #         # dder2=der2(x)
        #         # dder_list = dder2.tolist()
        #         # maxindex=dder_list.index(max(dder_list))
        #         # # print(maxindex)
        #         # time_max=jo['time'][maxindex]
        #         # close_max=jo['close'][maxindex]
        nu_nu=nu_nu+1
        print('+++++共提取'+str(nu_n)+'只股票符合条件++++')            
    return li_code_tmp


            
      















def get_laohu_analysis(n, url, li_code): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0    
    for code_nm in li_code:
        print('--------------------------------------'+str(nu_nu+(n*100))+'----------------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
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
            count=jo.shape[0]
            year=int(count/48)
            ax.set_title(str(code_nm)+'('+str(year)+')',fontsize=18,fontweight='bold')    
            # plot1=ax.plot(x, y, marker=r'$\clubsuit$', color='goldenrod',markersize=15,label='original values')
            plot1=ax.plot(x, y, 'o', color='goldenrod',markersize=10,label='original values')
            # plot1.set_zorder(0)
            # plot1=ax.plot(x, y, 'o', ms=20, lw=2, alpha=1, mfc='goldenrod' , markersize=10,label='original values')
            plot2=ax.plot(x, yvals, color='orangered',linewidth=4,label='polyfit values') 
            # plot2.set_zorder(2)
            ax.annotate(' ', xy=(time_max, p1_max), xytext=(time_max, p1_max),fontsize= 16,arrowprops=dict(facecolor='black', shrink=0.1),)
            # plot2_1=ax.scatter(time_max, p1_max, zorder=10, s=100,color='black')
            plot2_2=ax.plot([time_max, time_max],[p1_max,0], 'k--', lw=2.5)
                       
            # ax.legend(loc=4)
            # g=sns.relplot(x= 'time', y='close' , data=jo, s=75,  ax=axes[nu_nu//10, nu_nu%10 ])
            # ax.annotate(' ', xy=(time_max, close_max), xytext=(time_max, close_max),arrowprops=dict(facecolor='red', frac=0.5,shrink=0.05),)
            
            # ax.annotate(' ', xy=(time_max, p1_max), xytext=(time_max, p1_max),fontsize= 16,arrowprops=dict(facecolor='black', shrink=0.1),)

            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)

            
            ax2 = ax.twinx()
            plot3=ax2.plot(x, vol, zorder=0, c="g",linewidth=2,alpha=0.7)
            ax2.set_zorder(0)
            # ax2.set_ylabel('volume')
            ax2.set_ylim(vol_min,vol_up) 
            ax2.yaxis.set_major_locator(plt.NullLocator()) 


            # ax2 = ax.twinx()
            # g1=sns.barplot(x= 'time', y='volume' , data=jo,  ax=ax2)         
            # ax.xaxis.set_major_formatter(ticker.NullLocator())
            # plt.xticks([])
            # plt.close(plt.fig) 
            # plt.show()         
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig("fig_20181010_price_"+str(n)+".png")
    # plt.show()
    
            
        

codee=get_grow_code(url_day, li_code)

for i in range((len(codee)//100)+1):
    start=i*100 
    end=(i+1)*100
    if end >= len(codee):
        end = len(codee)  
    tmp=codee[start:end]
    get_laohu_analysis(i, url_week, tmp)




















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

