import requests
import pandas as pd
import time
headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
,'Accept-Encoding': 'gzip, deflate, br'
,'Accept-Language': 'zh-CN,zh;q=0.9'
,'Cache-Control': 'max-age=0'
,'Cookie': r'FUTU_TOOL_STAT_UNIQUE_ID=15424227214619448; UM_distinctid=1671f8ef5bed2-0b4123a4c75918-3a3a5c0e-1fa400-1671f8ef5bf87a; cipher_device_id=1542422722481133; uid=2266118; web_sig=64Clg85dHGv2H6ss1mfeF2iUkRavkfjn6Utnt35KOOJ5mkSnat%2B6QS9xkqFAJprPyy%2FhP3RpB8Fe%2BVjMFYoCQqcYiXSAC%2FsB2rVmlUDaKvbhYHCuDfKeTXRg57RjVtYI; ci_sig=2gpjUN0tSSdeshqJPH1VwBamzOJhPTEwMDAwNTM4JmI9MjAxMTM2Jms9QUtJRENXblN2cWJ4UDkza3lYdW55ZTNNYXVJUWp2angydFlEJmU9MTU0NTAxOTM4NSZ0PTE1NDI0MjczODUmcj0yODAxNTIxODUmdT0mZj0%3D; PHPSESSID=dk2dnae18t0ii72iu79ibij9p6; CNZZDATA1256186977=1776778979-1542421393-https%253A%252F%252Fwww.futu5.com%252F%7C1542426793; tgw_l7_route=7587343559275141d1207d24944b360a'
,'Host': 'www.futunn.com'
,'Upgrade-Insecure-Requests': '1'
,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}


url='https://www.futunn.com/quote/kline-v2?security_id=73933567245926&type=2&from=&_=1542429895594'

r = requests.get(url,headers=headers).json()
time.sleep(0.15)
# print(r.get("data").get("list"))
# print(r.get("data").get("pages"))
df=pd.DataFrame(r.get("data").get("list"))
# print(df.columns)

df.rename(columns={'c':'close','o':'open','h':'high','l':'low','k':'time','v':'volumne'}, inplace=True) 
df['close']=df['close']/1000
df['open']=df['open']/1000
df['high']=df['high']/1000
df['low']=df['low']/1000
df['volumne']=df['volumne']/10000
df.to_csv('tmp.csv',index=False, encoding='gbk')












