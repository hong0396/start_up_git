import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import json
import random
import ast

my_headers = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
header={"User-Agent":random.choice(my_headers)}
# http://emweb.securities.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?ctype=4&type=0&code=sz300612
url='http://emweb.securities.eastmoney.com/NewFinanceAnalysis/DubangAnalysisAjax?code=sz300612'
con = requests.get(url, headers=header).content
a = str(con.decode())
#print(a)
list = []
dic = json.loads(a)
#dic=ast.literal_eval(a)
year_du=dic.get('nd')
for year in year_du:
    date =year.get('date')
    roe =year.get('jzcsyl')
    lrl =year.get('yyjlrl')
    zz =year.get('zzczzl')
    fz =year.get('zcfzl')
    print(date)