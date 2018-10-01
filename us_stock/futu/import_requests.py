import requests
import pandas as pd

headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'tgw_l7_route=8d34ab350eb9a9772a5a0c377f34d47d; FUTU_TOOL_STAT_UNIQUE_ID=15375072309308595; UM_distinctid=165fa9285fb762-07c06f613d5cac-8383268-e1000-165fa9285fc20a; CNZZDATA1256186977=78042582-1537502489-%7C1537502489; cipher_device_id=1537507232150902',
'Host': 'www.futunn.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'	
}

url='https://www.futunn.com/stock/top-list?plate_id=200306&sort_direct=2&_=1537507268174'
r = requests.get(url,headers=headers).json()
print(r.get("data").get("list"))
print(r.get("data").get("pages"))


df=pd.DataFrame(r.get("data").get("list"))
print(df.columns)
