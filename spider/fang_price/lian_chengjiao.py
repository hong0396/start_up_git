import  requests
from bs4 import BeautifulSoup
url="http://sh.lianjia.com/chengjiao/"

def parse(url):
    res= requests.get(url)
    #res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    sumlink = soup.find_all('li')
    #print(sumlink)
    for lin in sumlink:
        #title=lin.find('p', 'title').text
        title = lin.find('img','lj-lazy')
        #large=lin.find('div',"area alignR").find('p').text
        priceper = lin.find('div', "info-col price-item minor")
        price=lin.find('span', "strong-num")
        if title:
            print(title['alt'])
            print(priceper.text)
            print(price.text)
parse(url)
url2="http://sh.lianjia.com/chengjiao/d{}/"
for i in range(2,101):
    url3=url2.format(i)
    parse(url3)

