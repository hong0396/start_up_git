from selenium import webdriver

url='http://q.10jqka.com.cn/hk/detail/board/all'
# url='http://q.10jqka.com.cn/hk/detail/board/all/field/zdf/order/desc/page/2/ajax/1/'
browser = webdriver.Firefox()
browser.get(url)
cookie = browser.get_cookies()
print(eval(str(cookie[0])).get('value'))





