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



# url_file='http://quotes.money.163.com/service/zycwzb_300703.html?type=year'
# r = requests.get(url_file, stream=True)
# for chunk in r.iter_content(chunk_size=512):
#     if chunk:
#         print( chunk.decode('gbk'))


pan=pd.read_csv('http://quotes.money.163.com/service/zycwzb_300703.html?type=year', engine='python', encoding='gbk')
print(pan)






# http://quotes.money.163.com/service/zycwzb_300703.html?type=year&part=yynl