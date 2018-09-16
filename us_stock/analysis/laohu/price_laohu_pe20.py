
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
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
'Authorization': 'Bearer c6Sw3I4Vu3uNivRgU5tYvBhDyZwOZR',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


code=pd.read_csv('D:\\Git\\us_stock\\analysis\\pe20_net.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()

# li_code=li_code[:10]
# code=code[:10]


url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url='https://hq.itiger.com/stock_info/candle_stick/month/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'




def get_laohu_analysis(n, url, li_code): 
    fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    nu_nu=0    
    for code_nm in li_code:
        print('------------------------------------------'+str(nu_nu+(n*100))+'----------------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            jo=pd.DataFrame(li_data)
            # print(jo)
            ax=axes[nu_nu//10, nu_nu%10]
            ax.set_title(str(code_nm),fontsize=18,fontweight='bold')    
            g=sns.relplot(x= 'time', y='close' , data=jo, s=75,  ax=axes[nu_nu//10, nu_nu%10 ])
            ax.xaxis.set_major_locator(ticker.NullLocator())
            ax.set_ylabel(' ', fontsize=0.01)
            ax.set_xlabel(' ', fontsize=0.01)
            ax.spines['top'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['left'].set_linewidth(2)
            ax.spines['right'].set_linewidth(2)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)
            # ax2 = ax.twinx()
            # g1=sns.barplot(x= 'time', y='volume' , data=jo,  ax=ax2)         
            # ax.xaxis.set_major_formatter(ticker.NullLocator())
            # plt.xticks([])
            plt.close(g.fig)         
        nu_nu=nu_nu+1    
    fig.tight_layout(rect=[0.02,0.02,0.98,0.98], pad=0.2, h_pad=0.2, w_pad=0.2)
    fig.subplots_adjust(wspace =0.2, hspace =0.2)
    plt.savefig("fig_pe20_"+str(n)+".png")
    # plt.show()
    
            
        


def get_laohu_price(url,li_code):
    li=[]
    nu_nu=0
    for code_nm in li_code:
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
        dic_tmp['mean']=0
        dic_tmp['std']=0
        dic_tmp['max']=0
        dic_tmp['min']=0
        dic_tmp['start']=0
        dic_tmp['end']=0
        dic_tmp['year']=0
        dic_tmp['price_start']=0
        dic_tmp['price_middle']=0
        dic_tmp['price_end']=0
        dic_tmp['volume_start']=0
        dic_tmp['volume_end']=0
        if li_data is not None:
            jo=pd.DataFrame(li_data)
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
            dic_tmp['count']=count
            dic_tmp['mean']=meam_tmp
            dic_tmp['std']=std_tmp
            dic_tmp['max']=max
            dic_tmp['min']=min
            dic_tmp['start']=startprice
            dic_tmp['end']=endd
            dic_tmp['year']=year
            dic_tmp['price_start']=price_start
            dic_tmp['price_middle']=price_middle
            dic_tmp['price_end']=price_end
            dic_tmp['volume_start']=vol_start
            dic_tmp['volume_end']=vol_end
            li.append(dic_tmp)
        nu_nu=nu_nu+1
    datatable=pd.DataFrame(li)
    return datatable




for i in range((len(li_code)//100)+1):
    start=i*100 
    end=(i+1)*100
    if end >= len(li_code):
        end = len(li_code)  
    tmp=li_code[start:end]
    get_laohu_analysis(i, url, tmp)












# re=pd.merge(code,pan,how='outer',on='code')
# re=re.drop_duplicates()
# re.to_csv(date+'_Laohu_us_analysis.csv', encoding = 'gbk',index=False)

