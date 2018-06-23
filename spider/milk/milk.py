import  requests
from urllib import request
import  re
import json
from bs4 import BeautifulSoup
import os

url_nz='https://list.jd.com/list.html?cat=1320,5019,12215&ev=exbrand_22296&sort=sort_totalsales15_desc&trans=' \
    '1&JL=3_%E5%93%81%E7%89%8C_%E7%BA%BD%E9%BA%A6%E7%A6%8F%EF%BC%88Meadow%20fresh%EF%BC%89#J_crumbsBar'
url_nz_js='https://p.3.cn/prices/mgets?callback=jQuery8031365&type=1&area=1_72_2799_0&skuIds=J_1431598%2CJ_' \
      '1431626%2CJ_1431622%2CJ_4390362%2CJ_2854425%2CJ_1431620%2CJ_2854421%2CJ_10809075381%2CJ_10809094519' \
      '&pdbp=0&pdtk=&pdpin=&pduid=1493168484631737432685&source=list_pc_front&_=1493434452636'
url_z="https://list.jd.com/list.html?cat=1320,5019,12215"
url_z_js="https://p.3.cn/prices/mgets?callback=jQuery448791&type=1&area=1_72_2799_0&skuIds=J_1385736%" \
      "2CJ_627718%2CJ_1070843%2CJ_1857014%2CJ_1431598%2CJ_2149283%2CJ_1307900%2CJ_2658756%2CJ_3061636%" \
      "2CJ_1070841%2CJ_896024%2CJ_1431626%2CJ_1805141%2CJ_3723872%2CJ_1947734%2CJ_2458098%2CJ_2149294%2C" \
      "J_1938564%2CJ_2458385%2CJ_1796166%2CJ_1127466%2CJ_896020%2CJ_1533902%2CJ_2005965%2CJ_1857008%2CJ_" \
      "1546827%2CJ_627720%2CJ_3900955%2CJ_2458387%2CJ_1803729&pdbp=0&pdtk=&pdpin=&pduid=1493168484631737432685" \
      "&source=list_pc_front&_=1493441327143"
def milk(url, url_js):
    res=requests.get(url)
    res_j=requests.get(url_js)
    # response=request.urlopen(url)
    # html=response.read()
    qur=re.compile(r'\[(.*?)\]')
    qu=re.findall(qur,str(res_j.content))
    soup = BeautifulSoup(res.content, 'lxml')
    lis=soup.find_all('li', "gl-item")
    list=[]
    for i in lis:
        _list=[]
        _list.append(i.find_all('em')[-1].string)
        a=re.compile(r'\d+')
        b=re.findall(a, str(i.find('div', 'p-img').find('a').get('href')))
        for dict in qu:
            for j in eval(dict):
                if str(j.get('id').split('_')[-1]) == str(b[0]):
                    _list.append(j.get('p'))
        list.append(_list)
    return list

list=milk(url_nz,url_nz_js)
for i in list:
    print(i)
