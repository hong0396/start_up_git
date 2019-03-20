#!/usr/bin/env python
# -*- coding:utf-8
import requests
import time
import pandas as pd
from collections import OrderedDict
def getNewsDetail(item_list):
    news_list = []
    for item in item_list:
        news=OrderedDict()
        news['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item['display_time']))
        news['id']   = item['id']
        news['content'] = item['content_text']
        news_list.append(news)
    return news_list

APIurl = 'https://api-prod.wallstreetcn.com/apiv1/content/lives'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept':'application/json, text/plain, */*'}

pc_params = {'channel':'global-channel',
        'client':'pc',
        'cursor':0,
        'limit':40}

news_list = []
for Loop_count in range(5): 
    resp = requests.get(APIurl,headers=headers,params=pc_params)
    content = resp.json()['data']
    pc_params['cursor'] = content['next_cursor']
    news_list.extend(getNewsDetail(content['items']))

df = pd.DataFrame(news_list)
df.to_excel('华尔街.xlsx')