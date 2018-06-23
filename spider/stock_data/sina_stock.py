import requests
import time
import pandas as pd
import json
import random
import ast

df = pd.read_html('http://quotes.money.163.com/f10/zycwzb_600004.html#01c01')
df1 = pd.read_html('http://quotes.money.163.com/f10/cwbbzy_600004.html#01c04')
#pd.DataFrame(df[4]).to_csv("a.csv")
rep1=df[4].T
col=['日期']+list(df[3].iloc[:,0])
rep1.columns=col
#print(df[5].T)
#print(df[6])
# print(df1[3])
# print(df1[4].T)
#print(df2)

current = time.strftime("%Y%m%d")
#print(current)

my_headers = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
header={"User-Agent":random.choice(my_headers)}
global null
null = ''

def stock_list_sh():
    url="http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%" \
        "2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page={}&query" \
        "=STYPE%3AEQA%3BEXCHANGE%3ACNSESH&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT" \
        "%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CH" \
         "S%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO1" \
        "0%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=SYMBOL&order=asc&count=24&type=query"
    con = requests.get(url.format(0), headers=header).content
    a = str(con.decode())
    list = []
    null = ''
    for num in range(int(eval(a)['pagecount'])):
        conn = requests.get(url.format(num),headers=header).content
        b = str(conn.decode())
        for i in eval(b)['list']:
            if i:
                if i['CODE']:
                    list.append(i['CODE'][1:])
    return list

def stock_list_sz():
    url = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%" \
          "2Fhs%2Fservice%2Fdiyrank.php&page={}&query=STYPE%3AEQA%3BEXCHANGE%3ACNSESZ&fields=NO%2CSYMBOL" \
          "%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2" \
          "CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10" \
          "%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=SYMBOL&order=asc&count=24&type=query"
    con = requests.get(url.format(0),headers=header).content
    a = str(con.decode())
    list = []
    null = ''
    for num in range(int(eval(a)['pagecount'])):
        conn = requests.get(url.format(num),headers=header).content
        b = str(conn.decode())
        #eval(b)['list']:
        for i in eval(b)['list']:
            if i:
                if i['CODE']:
                    list.append(i['CODE'][1:])
    return list


def stock_id():
    sh=stock_list_sh()
    sz = stock_list_sz()
    list=sh+sz
    return list







##http://quotes.money.163.com/service/chddata.html?code=0600004&start=20030428&end=20170512&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP