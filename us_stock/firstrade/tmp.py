import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver
chrome_options = Options()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(executable_path=chromedriver,chrome_options=chrome_options)

url='https://invest.firstrade.cn/cgi-bin/login?ft_locale=zh-cn'
# url='http://q.10jqka.com.cn/hk/detail/board/all/field/zdf/order/desc/page/2/ajax/1/'
# browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(10)
username="" 
passwd=""

elem=browser.find_element_by_id("username")
elem.send_keys(username)
elem=browser.find_element_by_id("password")
elem.send_keys(passwd)
elem=browser.find_element_by_id("loginButton")
elem.click()
elem=browser.find_element_by_id("")
elem.click()
elem=browser.find_element_by_id("")
elem.click()
elem=browser.find_element_by_id("")
elem.click()
elem=browser.find_element_by_id("")
elem.click()
elem=browser.find_element_by_id("submit")
elem.click()
elem=browser.find_element_by_id("myaccount_link").send_keys(Keys.ENTER)
elem.click()

# cookie = browser.get_cookies()
# cook=eval(str(cookie[1])).get('value')
# print(cookie)
# browser.close()
# browser.quit()