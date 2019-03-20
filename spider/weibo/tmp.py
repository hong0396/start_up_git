#-*- coding=utf-8
from requests import Session
import json

def formatUrl(urldict):
    for key,value in urldict.items():
        urldict[key]=value.replace("\\",'')

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
         'Referer':'https://passport.weibo.cn/signin/login?entry=mweibo'}

cookies={'_s_tentry':'news.ifeng.com',
        'UOR':'news.ifeng.com,widget.weibo.com,tech.ifeng.com'}

url='https://passport.weibo.cn/sso/login'

username=input('pls input weibo ID: ')
pwd =input('pls input weibo password: ')


fromdata={'username':username,'password':pwd,
        'savestate':'1','r':None,'ec':'0','pagerefer':None,
        'entry':'mweibo','wentry':None,'loginfrom':None,
        'client_id':None,'code':None,'qq':None,'mainpageflag':'1',
        'hff':None,'hfp':None}

with Session() as s:
    s.headers.update(headers)
    resp = s.post(url,data=fromdata)
    cross_domain_list = json.loads(resp.text)['data']['crossdomainlist']
    formatUrl(cross_domain_list)
    s.get(cross_domain_list['weibo.com'],cookies=cookies)
    #通过cross_domain 获取PC端的登陆状态，此时可以以登录状态直接访问PC端的页面，从而绕过诸多加密校验
    s.get(cross_domain_list['sina.com.cn'])
    s.get(cross_domain_list['weibo.cn'])
    s.headers.update({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'})
    resp=s.get('https://weibo.com/')
    with open('webo.html','wb') as f:
        f.write(resp.content)