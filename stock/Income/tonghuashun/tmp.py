import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast
import tushare as ts
from functools import reduce
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine
import datetime
import requests
import pandas as pd 
import time 
import random
import re 
import xlwt , xlrd
import io, openpyxl
import io
import os
import os.path
import win32com.client as win32


def xls_xlsx(fname)  :
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fname)
    # xlsx: FileFormat=51
    # xls:  FileFormat=56,

    wb.SaveAs(fname+"x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
    wb.Close()                               #FileFormat = 56 is for .xls extension
    excel.Application.Quit()

#获取动态cookies
def get_cookie():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver=webdriver.Chrome(executable_path=chromedriver,chrome_options=options)
    url="http://basic.10jqka.com.cn"
    driver.get(url)
    # 获取cookie列表
    cookie=driver.get_cookies()
    driver.close()
    return cookie

# cook=get_cookie()
# print(cook)
header ={
'Host': 'basic.10jqka.com.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': 'spversion=20130314; __utma=156575163.2100208507.1552196394.1552196394.1552196394.1; __utmz=156575163.1552196394.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; historystock=1A0001%7C*%7C000757%7C*%7C300059%7C*%7C002803%7C*%7C002127; searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1552196434,1552309055,1552577264,1552655966; reviewJump=nojump; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1552658831; skin_color=black; talogid=; v=Agw4QpawvNSjyaio0WhR2c1K3WE9RbDusunEs2bNGLda8aJXjlWAfwL5lP-1'
 }
path=os.getcwd()
url ='http://basic.10jqka.com.cn/api/stock/export.php?export=benefit&type=report&code=600519'
con=requests.get(url,headers=header)
html=con.content
with open('test5.xls','wb') as f:
    f.write(html)
fname= path+'\\test5.xls'
xls_xlsx(fname)
aa=pd.read_excel(fname+"x")
os.remove(fname) 
os.remove(fname+"x") 
print(aa)
















