import requests
import pandas as pd
from sqlalchemy import create_engine
import pymysql

def sh_list():
    headers = {
        'Host': 'query.sse.com.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'yfx_c_g_u_id_10000042=_ck17051300331218775756943779163; yfx_mr_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000042=; VISITED_COMPANY_CODE=%5B%22600000%22%5D; VISITED_STOCK_CODE=%5B%22600000%22%5D; seecookie=%5B600000%5D%3A%u6D66%u53D1%u94F6%u884C; yfx_f_l_v_t_10000042=f_t_1494606792868__r_t_1494606792868__v_t_1494608647214__r_c_0; VISITED_MENU=%5B%228529%22%2C%228451%22%2C%228464%22%2C%228523%22%2C%228466%22%2C%229062%22%2C%229055%22%2C%228528%22%2C%229857%22%5D'
    }
    url='http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1'
    res=requests.get(url, headers=headers)
    pdf=res.text
    li=[]
    for i in pdf.splitlines():
        tem=[j.strip() for j in i.split('\t')]
        while  '' in tem:
            tem.remove('')
        li.append(tem)
    pan=pd.DataFrame(li[1:], columns=li[0])
    return pan


def pd_mysql(pan, table):
    engine = create_engine('mysql+pymysql://root:guihong@localhost/datebase?charset=utf8')
    pan.to_sql(table, engine, if_exists='replace', index= False)

pd_mysql(sh_list(),'stock_list')




