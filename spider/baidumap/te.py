import requests
import pandas as pd

name = '上海'
key = 'vLyZjPkryKy5Mn2LG1fp6ColMGFfFFiu'
url = 'http://api.map.baidu.com/place/v2/search?query=曼玲粥店&region=上海&pagesize=20&page_num={}&output=json&ak='+key

li=[]
name = []
lng = []
lat = []
address = []
area = []
for i in range(16):
    print(i)
    r = requests.get(url.format(str(i)))
    res = r.json()
    print(list(res.get('results')))
    results=list(res.get('results'))
    for adr in results:
        name.append(adr['name'])
        location= adr['location']
        lng.append(float(location['lng']))
        lat.append(float(location['lat']))
        address.append(adr['address'])
        area.append(adr['area'])
df=pd.DataFrame({'name':name,'lng':lng, 'lat':lat,'address':address,'area':area})
df.to_csv('address1.csv',encoding='gbk' )
