from urllib import request
from bs4 import BeautifulSoup
from distutils.filelist import findall
import time, datetime
import requests

#从66ip获取页面地址
def getUrlFrom66Ip(page):
	if page == 1:
		return "http://www.66ip.cn/index.html"
	else:
		return "http://www.66ip.cn/%d.html"%page

def getIpsFrom66Url(url):
	page = request.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	iplistTable = soup.find(attrs={"class":"containerbox"})
	trList = iplistTable.find_all("tr")
	ipPortList = []
	for tr in trList[1:]:
		tdList = tr.find_all("td")
		ip = tdList[0].get_text()
		port = tdList[1].get_text()
		isinuse = 1
		source = "66ip"
		addtime = int(time.time())
		# ipPortList.append((ip, port, isinuse, source, addtime))
		ipPortList.append(ip+":"+port)

	# print(ipPortList, "\n")
	return ipPortList

def get_valid_ip( ip_set):
    """
    代理ip可用性测试
    """
    # 设置请求地址
    url = 'https://www.baidu.com'

    # 可用代理结果
    results = set()
    # 不可用的代理
    fail_ip = set()
    # 挨个检查代理是否可用
    for p in ip_set:
        proxy = {'http': 'http://'+p}
        try:
            # 请求开始时间
            start = time.time()
            r = requests.get(url, proxies=proxy, timeout=1.5)
            # 请求结束时间
            end = time.time()
            # 判断是否可用
            if r.text is not None:
                print ('succeed: ' + p + '\t' + " in " + format(end-start, '0.2f') + 's')
                # 追加代理ip到返回的set中
                results.add(p)
            else:
                fail_ip.add(p)
        except OSError:
            print ('timeout:', p)

    return results




#循环获取ip列表
def getIps():
	page=1
	li=[]
	while(page<10):
		#获取当页的url
		url=getUrlFrom66Ip(page)
		#获取当页面上的ip列表
		ips=getIpsFrom66Url(url)
		if (len(ips) == 0):
			break
		li.extend(ips)
		#保存列表到数据库
		# saveIpsToDb(ips)
		#页数增加
		page = page + 1
	result=get_valid_ip(li)
	return result

# print(getIps())