import urllib.request
import re
import time
import requests
import csv
import pandas as pd


df = requests.get('http://stockpage.10jqka.com.cn/financeflash/hk/HK1169/keyindex.txt')
print(df)