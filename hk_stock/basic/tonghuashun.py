import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver




def get_cookie():
    url='http://q.10jqka.com.cn/hk/detail/board/all'
    # url='http://q.10jqka.com.cn/hk/detail/board/all/field/zdf/order/desc/page/2/ajax/1/'
    browser = webdriver.Firefox()
    browser.get(url)
    cookie = browser.get_cookies()
    cook=eval(str(cookie[0])).get('value')
    # browser.close()
    browser.quit()
    return cook
     


#     url_login = 'http://login.weibo.cn/login/' 
#     driver = webdriver.PhantomJS()
#     driver.get(url_login)
#     driver.find_element_by_xpath('//input[@type="text"]').send_keys('your_weibo_accout') # 改成你的微博账号
#     driver.find_element_by_xpath('//input[@type="password"]').send_keys('your_weibo_password') # 改成你的微博密码

#     driver.find_element_by_xp
# ath('//input[@type="submit"]').click() # 点击登录

#     # 获得 cookie信息
#     cookie_list = driver.get_cookies()
#     return cookie_list

# cookie=get_cookie()


ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
li_code=[]
for n in range(1, 40):
    # time.sleep(1)
    url='http://q.10jqka.com.cn/hk/detail/board/all/field/zdf/order/desc/page/'+str(n)+'/ajax/1/'
    num = 403
    while num == 403:
        cookie=get_cookie()
        headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.9','Cache-Control': 'max-age=0','Connection': 'keep-alive','Host': 'q.10jqka.com.cn','Cookie': 'v='+cookie,'Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        res=requests.get(url, headers=headers)
        num = res.status_code 
    print('------------------------'+str(n)+'------------------------')    
    
    soup = BeautifulSoup(res.text, 'html5lib')
    lii=soup.find_all("tr")
    for i in lii[1:]:
	    tmp=i.text.replace('\t','').replace(' ','')
	    li_tmp=tmp.split('\n')	
	    li_code.append(li_tmp[1:-2])
	    
    # print(li_code)
pd=pd.DataFrame(li_code, columns=['序号','code',	'name','现价','涨跌幅(%)','涨跌','换手(%)','成交量','市盈率','昨收','开盘价','最高价','最低价'])
pd.to_csv('THS_hk_all_code.csv',encoding = 'gbk', index=False)











