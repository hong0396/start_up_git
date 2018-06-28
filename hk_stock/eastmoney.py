import urllib.request
import re
import time
import requests
import csv
import pandas as pd
from sqlalchemy import create_engine
# import pymysql
import random
from  bs4 import BeautifulSoup
import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
# url = 'http://quotes.money.163.com/hkstock/cwsj_00119.html'
current = time.strftime("%Y%m%d")
url='http://hkf10.eastmoney.com/F9HKStock/GetAnalysisSummaryData.do?securityCode={}.HK&yearList=2018,2017,2016,2015&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'
# 'http://hkf10.eastmoney.com/F9HKStock/GetAnalysisSummaryData.do?securityCode=00241.HK&yearList=2018,2017,2016,2015&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'
# df = pd.read_html(url)
# html = urllib.request.urlopen(url.format('00241')).read()
# html = html.decode('gbk')
con = requests.get(url.format('00241'), headers=header).content
# print(type(con.decode()))
a = str(con.decode())
# dic = json.loads(list(a)[0])
# s = r'\\(.*?)\\'
# pat = re.compile(s)
# test = pat.findall(a)
# print(type(a))
test=re.sub(r'\\','', str(a)) 
lis=[]
pan=pd.DataFrame()
li=test.strip('"[').strip(']"').split(r'},')
for i in li:
    if i[-1] != '}':
        i=i+'}'
    else:
        pass
    dic = json.loads(i)
    # print(dic)
    tmp_pd=pd.Series(dic)   
    lis.append(tmp_pd)

pan=pd.concat(lis, axis=1)
pan=pan.T
pan=pan.drop(["Indent","IsBold","IsShowChart"],1)
print(pan)
pan.to_csv("a.csv",encoding='gbk')