import requests
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

headers={
# 'GET https://finance.futunn.com/api/finance-v2/income-statement?code=AAPL&market=us&quarter=6&flag=0&size=8&date= HTTP/1.1
'Host': 'finance.futunn.com',
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; LEX727 Build/WEXNAOP5801809152S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044208 Mobile Safari/537.36 FutuNN_Android/8.13.726 CliLang/zh-cn ClientFont/1.0 (quote:1; trade:1; news:1; nnc:1; sns:1; other:1) ClientSkinType/0',
'Referer': r'https://finance.futunn.com/site/h5?clientver=8.13.726&market=us&url=2020025&code=AAPL&clienttype=13&user_id=2266118&web_session_key=ZKGxT7xAAWGP0hN2SXm2%2Fxlvt%2FHNQH6gi0Sb3z0utRss55ljh3BoYKnJiwdNzr2gXsBO%2BHnMl0WA1cKJp5BCMedCVJWV4f92spqBeN%2FDqDirFH3c3561NnwPXjrPMn5U',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,en-US;q=0.8',
'Cookie': r"UM_distinctid=165fac4a8340-0c136e5bf2155b-11267b6c-49a10-165fac4a83fef; cipher_device_id=1537510516586901; promotion_verify=8a5314b8675397c7a18c4cbaa099adf7; channel=4; expire=1538153983; domain=.futunn.com; path=/; tgw_l7_route=00669fc3f4aa68772a1f12d0695522ec; PHPSESSID=f53e013ki1lkd3bu1k4kio9754; web_sig=yk9GEbUkMqYOqO4GoK%2BNDP87esBDN%2BkbH3xl8MSd9gU%2Fn2X44gbnN%2BNHiaQoNhZkVqMchwBuZ4eS4op4A69rs6%2FMajIT9%2BEUnjY7vTcVpiM%3D; uid=2266118; ci_sig=8YkFRVR4uEGdK6GqhU1Xwv3CdG9hPTEwMDAwNTM4JmI9MjAxMTM2Jms9QUtJRENXblN2cWJ4UDkza3lYdW55ZTNNYXVJUWp2angydFlEJmU9MTU0MDEwMjQ1OSZ0PTE1Mzc1MTA0NTkmcj0yNzUyMzUyNTkmdT0mZj0%3D; FUTU_TOOL_STAT_UNIQUE_ID=15375105977898992; CNZZDATA1256186977=1019813802-1537509454-%7C1537549132"
}

url='https://finance.futunn.com/api/finance-v2/income-statement?code=AAPL&market=us&quarter=6&flag=0&size=8&date='
r = requests.get(url,headers=headers, verify=False).json()
# print(r.get('data').get('list').get('title'))
# print(r.get('data').get('list').get('values'))
# print(r.get('data').get('list').get('keys'))
# print(r.get('data').get('list').get('us_ext_msg'))
value=r.get('data').get('list').get('values')
title=r.get('data').get('list').get('title')
key=r.get('data').get('list').get('keys')
df=pd.DataFrame(value,index=title,columns=key)
print(df)
