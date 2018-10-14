import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import tushare as ts

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])
headers={
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Authorization': 'Bearer MJzA2xsEL5wkh0s8DjRd2Cr7WgZXu6gY15soFmLceWW0zw5QmD',
'Connection': 'keep-alive',
'Host': 'hq.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quote/PDD/finance',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}



# code=pd.read_csv('D:\\Git\\us_stock\\profit\\2018-07-15_us_basic.csv',encoding='gbk')                
# li_code=code['code'].tolist()
# print(li_code)



dic={}
codd=[]
profit201806 =[]
profit201803 =[]
profit201712 =[]
profit201709 =[]

li_sum=[profit201806,profit201803,profit201712,profit201709]
li_time=['2018-06','2018-03','2017-12','2017-09']

code=pd.read_csv('D:/Git/us_stock/laohu/basic_code/2018-09-21us_all_code.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()
# for i in range(len(li_code)):
#     li_code[i] = str(li_code[i]).replace('hk','')
# print(li_code)

nu_nuu=0
for code_nm in li_code:
    print('------------------------------------------'+str(nu_nuu)+'----------------------------------------------')
    url='https://hq.itiger.com/fundamental/usstock/earnings/income/'+code_nm+'?type=income&symbol='+code_nm+'&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
    time.sleep(0.1)
    res=requests.get(url, headers=headers)
    if res.status_code == 200:
        a=res.json()
        li=a.get('data').get('page')
        li_h=a.get('data').get('header')
        # print(li_h[7])
        num=2018
        num_income=2018
        for w in range(len(li_time)):
            li_sum[w].append('0_0_0_0')


        if not li_h is None:
            for h in range(len(li_h)):
                if li_h[h].get('name') ==  "净利润":
                    num=h
                if li_h[h].get('name') ==  "主营业务收入":
                    num_income=h


        

        if num != 2018: 
            if not li is None:
                # codd.append(code_nm)
                for i in range(len(li)):
                    if li[i].get('type') == '季报':
                        year_date=li[i].get('date')[:7]
                        tmmp=li[i].get('cell')
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

                        for k in range(len(li_time)):
                            if year_date in li_time[k]:
                                li_sum[k][nu_nuu]=str(value)+'_'+yoy+'_'+str(value_income)+'_'+yoy_income

                #                 index_num=li_sum[k].index(value)
                # for w in range(len(li_time)):
                #     if  index_num +1 == len(li_sum[w]):
                #         li_sum[w].append('0')
            # else:
            #     for w in range(len(li_time)):
            #         li_sum[w].append('0')


            # for w in range(len(li_time)):
            #     print(li_sum[w])
          
    else:
        print('下载数据错误')
    nu_nuu=nu_nuu+1


pdd=pd.DataFrame(li_sum,  index=li_time)
pan=pdd.T
print(pan)
for i in li_time:
    col1='net'+i
    col2='net_radio'+i
    col3='income'+i
    col4='income_radio'+i
    pan[col1] = pan[i].map(lambda x:x.split('_')[0])
    pan[col2] = pan[i].map(lambda x:x.split('_')[1])
    pan[col3] = pan[i].map(lambda x:x.split('_')[2])
    pan[col4] = pan[i].map(lambda x:x.split('_')[3])



pan['code'] = li_code
re=pd.merge(code,pan,how='outer',on='code')
re=re.drop_duplicates()
re.to_csv(date+'_Laohu_us_profit_income_quarter.csv', encoding = 'gbk',index=False)


















# def get_profit(code):
#     global nu_nu
#     print('--------------------------'+str(nu_nu)+'--------------------------------')
#     url='https://hq1.itiger.com/fundamental/usstock/earnings/income/'+code+'?type=income&symbol=WFC&deviceId'+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
#     res=requests.get(url, headers=headers)
#     a=res.json()
#     li=a.get('data').get('page')
#     li_h=a.get('data').get('header')
#     num=37
#     # print(li_h)
#     if not li_h is None:
#         for h in range(len(li_h)):
#             if li_h[h].get('name') ==  "净利润":
#                 num=h
#     time.sleep(0.5)
#     url='https://hq1.itiger.com/fundamental/usstock/earnings/balance/'+code+'?type=balance&symbol=WFC&deviceId='+ti+'&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
#     res=requests.get(url, headers=headers)
#     a=res.json()
#     li_s=a.get('data').get('page')
#     li_s_h=a.get('data').get('header')
#     num_s=59
#     if not li_s_h is None:
#         for g in range(len(li_s_h)):
#             if li_s_h[g].get('name') == "股东权益合计" :
#                 num_s=g
#     li_di=[]
    
#     for p in li_sum:
#         p.append(0)
#     if not li_s is None:
#         for i in range(min(len(li_s),len(li))):
#     # if i.get('type') == '季报':
# 	   #  print(i.get('date'))
# 	   #  print(i.get('cell')[59])
#     #     # value=i.get('cell')[37].get('value')
#         # if li[i].get('type') == '年报':
#         #     if li_s[i].get('type') == '年报' :
#             if li[i].get('date') == li_s[i].get('date') :   
#                 for m in range(len(li_time)):
#                     if  li[i].get('date') == li_time[m] :  
#                         if not li[i].get('cell')[num].get('value') is None:
#                             u_tmp=li[i].get('cell')[num].get('value')                                            
#                             if '亿' in u_tmp:
#                                 u_tmp=u_tmp.replace('亿','').replace(',','')
#                                 u=float(u_tmp)*100000000
#                             elif '万' in u_tmp:
#                                 u_tmp=u_tmp.replace('万','').replace(',','')
#                                 u=float(u_tmp)*10000
#                             elif '千' in u_tmp:
#                                 u_tmp=u_tmp.replace('千','').replace(',','')
#                                 u=float(u_tmp)*1000
#                             else:
#                                 u=u_tmp.replace(',','')
#                             if not li_s[i].get('cell')[num_s].get('value') is None:  
#                                 d_tmp=li_s[i].get('cell')[num_s].get('value')                                          
#                                 if '亿' in d_tmp:
#                                     d_tmp=d_tmp.replace('亿','').replace(',','')
#                                     d=float(d_tmp)*100000000
#                                 elif '万' in d_tmp:
#                                     d_tmp=d_tmp.replace('万','').replace(',','')
#                                     d=float(d_tmp)*10000
#                                 elif '千' in d_tmp:
#                                     d_tmp=d_tmp.replace('千','').replace(',','')
#                                     d=float(d_tmp)*1000
#                                 else:
#                                     d=d_tmp.replace(',','')

#                                 if float(d) != 0.0:
                                   
#                                     li_sum[m][nu_nu]=round(float(u)/float(d),4)
#     nu_nu=nu_nu+1
#                     # print(result)
#                     # if da in dic:
#                     #     dic[da].append(result)
#                     # else:
#                     #     dic[da]=[]
#                     #     dic[da].append(result)    


# for k in li_code:
#     get_profit(k)
# # print(li_sum)
# pdd=pd.DataFrame(li_sum,   columns=li_code , index=[ '2014-12-31','2015-12-31','2016-12-31','2017-12-31'])
# pan=pdd.T
# pan['code'] = li_code
# re=pd.merge(code,pan,how='outer',on='code')
# re.to_csv('Laohu_us_profit.csv', encoding = 'gbk',index=False)













































