import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool,freeze_support
import traceback
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
    print(iplist) 

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

#单进程
#for url in xiciip:
#   getIPList(url)

#以下为多进程代码

if __name__ == '__main__':
    freeze_support() 
    pool = Pool()
    pool.map(getIPList,xiciip)
    pool.close()
    pool.join()
    print('bug completed')
    