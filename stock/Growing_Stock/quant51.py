import numpy as np
import pandas as pd
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
import json
date=time.strftime('%Y%m%d',time.localtime(time.time()))

date1=time.strftime('%Y-%m-%d',time.localtime(time.time()))

code='sh600000'
url='http://www.quant51.cn:8051/hisdata?code='+code+'&start=19900101&end='+date+'&datatype=fin&rt=json'
# url='http://www.quant51.cn:8051/hisdata?code='+code+'&start=19900101&end='+date+'&datatype=nd&rt=json'
# url='http://www.quant51.cn:8051/hisdata?code='+code+'&start=19900101&end='+date+'&datatype=fin&rt=csv'
# print(df)


# r = requests.get(url, stream=True)
# for chunk in r.iter_content(chunk_size=512):
#     if chunk:
#         print(chunk.decode('gbk'))
#         con=chunk.decode('gbk')

r = requests.get(url, stream=True).json()
# for chunk in r.iter_content(chunk_size=512):
#     if chunk:
#         print(chunk.decode('gbk'))
#         con=chunk.decode('gbk')

# print(type(con))
# s = r'value\"\:(.*?)\]\}'
# pat = re.compile(s)
# code = pat.findall(con)
# print(code)
val=[]
li=r.get('value')[0].get('value')
for i in li:
    va=i.split(',')
    val.append(va)

val_pd=pd.DataFrame(val)
print(val_pd)


val_pd.to_csv(date1+'_'+code+"_peTTM_data.csv", encoding="gbk", index=False)




