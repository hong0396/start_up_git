
import json
import  os
import hashlib
import  re
import  requests
from  bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

name = "秋冬裙"



url='https://acs.m.taobao.com/h5/mtop.aitaobao.item.search/7.0/?v=' \
    '7.0&api=mtop.aitaobao.item.search&appKey=12574478&t=151425506732' \
    '6&callback=mtopjsonp2&type=jsonp&sign=65506eb2371f82aaa54609d570c' \
    '27f99&data={"spm"%3A"a311n.7676424%2Fd.1002.1"%2C"prepvid"%3A"201' \
    '_10.184.72.35_28093043_1514193031224"%2C"q"%3A"'+name+'"%2C"pid"%3A"m' \
    'm_33231688_7050284_23466709"%2C"clk1"%3A"undefined"%2C"ac"%3A"SILH' \
    'EuewUQ8CAXBAuwKA7ZLE"%2C"page"%3A1%2C"pvid"%3A"201_10.184.72.35_280' \
    '93043_1514255059871"%2C"bucket_info"%3A"_TL-39015"%2C"bucke' \
    't"%3A"_TL-39015"%2C"useItemCouponPage"%3A"1"%2C"lunaUrlParam"%3A"{\"al' \
    'go_sort\"%3A\"mixcoupon\"%2C\"rank\"%3A\"rank_profile%3AFirstRankSco' \
    'rer_atbh5\"%2C\"PS\"%3A\"tk_item_score_atbh5\"%2C\"appBucket\"%3A\"d\"}"%2' \
    'C"aplus_ab_b"%3A"%2Fd"%2C"sort"%3A"sales_desc"%2C"nickname"%3A""}'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'thw=cn; v=0; t=ec4ec7cb80d07944db09910fc39acd65; cookie2=39c337a7af135fbe54447dc12e4a3595; _tb_token_=e31e13e3733be; cna=SILHEuewUQ8CAXBAuwKA7ZLE; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTdf1DErt5jYA%3D%3D; UM_distinctid=1608ce926d67ff-0d1cbbfcd1a8d4-5f19331c-100200-1608ce926d77b4; miid=604768693119457036; mt=ci%3D-1_1; tk_trace=oTRxOWSBNwn9dPy5J8INBQzvy4fwxmImetkiRradetuV%2FIddSB%2FVIE%2FAkdH6JA5gpmw8nhTggb%2Btjj2uRGlKqHITLra%2Bf7iHsNPSPAMBk%2BB9JvnMakex3e7iiIXGw1SGCL6PkV8V0JAZRdJJ6GdwXM957HzqojDvWHr4CWyDwubgClPy0d99A%2FP54eN9blC400QJUbvLNlAH7%2BP1Mtb4v4%2FLucPTOBlNuOiINvc8RGUoY80O2W0wZOlVoGYZ36nLr2Zg6vWMOLgTji20muoMtLWcFJLvMyYbdhTlTbYdMIDpvyRIi%2Ftcj4bd2kKPgDPsgeDglfmg2k76HMNPRFVmlJAu1vu7QY8RGbnM0ezlwZHtw00lJWGx8uY7o%2FRHAoo8ApbOwBQiC6qdbTBGR6AAyRL%2BzaFfoH7Aw1cEdauX6EBbGJsP%2FIntf7YTau25pgNQPGCXgwOrtKQ1gP84c5soNsS6SZXZaY3Ja9WeGd9nUtb2DqeFG0slxK%2BYOIZZvvOT%2FIgpEFqVqNG5QKs2RGjRhVWDvghFIgD04DgIY7AN1mu641wGr4pocD2Ff9sxqJ9EJzA6AQrRCdmabZ8a4mdXk6kMymX0gDbKisul8HgrKyhQk%2BCV8GMrqRQl5yaIeUNB77U7FBfwcGr%2FKhTzHfveoeFn6t%2BKQshxivCxki7Ad6AY1YR%2BJ%2FUJubwOKeMV4e1v%2BPlOf2HLEDdXT0JfT2sGYAIP5lWIMXGgiTrxLG72nB5lHPib4wENbDyUew%3D%3D; _m_h5_tk=f5c277f4d4d5eed166ba68c8571b05d7_1514255691605; _m_h5_tk_enc=67db9791044ae5fe080aa12ccaf45556; isg=Ap6eJTimSIiWSJztyFu2fwnW7zRiowTVIr-lrkgnyuHfazxFsO7l6XMJF0Ec',
    'Host':'acs.m.taobao.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


}

par ={
    'v':'7.0',
    'api':'mtop.aitaobao.item.search',
    'appKey':'12574478',
    't':'1514255067326',
    'callback':'mtopjsonp2',
    'type':'jsonp',
    'sign':'65506eb2371f82aaa54609d570c27f99',
    'data':'{"spm":"a311n.7676424/d.1002.1","prepvid":"201'
           '_10.184.72.35_28093043_1514193031224","q":"秋冬裙","pi'
           'd":"mm_33231688_7050284_23466709","clk1":"undefined","a'
           'c":"SILHEuewUQ8CAXBAuwKA7ZLE","page":1,"pvid":"201_10.'
           '184.72.35_28093043_1514255059871","bucket_info":"_TL-390'
           '15","bucket":"_TL-39015","useItemCouponPage":"1","lunaUr'
           'lParam":"{\"algo_sort\":\"mixcoupon\",\"rank\":\"rank_pro'
           'file:FirstRankScorer_atbh5\",\"PS\":\"tk_item_score_atbh5\",\"ap'
           'pBucket\":\"d\"}","aplus_ab_b":"/d","sort":"sales_desc","nickname":""}'
}




res=requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, 'lxml')
print(soup)
md5 = hashlib.md5(s.encode('utf-8')).hexdigest()
my_md5 = hashlib.md5()
my_md5.update(s.encode('utf-8'))
my_md5 = my_md5.hexdigest()
print(my_md5.upper())