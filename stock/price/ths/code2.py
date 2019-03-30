#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import requests,time,os,xlwt,xlrd,random
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine

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
    print(cookie)
    driver.close()
    for i in cookie:
        if i.get('name') == 'qgqp_b_id':
            cookie_v = i.get('value') 
    return cookie_v 
cook=get_cookie()
header = {'Host': 'quote.eastmoney.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Cookie': cook}
get_data()


    http://q.10jqka.com.cn/index/index/board/ss/field/zdf/order/desc/page/2/ajax/1/


