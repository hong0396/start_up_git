import requests
from bs4 import BeautifulSoup
import re
headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Cookie':'SINAGLOBAL=4934896784089.946.1493450684465; wb_publish_fist100_3067181337=1; un=gh0396@126.com; wvr=6; YF-V5-G0=5f9bd778c31f9e6f413e97a1d464047a; SCF=AhJxpoUEdsg8UH0Mxai1h8HtTcPrGcpVL7BH5kGAMc_EFGnsiuntN12_kwNZMVHr3wMHtfQ5ZNwhun83fTNF6Hw.; SUB=_2A250AOWZDeThGeVO7VUQ-C_PyDuIHXVXdFBRrDV8PUNbmtBeLWXckW-hoVllABMh09x8LarCLsLdaL77Vw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.3OQ0PG0Gg9WwU_zBlpyu5JpX5KMhUgL.Foe7SoMp1h20e0M2dJLoI7LQdc4r9cMpeoet; SUHB=03oVg8vpestAOg; ALF=1525008713; SSOLoginState=1493472713; _s_tentry=login.sina.com.cn; Apache=5439337516173.126.1493472702111; ULV=1493472702146:2:2:2:5439337516173.126.1493472702111:1493450684804; YF-Page-G0=23b9d9eac864b0d725a27007679967df; YF-Ugrow-G0=b02489d329584fca03ad6347fc915997; UOR=cuiqingcai.com,widget.weibo.com,login.sina.com.cn',
'Host':'weibo.com',
'Referer':'http://weibo.com/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/57.0.2987.133 Safari/537.36'
}

url='http://weibo.com/u/3067181337/home?is_pic=1#_0'
res=requests.get(url, headers=headers)
a=str(res.text)
print(a)
b=re.compile("<img.*?src=(.*?)<\/li>", re.S)
print(re.findall(b,a))



#soup = BeautifulSoup(res.content, 'lxml')
#print(soup.text)

