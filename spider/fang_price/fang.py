import  requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from multiprocessing import Pool
from functools import reduce
import pandas as pd
import re
url2="http://esf.sh.fang.com/"
url="http://esf.sh.fang.com/house/h316-i3{}/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}

def parse(url):
    res= requests.get(url, headers=headers)
    #res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    sumlink = soup.find_all('dd', 'info rel floatr')
    list=[]
    for lin in sumlink:
        li=[]
        href= 'http://esf.sh.fang.com'+str(lin.find('p','title').find('a').get('href'))
        title = lin.find('p', 'mt10').find('span').text
        site = lin.find('p', 'mt10').find('span','iconAdress ml10 gray9').text
        room = lin.find('p', 'mt12').text.strip().split(' ')[0].strip()
        large=lin.find('div',"area alignR").find('p').string[:-2]
        price=lin.find('div',"moreInfo").find('span','price').text
        priceper=str(lin.find('p',"danjia alignR mt5").text)[:-4]
        resp = requests.get(href, headers=headers)
        sou = BeautifulSoup(resp.text, 'lxml')

        if sou.find('span','mr10'):
            if sou.find('span', 'mr10').find_next('span','mr10'):
                if sou.find('span', 'mr10').find_next('span', 'mr10').find_next('span'):
                    date=str(sou.find('span','mr10').find_next('span','mr10').find_next('span').text.strip())
                    rea=re.compile('.*(\d{4}-\d{2}-\d{2}).*')
                    if rea:
                        li.append(str(re.findall(rea, date)).replace('[','').replace(']',''))
                    else:
                        li.append(' ')
                else:
                    li.append(' ')
            else:
                li.append(' ')
        else:
            li.append(' ')
        if sou.find('a', id='agantesfxq_B02_09'):
            li.append(str(sou.find('a', id='agantesfxq_B02_09').text.strip()))
        elif sou.find('a', id='esfshxq_12'):
            li.append(str(sou.find('a', id='esfshxq_12').text.strip()))
        else:
            li.append(' ')
        if sou.find('a', id='agantesfxq_B02_10'):
            li.append(str(sou.find('a', id='agantesfxq_B02_10').text.strip()))
        elif sou.find('a', id='esfshxq_13'):
            li.append(str(sou.find('a', id='esfshxq_13').text.strip()))
        else:
            li.append(' ')
        li.append(title)
        li.append(large)
        li.append(price)
        li.append(priceper)
        li.append(room)
        li.append(site)
        li.append(href)
        list.append(li)
    return list



#print(parse(url.format(1)))
# for i in range(2,101):
#     url3=url2.format(i)
#     parse(url3)

def pd_mysql(pan, table):
    engine = create_engine('mysql+pymysql://root:guihong@localhost/datebase?charset=utf8')
    pan.to_sql(table, engine, if_exists='replace')

if __name__ == '__main__':
    pool = Pool()
    list=pool.map(parse, [ url.format(i) for i in range(1, 101)])
    lis=reduce(lambda x,y:x+y,list)
    print(lis)
    pan = pd.DataFrame(lis, columns = ['date', 'qu', 'quyu', 'xiaoqu', 'large','price', 'priceper', 'room', 'site', 'href'])
    pd_mysql(pan,'fangtianxia')

