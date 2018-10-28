import pandas as pd
import numpy as np 
import datetime
import time
import xarray as xr
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
from sqlalchemy import create_engine
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.linear_model import LassoCV 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from  sklearn.metrics  import  average_precision_score 
from sklearn.metrics import r2_score  
import csv
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
from sqlalchemy import create_engine
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from  sklearn.metrics  import  average_precision_score 
from sklearn.metrics import r2_score  
from xgboost import XGBRegressor
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_iris
from sklearn.svm import SVC
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import pickle
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


code=pd.read_csv('2018-10-13us_all_code.csv',encoding='gbk')                
li_code=code['code'].tolist()
# li_code=['SCOR','TBRG','MPAC','PRQR','LEJU','ICL','TBC','SPAQ','USFR']



url_week='https://hq.itiger.com/stock_info/candle_stick/week/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
url_day='https://hq.itiger.com/stock_info/candle_stick/day/{}?beginTime=-1&endTime=-1&right=br&limit=251&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'




def get_grow_code(url, li_code): 
    # fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(30,30))
    li=[]
    li_code_tmp=[]
    li_0grow_tmp=[]
    li_1grow_tmp=[]
    li_2grow_tmp=[]
    li_3grow_tmp=[]
    li_4grow_tmp=[]
    li_5grow_tmp=[]
    li_1up_tmp=[]
    li_2up_tmp=[]
    li_3up_tmp=[]
    li_4up_tmp=[]
    li_5up_tmp=[]
    nu_nu=0
    nu_n=0 
    for code_nm in li_code:
        print('------------------------从第'+str(nu_nu)+'只股票提取-----------------------------------------')
        con = requests.get(url.format(str(code_nm)), headers=header).json()
        time.sleep(0.1) 
        li_data=con.get('items')
        if li_data is not None:
            zong=pd.DataFrame(li_data)
            zong=zong.sort_values(by='time', ascending=False) 
            if len(zong) > 10:
                for i in range(5):
                    if round(zong.iloc[i]['open'],2) <= round(zong.iloc[i+2]['open'],2):
                            if round(zong.iloc[i+2]['open'],2) <= round(zong.iloc[i+3]['open'],2):
                                if round(zong.iloc[i+3]['open'],2) <= round(zong.iloc[i+4]['open'],2):
                                    # if round(zong.iloc[i+4]['open'],2) <= round(zong.iloc[i+5]['open'],2):   

                                        if (zong.iloc[i]['close'] - zong.iloc[i]['open'])/zong.iloc[i]['open'] <= 0:
                                            if (zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] >= 0:
                                                if (zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] <= 0:
                                                    if (zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] <= 0:
                                                        if (zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] <= 0:
                                                            if (zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] <= 0:

                                                                    li_code_tmp.append(str(code_nm))
                                                                    # print(str(code_nm))
                                                                    # print(str(i))
                                                                    # print(zong.iloc[i+0]['close'] )
                                                                    # print(zong.iloc[i+0]['open'] )
                                                                    li_0grow_tmp.append((zong.iloc[i+0]['close'] - zong.iloc[i+0]['open'])/zong.iloc[i+0]['open'] )
                                                                    li_1grow_tmp.append((zong.iloc[i+1]['close'] - zong.iloc[i+1]['open'])/zong.iloc[i+1]['open'] )
                                                                    li_2grow_tmp.append((zong.iloc[i+2]['close'] - zong.iloc[i+2]['open'])/zong.iloc[i+2]['open'] )
                                                                    li_3grow_tmp.append((zong.iloc[i+3]['close'] - zong.iloc[i+3]['open'])/zong.iloc[i+3]['open'] )
                                                                    li_4grow_tmp.append((zong.iloc[i+4]['close'] - zong.iloc[i+4]['open'])/zong.iloc[i+4]['open'] )
                                                                    li_5grow_tmp.append((zong.iloc[i+5]['close'] - zong.iloc[i+5]['open'])/zong.iloc[i+5]['open'] )
                                                                    li_1up_tmp.append((zong.iloc[i+1]['open'] - zong.iloc[i]['close'])/zong.iloc[i]['close']) 
                                                                    li_2up_tmp.append((zong.iloc[i+2]['open'] - zong.iloc[i+1]['close'])/zong.iloc[i+1]['close']) 
                                                                    li_3up_tmp.append((zong.iloc[i+3]['open'] - zong.iloc[i+2]['close'])/zong.iloc[i+2]['close']) 
                                                                    li_4up_tmp.append((zong.iloc[i+4]['open'] - zong.iloc[i+3]['close'])/zong.iloc[i+3]['close'])
                                                                    li_5up_tmp.append((zong.iloc[i+5]['open'] - zong.iloc[i+4]['close'])/zong.iloc[i+4]['close'])
                                                                    nu_n=nu_n+1             
        nu_nu=nu_nu+1
        print('+++++共提取'+str(nu_n)+'只股票符合条件++++')            
    tmp_df=pd.DataFrame({'code': li_code_tmp,'li_0grow_tmp': li_0grow_tmp,
    'li_1grow_tmp': li_1grow_tmp,'li_2grow_tmp': li_2grow_tmp,
    'li_3grow_tmp': li_3grow_tmp,'li_4grow_tmp': li_4grow_tmp,
    'li_5grow_tmp': li_5grow_tmp, 'li_1up_tmp': li_1up_tmp,
    'li_2up_tmp': li_2up_tmp, 'li_3up_tmp': li_3up_tmp,
    'li_4up_tmp': li_4up_tmp, 'li_5up_tmp': li_5up_tmp})
    return tmp_df
  

            
def write_li(fileName,li):
       fp = open(fileName,'w+')      
       for i in range(len(li)):
           fp.write(str(li[i])+'\n')
       fp.close()
       return True



#提取当天的基础数据并保存      
codee=get_grow_code(url_day, li_code)
codee.to_csv(date+'_down_day_basic_data.csv',index=False)

#模型数据初处理
codee=codee[codee!=0]
codee=codee.dropna()


#删除code
day_data=codee.drop(['code'], axis = 1)


#模型预测
clf = joblib.load('2018-10-28down_model.joblib') 
y_predst=clf.predict(day_data)

codee['predict']=y_predst
codee.to_csv(date+'_down_day_last_data.csv',index=False)







