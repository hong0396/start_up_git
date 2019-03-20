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
    url="http://q.10jqka.com.cn/thshy/"
    driver.get(url)
    # 获取cookie列表
    cookie=driver.get_cookies()
    driver.close()
    return cookie[0]['value']
# cook=get_cookie()
# print(cook)
header ={
'Host': 'basic.10jqka.com.cn',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko',
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,en-US;q=0.8',
'Cookie': 'AoIP6LStatHG63YNT30wlAaL04PkU4ZtOFd6kcybrvWgHyy5tOPWfQjnyqOf'
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
            n1tmp2=li[i+1].find('ul',"items").find_all('li')[n1].get_text().strip().replace(' ','')
        else:
            n1tmp2='0'
    else:
        n1tmp2='0' 
    lia=str(n1tmp1)+ '_' + str(n1tmp2)    
    return  lia
        
















url='http://basic.10jqka.com.cn/mobile/NVTA/benefit_ajax.html?report=djdfirst'
con=requests.get(url,headers=header)
soup = BeautifulSoup(con.content.decode('gbk'),'lxml')
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



n1=2019
n2=2019
n3=2019
n4=2019
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
    if li[i].find('span').get_text().strip().replace(' ','') == '2015一季度(累计)':
        income2015.append(get_nn(li, i, n1))        
        sale2015.append(get_nn(li, i, n2))
        exp2015.append(get_nn(li, i, n3))
        net2015.append(get_nn(li, i, n3))  
    if li[i].find('span').get_text().strip().replace(' ','') == '2016一季度(累计)':
        income2016.append(get_nn(li, i, n1))        
        sale2016.append(get_nn(li, i, n2))
        exp2016.append(get_nn(li, i, n3))
        net2016.append(get_nn(li, i, n3))
    if li[i].find('span').get_text().strip().replace(' ','') == '2017一季度(累计)':
        income2017.append(get_nn(li, i, n1))        
        sale2017.append(get_nn(li, i, n2))
        exp2017.append(get_nn(li, i, n3))
        net2017.append(get_nn(li, i, n3))      
    if li[i].find('span').get_text().strip().replace(' ','') == '2018一季度(累计)':
        income2018.append(get_nn(li, i, n1))        
        sale2018.append(get_nn(li, i, n2))
        exp2018.append(get_nn(li, i, n3))
        net2018.append(get_nn(li, i, n3))      

print(income2015)













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
        # income2015.append(str(n1tmp1)+ '_' + str(n1tmp2))
        



         




