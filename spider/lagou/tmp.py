#!/usr/bin/env python
# -*- coding:utf-8
import requests
import pandas as pd
from collections import OrderedDict
from bs4 import BeautifulSoup
import time


def getPosInfo(posList,curSession):
    posinfoList=[]
    if posList['state'] == 1:
        posList = posList['content']['data']['page']
    else:
        print('Something goes wrong with our spider!')
        return ['no job available']
    for pos in posList['result']:
        posinfo = OrderedDict()
        posinfo['公司全称'] = pos['companyFullName']
        posinfo['公司缩写'] = pos['companyName'] 
        posinfo['创建时间'] = pos['createTime']
        posinfo['职位名称'] = pos['positionName']
        posinfo['薪水'] = pos['salary']
        posinfo['职位编号'] = str(pos['positionId'])
        getPosDetail(posinfo,curSession)
        posinfoList.append(posinfo)
        time.sleep(0.5)

    return posinfoList


def getPosDetail(posinfo,curSession):
    resp = curSession.get(posDetailurl.format(positionid=posinfo['职位编号']))
    print(resp.url)
    bsobj = BeautifulSoup(resp.text,'html.parser')
    temptation = bsobj.select('div.temptation')
    if temptation != []:
        posinfo['职位诱惑'] = temptation[0].string.strip().lstrip('职位诱惑：')
    else:
        posinfo['职位诱惑']= '无'
    desc=''
    for line in bsobj.select('div.content p')[::]:
        if line.string != None:
            desc+=(line.string + '\n')
    posinfo['职位描述'] = desc


cookies={'JESSIONID':'XXX',
         'LGRID':'XXX',
         'LGSID':'XXX',
         'LGUID':'XXX',
         'user_trace_token':'XXX',
         'login':'true',
         }
starturl = 'https://m.lagou.com/search.json'
posDetailurl='https://m.lagou.com/jobs/{positionid}.html'
headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
         'X-Requested-With':'XMLHttpRequest',
         'Accept':'application/json',
         'Accept-language':'zh-CN,zh;q=0.8',
         'Accept-Encoding':'gzip, deflate, br'}

params={'city':'上海',
        'positionName':'python 爬虫',
        'pageNo':1,
        'pageSize':15}

city = input("请输入职位所在城市: ")
position = input("请输入搜索职位: ")
params['city']= city
params['positionName'] = position
poslist=[]
with requests.Session() as s:
    s.headers.update(headers)
    s.cookies.update(cookies)
    #请自行调节爬取的页数
    for page in range(1,3):
        params['pageNo']=page
        content = s.get(starturl,params=params)
        content.encoding='utf-8'
        poslist.extend(getPosInfo(content.json(),s))

ds = pd.DataFrame(poslist)
ds.to_excel('拉钩.xlsx')