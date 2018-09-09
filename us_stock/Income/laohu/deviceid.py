import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

url='https://web.itiger.com/quote/BIDU/finance'
# url='http://q.10jqka.com.cn/hk/detail/board/all/field/zdf/order/desc/page/2/ajax/1/'
browser = webdriver.Firefox()
browser.get(url)
cookie = browser.get_cookies()
# cook=eval(str(cookie[1])).get('value')
print(cookie)
# browser.close()
browser.quit()


