import ast
import json
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import time
import tushare as ts
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])


def scroll(driver):
    driver.execute_script(""" 
        (function () { 
            var y = document.body.scrollTop; 
            var step = 250; 
            window.scroll(0, y); 
            function f() { 
                if (y < document.body.scrollHeight) { 
                    y += step; 
                    window.scroll(0, y); 
                    setTimeout(f, 50); 
                }
                else { 
                    window.scroll(0, y); 
                    document.title += "scroll-done"; 
                } 
            } 
            setTimeout(f, 1000); 
        })(); 
        """)




url='http://www.aastocks.com/en/stocks/market/index/h-shares.aspx'
    
browser = webdriver.Firefox()
browser.get(url)
browser.set_page_load_timeout(30)



scroll(browser)
time.sleep(5)  
# cookie = browser.get_cookies()
# cook=eval(str(cookie[0])).get('value')
# print(cook)

# text=browser.find_element_by_id('ftConw').text
text=browser.find_element_by_class_name('grid_16')
print(text.text)
browser.quit()





