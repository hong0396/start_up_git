import urllib.request
import re
import time
import requests
import csv
import pandas as pd
import sys
import hashlib
import re
import base64
import matplotlib.pyplot as plt


# url_file='http://quotes.money.163.com/service/zycwzb_300703.html?type=year'
# r = requests.get(url_file, stream=True)
# for chunk in r.iter_content(chunk_size=512):
#     if chunk:
#         print( chunk.decode('gbk'))


pan=pd.read_csv('http://quotes.money.163.com/service/zycwzb_000651.html?type=year', engine='python', encoding='gbk')
pant=pan.T
print(pan)
li=pant.loc[['报告日期']].values.tolist()
pant.drop('报告日期',inplace=True)

pant.columns=li
# print(pant)主营业务利润(万元) 







# http://quotes.money.163.com/service/zycwzb_300703.html?type=year&part=yynl