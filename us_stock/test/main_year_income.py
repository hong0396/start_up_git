import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time,os
import tushare as ts

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])
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
'Authorization': 'Bearer dD5B49CfmRbSjaglaBhU69wmdoUGWP',
'Host': 'hq2.itiger.com',
'Origin': 'https://web.itiger.com',
'Referer': 'https://web.itiger.com/quotation',
"User-Agent":random.choice(my_headers) }



# code=pd.read_csv('D:\\Git\\us_stock\\profit\\2018-07-15_us_basic.csv',encoding='gbk')                
# li_code=code['code'].tolist()
# print(li_code)



dic={}
codd=[]
profit2018 =[]
profit2017 =[]
profit2016 =[]
profit2015 =[]
profit2014 =[]

li_sum=[profit2018,profit2017,profit2016,profit2015,profit2014]
li_time=['2018_profit','2017_profit','2016_profit','2015_profit','2014_profit']

code=pd.read_csv('2019-02-24us_all_code.csv',encoding='gbk')
# code=pd.read_csv('D:/Git/us_stock/ROE/2018-08-19_all_us_basic.csv',encoding='gbk')
# code['code']= code['code'].str.replace('HK','0')
# print(code)                
li_code=code['code'].tolist()
# for i in range(len(li_code)):
#     li_code[i] = str(li_code[i]).replace('hk','')
# print(li_code)

nu_nuu=0

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
    print('------------------------------------------'+str(nu_nuu)+'----------------------------------------------')
    # url='https://hq.itiger.com/fundamental/usstock/earnings/income/'+code_nm+'?type=income&symbol='+code_nm+'&deviceId=web20180727_722849&platform=desktop-web&env=Chrome&vendor=web&lang=&appVer=4.1.0'
    # time.sleep(0.1)
    # res=requests.get(url, headers=headers)


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
            
    print(res)
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
                if li_h[h].get('name') ==  "营业总收入":
                    num_income=h


        

        if num != 2018: 
            if not li is None:
                # codd.append(code_nm)
                for i in range(len(li)):
                    if li[i].get('type') == '年报':
                        year_date=li[i].get('date')[:4]
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
re.to_csv(date+'_Laohu_us_profit_income_year.csv', encoding = 'gbk',index=False)


















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













































