import  requests
from bs4 import BeautifulSoup
url="http://sh.lianjia.com/ershoufang/"

def parse(url):
    res= requests.get(url)
    #res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    sumlink = soup.find_all('li')
    #print(sumlink)
    for lin in sumlink:
        title = lin.find('a', "laisuzhou")
        priceper = lin.find('span', "info-col price-item minor")
        price=lin.find('div', "info-col price-item main")
        mianji =lin.find('span', "info-col row1-text")

        if title:
            print(str(title.text).replace('\n', '').lstrip().rstrip().strip())
            print(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[0].strip())
            print(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[1].strip())
            print(str(priceper.text).replace('\n', '').lstrip().rstrip().strip())
            print(str(price.text).replace('\n', '').lstrip().rstrip().strip())
parse(url)
url2="http://sh.lianjia.com/ershoufang/d{}/"
for i in range(2,101):
    url3=url2.format(i)
    parse(url3)

