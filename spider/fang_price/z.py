import pandas as pd
import pymysql
import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
from functools import reduce
from sqlalchemy import create_engine
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}

def parse(url):
    res = requests.get(url, headers=headers)
    # res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    _list = []
    sumlin = soup.find_all('div', "info")
    for i in sumlin:
        list = []
        data = i.find_previous_sibling().find('img')
        text = str(data["data-img-layout"])
        m = re.search('\d{8}', text)
        if m:
            list.append(m.group(0))
        else:
            list.append(' ')
        # print(data["alt"])
        price = i.find('div', "info-col price-item main")
        priceper = i.find('span', "info-col price-item minor")
        mianji = i.find('span', "info-col row1-text")
        list.append(i.find('a', 'laisuzhou').text)
        list.append(i.find('a', 'laisuzhou').find_next('a').text)
        list.append(i.find('a', 'laisuzhou').find_next('a').find_next('a').text)
        list.append(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[0].strip())
        list.append(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[1].strip()[:-1])
        list.append(str(priceper.text).replace('\n', '').lstrip().rstrip().strip()[2:][:-3])
        list.append(str(price.text).replace('\n', '').lstrip().rstrip().strip()[:-1])
        _list.append(list)
    return _list


def pd_mysql(pan, table):
    engine = create_engine('mysql+pymysql://root:guihong@localhost/datebase?charset=utf8')
    pan.to_sql(table, engine, if_exists='append')

url = "http://sh.lianjia.com/ershoufang/d{}s7"

#print(parse(url.format(1)))
if __name__ == '__main__':
    pool = Pool()
    list=pool.map(parse, [ url.format(i) for i in range(1, 101)])
    lis=reduce(lambda x,y:x+y,list)
    pan = pd.DataFrame(lis, columns = ['date', 'xiaoqu', 'qu', 'weizi', 'room','pingfang',  'priceper', 'price'])
    pd_mysql(pan,'lianjia')







#
# for i in range(1, 101):
#     urls = url.format(i)
#     list += parse(urls)
#     print(list[0])
#     pan = pd.DataFrame(list)
#     print(pan)


#
# , columns = ['date', 'xiaoqu', 'qu', 'weizi', 'room','pingfang',  'large', 'mianji']
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='db1')
# cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS test")#必须用cursor才行
#
# sql = "insert into table  lianjia  "
# df = pd.read_sql(sql,conn,)
# aa=pd.DataFrame(df)
# print aa