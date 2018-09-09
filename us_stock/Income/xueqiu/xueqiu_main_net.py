
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
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'_ga=GA1.2.703130432.1533452387; device_id=4f08f42f3c284ff8fb023eb3ec131209; s=dp12kzss4l; xq_a_token=9dec42418464c150808cc38189ba5cd21c01cecc; xqat=9dec42418464c150808cc38189ba5cd21c01cecc; xq_r_token=35e3dd9b5bce99386c63ce72b702d45ee73a2feb; xq_is_login=1; u=5396072226; bid=343c77da7db204b06e2badbccc03728a_jkzgnfvl; __utmz=1.1534953544.6.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); xq_token_expire=Mon%20Sep%2017%202018%2023%3A48%3A20%20GMT%2B0800%20(CST); _gid=GA1.2.1981878488.1535121502; __utma=1.703130432.1533452387.1534953544.1535177050.7; aliyungf_tc=AQAAAC9w6UNNIQsAbIyctLg+Y9gvY8cM; __utmc=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1535121502,1535177050,1535177540,1535177945; __utmb=1.14.8.1535178264948; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1535178308',
'Host':'xueqiu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# code=pd.read_csv('D:\\Git\\us_stock\\profit\\2018-07-15_us_basic.csv',encoding='gbk')                
# li_code=code['code'].tolist()
# print(li_code)


dic={}
codd=[]
net201806 =[]
net201803 =[]
net201712 =[]
net201709 =[]
net201706 =[]
net201703 =[]
net201612 =[]
net201609 =[]
li_sum=[net201806,net201803,net201712,net201709,net201706,net201703,net201612,net201609]
li_time=['2018-06','2018-03','2017-12','2017-09','2017-06','2017-03','2016-12','2016-09']

code=pd.read_csv('D:\\Git\\us_stock\\ROE\\2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()
# for i in range(len(li_code)):
#     li_code[i] = str(li_code[i]).replace('hk','')
# print(li_code)

nu_nu=0
for code_nm in li_code[:1]:
    print('------------------------------------------'+str(nu_nu)+'----------------------------------------------')
    url='https://xueqiu.com/stock/finance_us_income_statement.json?symbol=AAPL&data_type=1&dateAscType=desc&_='+ti
    for nn in li_sum:
        nn.append('0')
    time.sleep(0.1)
    res=requests.get(url, headers=headers)
    if res.status_code == 200:
        a=res.json()
        # print(a)
        li=a.get('financeUSIncomeStatementList')
        for i in li:
            tmp_symbol = i.get('symbol')
            tmp_date = i.get('date') 
            tmp_income = i.get('net_income_from_continuing_operations')  
            tmp_earn = i.get('basic_earnings_per_share')         
            for j in range(len(li_time)):
                if tmp_date == li_time[j]:
                    if not tmp_income is None:
                        li_sum[j][nu_nu]=tmp_income
    else:
        print('下载数据错误')
    nu_nu=nu_nu+1


pdd=pd.DataFrame(li_sum,  index=li_time)
pan=pdd.T
print(pan)
# for i in li_time:
#     col1='profit'+i
#     col2='radio'+i
#     pan[col1] = pan[i].map(lambda x:x.split('_')[0])
#     pan[col2] = pan[i].map(lambda x:x.split('_')[1])

pan['code'] = li_code
re=pd.merge(code,pan,how='outer',on='code')
re=re.drop_duplicates()
re.to_csv(date+'_xueqiu_us_profit.csv', encoding = 'gbk',index=False)
























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













































