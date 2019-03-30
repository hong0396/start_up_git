import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool,freeze_support
import traceback,time
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
xiciip=['http://www.xicidaili.com/nn/{page}',
        'http://www.xicidaili.com/nt/{page}',
        'http://www.xicidaili.com/wn/{page}',
        'http://www.xicidaili.com/wt/{page}']

def getIPList(starturl):
    iplist = []
    try:
        for page in range(1,2):
            resp = requests.get(starturl.format(page=page),headers=headers)
            resp.raise_for_status()
            genIPitem(resp.text,iplist)
    except Exception as e:
        print('erro raised',e)
        traceback.print_exc()
    finally:
        pass
    # print(iplist)
    return iplist

def genIPitem(html,iplist):
    bs = BeautifulSoup(html,'html.parser')
    for line in bs.find_all('tr')[1::]:
        item = {}
        details = line.find_all('td')[1:6]
        item['ip'] = details[0].string
        item['port'] = details[1].string
        item['location'] = details[2].a.string if details[2].a is not None else details[2].string.strip()
        item['protocol'] = details[-1].string
        item['stype'] = details[-2].string
        iplist.append(item)

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
        proxy = {'http': p}
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

    return results,fail_ip



def check_ip( ip):
    test_url = "https://www.baidu.com"
    proxy = {
    'https': 'https://'+ip,
    'http': 'http://'+ip
    }
    try:
        re = requests.get(url=test_url,proxies=proxy,timeout=1.5)
    except Exception as e:
        # print('-[FAIL]'+proxy['https'])
        return False
    if re.status_code == 200:
        # print('*[OK]' + proxy['https'])
        return True
    else:
        # print('-[FAIL]' + proxy['https'])
        return False


#单进程
def get_ip():
    li=[]
    for url in xiciip:
        ip=getIPList(url)
        for i in ip:
            ip_pro=i.get('ip')+':'+i.get('port')
            if check_ip(ip_pro):
                li.append(ip_pro)    

    return li
# print(get_ip())

# proxy = random.choice(list(useful_proxies.keys()))
# proxies={"http": "http://" +proxy},

#以下为多进程代码

# if __name__ == '__main__':
#     freeze_support() 
#     pool = Pool()
#     pool.map(getIPList,xiciip)
#     pool.close()
#     pool.join()
#     print('bug completed')