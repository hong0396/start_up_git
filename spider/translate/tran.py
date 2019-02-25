#!/usr/bin/env python
# -*- coding:utf-8 -*-
  
'''
爬虫之百度翻译
需要的库有 js2py, requests, re, json
'''
  
__author__ = 'YXQ'
  
  
import js2py
import requests
import json
import re
  
#百度翻译的主页
url_fanyi = 'http://fanyi.baidu.com'
#翻译时post的api
url_api = 'http://fanyi.baidu.com/v2transapi'
#设置 headers
headers = {
    'Cookie':'BIDUPSID=A360C8CE43082B9E2E23B5B111FC4363; PSTM=1485329732; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=26524_1466_21124_18560_26350_22158; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1531663222,1531743493; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1531748592; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; BAIDUID=96A2302A5D66AFBE539FFC68E881260F:FG=1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13076.400',
}
  
#get百度翻译主页，是为了得到token
req_get = requests.get(url = url_fanyi, headers = headers)
token = re.search(r"token: '(.*?)',", req_get.text, re.S).group(1)
  
#需要翻译的内容，中英文都可以
translation_content = '我是一个中国人，我不为五斗米折腰'
  
#读入js代码
def get_js():
    with open('sign.js', 'r', encoding='utf-8') as f:
        return f.read()
#使用js2py在python中运行js代码并得到sign
run_js = js2py.EvalJs({})
run_js.execute(get_js())
sign = run_js.e(translation_content)
  
data = {
    'query':translation_content,
    'sign':sign,
    'token': token
}
  
req_post = requests.post(url = url_api, data = data, headers = headers)
result = json.loads(req_post.text)
  
print(result['trans_result']['data'][0]['dst'])