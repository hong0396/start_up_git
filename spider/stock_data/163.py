import urllib.request
import re
import time
import requests
import csv
import sina_stock
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import random

header={'Host': 'quotes.money.163.com',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'ser-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'Province=021; City=021; UM_distinctid=15bfcbf263fa27-0d18b021b5dd1f-541a301f-100200-15bfcbf2640575; vjuids=-3f64a0445.15bfcbf2943.0.c0b020852df6d; _ntes_nnid=fc5b23d9b9f1dda9ae52d8c81a08529f,1494594038099; _ntes_nuid=fc5b23d9b9f1dda9ae52d8c81a08529f; usertrack=c+5+hVkV7kStRHqRA8MdAg==; _ga=GA1.2.163554575.1494609469; _gid=GA1.2.19604338.1494609469; ne_analysis_trace_id=1494683090432; _ntes_stock_recent_=0600000%7C0603180%7C0601857%7C1000627%7C0600004; _ntes_stock_recent_=0600000%7C0603180%7C0601857%7C1000627%7C0600004; _ntes_stock_recent_=0600000%7C0603180%7C0601857%7C1000627%7C0600004; NE_DANMAKU_USERID=353d1; vjlast=1494594038.1494605991.13; vinfo_n_f_l_n3=0c74f13321747664.1.4.1494594038107.1494683899963.1494690827745; s_n_f_l_n3=0c74f133217476641494687558835'
}

##def downback(a,b,c):
##    ''''
##    a:已经下载的数据块
##    b:数据块的大小
##    c:远程文件的大小
##   '''
##    per = 100.0 * a * b / c
##    if per > 100 :
##        per = 100
##    print('%.2f%%' % per)

stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
current = time.strftime("%Y%m%d")
# 获取股票代码列表
def urlTolist(url):
    allCodeList = []
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodeList.append(item)
    return allCodeList

def pd_mysql(pan, table):
    engine = create_engine('mysql+mysqlconnector://root:guihong@localhost/datebase?charset=utf8')
    #engine = create_engine('mysql+pymysql://root:guihong@localhost/datebase?charset=utf8')
    #engine = create_engine('mysql+pymysql://root:guihong@localhost/datebase?charset=utf8mb4')
    pan.to_sql(table, engine, if_exists='append', index= False)


allCodelist = urlTolist(stock_CodeUrl)
panda = pd.DataFrame()
def main(list):
    for code in list:
        print('正在获取%s股票数据...' % code)
        if code[0] == '6':
            url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
              '&end='+current+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1' + code + \
              '&end='+current+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        req=requests.get(url, headers=header)                                          # 可以加一个参数dowmback显示下载进度
        req.encoding = 'gbk'
        pdf=req.text
        print(pdf)
        li = []
        for i in pdf.splitlines():
            tem = [j.strip().replace("'","") for j in i.split(',')]
            while '' in tem:
                tem.remove('')
            li.append(tem)
            #print(li)
        pan = pd.DataFrame(li[1:], columns=li[0])
        #pan=pan.drop('index', axis=1, inplace=True)
        #print(pan)
        #panda.append(pan)
        if not pan.empty:
            pd_mysql(pan, "stock_all")
    #pd_mysql(panda, "stock_all")






lis=sina_stock.stock_id()
print(lis)
main(lis)
#main(["600062","600000"])
