import requests
import re
import pandas as pd

stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
# 获取股票代码列表
def urlTolist(url):
    allCodeList = []
    html = requests.get(url).text
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodeList.append(item)
    return allCodeList


allCodelist = urlTolist(stock_CodeUrl)
for code in allCodelist:
    df = pd.read_html('http://quotes.money.163.com/trade/lsjysj_' + code + '.html#06f01')
    print(df[3])
    #df[3]
    print('正在获取%s' % code)
