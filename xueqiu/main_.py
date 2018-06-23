import ast
import json
import pandas as pd
import random
import requests
import time
import tushare as ts

ti=str(time.time()).replace('.','')[:13]
print(str(time.time()).replace('.','')[:13])
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
mon=time.strftime('%m',time.localtime(time.time()))
yea=time.strftime('%Y',time.localtime(time.time()))
# ll=[]
# for i in [03,06,09,12]:
#     if int(mon)<int(i):
#         ll.append(i)





hs300 = ts.get_hs300s()

headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'device_id=532a965a081c3ba0fbe39b5c0fc85f8b; s=e2171s6b07; aliyungf_tc=AQAAAMsY133sWgkA1/2vtA9WDvRJx9Ec; __utmc=1; bid=1bb2f5fa86a17a849cfda41df0d672fb_jg3oxrws; __utmz=1.1523976088.13.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; xqat=961527a5f69d4cf6fc5ec0f106462ae122e3703f; xq_token_expire=Sat%20May%2012%202018%2023%3A18%3A17%20GMT%2B0800%20(CST); snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1523970000,1523970929,1523976088,1523978420; xq_a_token=229a3a53d49b5d0078125899e528279b0e54b5fe; xq_a_token.sig=oI-FfEMvVYbAuj7Ho7Z9mPjGjjI; xq_r_token=8a43eb9046efe1c0a8437476082dc9aac6db2626; xq_r_token.sig=Efl_JMfn071_BmxcpNvmjMmUP40; u=411523978424149; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1523980715; __utma=1.1263372986.1522814179.1523976088.1523980715.14; __utmt=1; __utmb=1.1.10.1523980715',
'Host': 'xueqiu.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

#print(hs300)

#hs300.to_csv("hs300.csv")




code=hs300['code'].values.tolist()
name=hs300['name'].values.tolist()

for i in range(len(code)):
    if code[i][0] == '6':
        saa0=code[i]
        saa1='SH'+saa0
        code[i]=saa1
    else:
        saa0 = code[i]
        saa1 = 'SZ' + saa0
        code[i] = saa1
print(code)



stock=['SZ300072','SH600000']
stock=code




nor=['201712','201709','201706','201703','201612']


li1 =[]
li2 =[]
li3 =[]
li4 =[]
li5 =[]

sum_b={}
d = {}
for t in range(len(stock)):
    print("-----------------正在收集数据------------------")
    for k in range(len(nor)):
        d[nor[k]] = ' '
    #print(d)


    for j in [1,2]:
        url1='https://xueqiu.com/stock/f10/finmainindex.json?symbol='+stock[t]+'&page='+str(j)+'&size=4&_='
        url=url1+ti
        time.sleep(5)
        res=requests.get(url, headers=headers)
        a=res.text
        data=json.loads(a)

        for list in data['list']:
            print(list)
            datee=list['reportdate']
            b=list['naps']
            #print(datee[:6])
            for k in range(len(nor)):
                if datee[:6]==nor[k]:
                    d[nor[k]] = b

    for k in range(len(nor)):
        if k == 0:
            strr=d[nor[k]]
            li1.append(strr)
        elif k == 1:
            strr = d[nor[k]]
            li2.append(strr)
        elif k == 2:
            strr = d[nor[k]]
            li3.append(strr)
        elif k == 3:
            strr = d[nor[k]]
            li4.append(strr)
        elif k == 4:
            strr = d[nor[k]]
            li5.append(strr)


#print(li1)


li=[]
li.append(stock)
li.append(name)
li.append(li1)
li.append(li2)
li.append(li3)
li.append(li4)
li.append(li5)

sum=pd.DataFrame(li)
sum=sum.T
nor.insert(0, 'code')
nor.insert(1, 'name')
sum.columns = nor
#sum.index=stock
print(sum)
sum.to_csv(date+"sum.csv")
# li1_s = pd.Series(li1)
# li2_s = pd.Series(li2)
# li3_s = pd.Series(li3)
# li4_s = pd.Series(li4)
# li5_s = pd.Series(li5)
#
        #     li_date.append(date[:6])
        # else:
        #     li_date.append(' ')
        # if b:
        #     li_b.append(b)
        # else:
        #    li_b.append(' ')

#print(d)