import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast, os
from functools import reduce
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine

#获取动态cookies
def get_cookie():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver=webdriver.Chrome(executable_path=chromedriver,chrome_options=options)
    url="http://data.10jqka.com.cn/" #http://stock.10jqka.com.cn/
    driver.get(url)
    # 获取cookie列表
    cookie=driver.get_cookies()
    driver.close()
    return cookie[1]['value']
cook=get_cookie()
# print(cook)
header ={
'Referer': 'http://stockpage.10jqka.com.cn/HQ_v4.html',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
'Cookie': 'v='+cook
 }

def get_nn(li, i, n1):
    if not li[i].find('ul',"items")  is None:
        if n1 != 2019:
            n1tmp1=li[i].find('ul',"items").find_all('li')[n1].get_text().strip().replace(' ','')
        else:
            n1tmp1='0'
    else:
        n1tmp1='0'            
    if li[i+1].find('span').get_text().strip().replace(' ','') == '同比':
        if not li[i+1].find('ul',"items")  is None:
            if len(li[i+1].find('ul',"items").find_all('li')) > n1:
                n1tmp2=li[i+1].find('ul',"items").find_all('li')[n1].get_text().strip().replace(' ','')
            else:
                n1tmp2='0'
        else:
            n1tmp2='0'
    else:
        n1tmp2='0' 
    lia=str(n1tmp1)+ '_' + str(n1tmp2)    
    return  lia
        

# code=pd.read_csv('last_us_all_code.csv',encoding='gbk')
# li_code=code['code'].tolist()

url='http://d.10jqka.com.cn/v6/line/hs_600196/11/all.js'
con=requests.get(url,headers=header)  
# soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
# print(soup)
soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
# print(soup.text)
aa =re.findall(r'[^()]+', soup.text)[1]
dictinfo = json.loads(aa) 
date=[]
for i in dictinfo.get('sortYear'):
    li=[]
    li.append(str(i[0]))
    li_tmp=li*i[1]
    # print(li_tmp)
    date.extend(li_tmp)
# print(date)    
if len(date) == len(list(dictinfo.get('dates').split(','))):
    date_new=map(lambda x, y: x + y, date, list(dictinfo.get('dates').split(',')))
    date_new =list(date_new)
else:
    print('数据有误')
a=list(dictinfo.get('price').split(','))
b=[]
for i in range(0, len(a), 4):
    b.append(a[i:i+4])
open=[]
close=[]
low=[]
high=[]
for i in b:
    low.append(int(i[0])/100)
    open.append((int(i[0])+int(i[1]))/100)
    high.append((int(i[0])+int(i[2]))/100)
    close.append((int(i[0])+int(i[3]))/100)     
p=pd.DataFrame({'date':date_new, 'low':low,'close':close, 'high':high,'open':open, 'volumn': list(dictinfo.get('volumn').split(','))  })
print(p)









def get_income(url ,li_code):
    income2015=[]
    income2016=[]
    income2017=[]
    income2018=[]

    sale2015=[]
    sale2016=[]
    sale2017=[]
    sale2018=[]

    exp2015=[]
    exp2016=[]
    exp2017=[]
    exp2018=[]

    net2015=[]
    net2016=[]
    net2017=[]
    net2018=[]
    for code_nm in range(len(li_code)):
        print('---------------------'+str(code_nm)+'---'+str(li_code[code_nm])+'---------------------------')
        income2015.append('0_0')
        income2016.append('0_0')
        income2017.append('0_0')
        income2018.append('0_0')

        sale2015.append('0_0')
        sale2016.append('0_0')
        sale2017.append('0_0')
        sale2018.append('0_0')

        exp2015.append('0_0')
        exp2016.append('0_0')
        exp2017.append('0_0')
        exp2018.append('0_0')

        net2015.append('0_0')
        net2016.append('0_0')
        net2017.append('0_0')
        net2018.append('0_0')

        con=requests.get(url.format(str(li_code[code_nm])),headers=header)
        time.sleep(0.3)
        while (con.status_code != 200) or (not con.content ): 
            cook=get_cookie()
            con=requests.get(url.format(str(li_code[code_nm])),headers=header)  
        
            # cook=get_cookie()
            # con=requests.get(url.format(str(li_code[code_nm])),headers=header)  
        soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
        n1=2019
        n2=2019
        n3=2019
        n4=2019
        if not  soup.find('div','left') is None:
            lii=soup.find('div','left').find('ul',"items").find_all('li')
            for q in range(len(lii)):
                if (lii[q].get_text().strip().replace(' ','')) == '营业收入':
                    n1=q
                if (lii[q].get_text().strip().replace(' ','')) == '市场、销售和管理费用':
                    n2=q
                if (lii[q].get_text().strip().replace(' ','')) == '研发费用':
                    n3=q
                if (lii[q].get_text().strip().replace(' ','')) == '营业利润':
                    n4=q

            li=list(soup.find('div','right').find('div','slide-area').find_all('div','block-holder'))
            for i in  range(len(li)):
                if li[i].find('span').get_text().strip().replace(' ','') == '2015四季度':
                    income2015[code_nm]=(get_nn(li, i, n1))        
                    sale2015[code_nm]=(get_nn(li, i, n2))
                    exp2015[code_nm]=(get_nn(li, i, n3))
                    net2015[code_nm]=(get_nn(li, i, n3))  
                if li[i].find('span').get_text().strip().replace(' ','') == '2016四季度':
                    income2016[code_nm]=(get_nn(li, i, n1))        
                    sale2016[code_nm]=(get_nn(li, i, n2))
                    exp2016[code_nm]=(get_nn(li, i, n3))
                    net2016[code_nm]=(get_nn(li, i, n3))
                if li[i].find('span').get_text().strip().replace(' ','') == '2017四季度':
                    income2017[code_nm]=(get_nn(li, i, n1))        
                    sale2017[code_nm]=(get_nn(li, i, n2))
                    exp2017[code_nm]=(get_nn(li, i, n3))
                    net2017[code_nm]=(get_nn(li, i, n3))      
                if li[i].find('span').get_text().strip().replace(' ','') == '2018四季度':
                    income2018[code_nm]=(get_nn(li, i, n1))        
                    sale2018[code_nm]=(get_nn(li, i, n2))
                    exp2018[code_nm]=(get_nn(li, i, n3))
                    net2018[code_nm]=(get_nn(li, i, n3))      
    su= pd.DataFrame({'code':li_code, 
        'income2018':income2018,
        'sale2018':sale2018,
        'exp2018':exp2018,
        'net2018':net2018,

        'income2017':income2017,
        'sale2017':sale2017,
        'exp2017':exp2017,
        'net2017':net2017,

        'income2016':income2016,
        'sale2016':sale2016,
        'exp2016':exp2016,
        'net2016':net2016,

        'income2015':income2015,
        'sale2015':sale2015,
        'exp2015':exp2015,
        'net2015':net2015,

        })

    return su
   
# date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
# sun=get_income(url ,li_code)
# sun.to_csv(date+'_year_income_ths.csv',encoding = 'gbk',index=False)










        # if not li[i].find('ul',"items")  is None:
        #     if n1 != 2019:
        #         n1tmp1=li[i].find('ul',"items").find_all('li')[n1].get_text().strip().replace(' ','')
        #     else:
        #         n1tmp1='0'
        # else:
        #     n1tmp1='0'            
        # if li[i+1].find('span').get_text().strip().replace(' ','') == '同比':
        #     if not li[i+1].find('ul',"items")  is None:
        #         n1tmp2=li[i+1].find('ul',"items").find_all('li')[n1].get_text().strip().replace(' ','')
        #     else:
        #         n1tmp2='0'
        # else:
        #     n1tmp2='0' 
        # (str(n1tmp1)+ '_' + str(n1tmp2))
        



         




