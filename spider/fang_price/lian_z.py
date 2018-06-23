import  requests
import  re
from bs4 import BeautifulSoup
#url="http://sh.lianjia.com/ershoufang/d1s7"

def parse(url):
    res= requests.get(url)
    #res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    # sumlin = soup.find('a', "laisuzhou").next_element
    # sumlink = soup.find('a', "laisuzhou").next_sibling
    # umli = soup.find('a', "laisuzhou").next_sibling.next_sibling
    # for li in sumlin:
    #     print(repr(li))
    #     #print(repr(sumli))

    sumlin = soup.find_all('div', "info")
    #data=soup.find('div', "info").find_previous_sibling().find('img')
   # print(data)
    for i in sumlin:
        data=i.find_previous_sibling().find('img')
        text=str(data["data-img-layout"])
        m=re.search('\d{8}', text)
        if m:
            print(m.group(0))
        print(data["alt"])
        price=i.find('div', "info-col price-item main")
        priceper = i.find('span', "info-col price-item minor")
        mianji = i.find('span', "info-col row1-text")
        print(i.find('a','laisuzhou').text)
        print(i.find('a','laisuzhou').find_next('a').text)
        print(i.find('a', 'laisuzhou').find_next('a').find_next('a').text)
        print(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[0].strip())
        print(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[1].strip())
        print(str(priceper.text).replace('\n', '').lstrip().rstrip().strip())
        print(str(price.text).replace('\n', '').lstrip().rstrip().strip())


        #print(sumlink)
    # for lin in sumlink:
    #     title = lin.find('a', "laisuzhou")
    #     priceper = lin.find('span', "info-col price-item minor")
    #     price=lin.find('div', "info-col price-item main")
    #     mianji =lin.find('span', "info-col row1-text")

        # if title:
        #     print(str(title.text).replace('\n', '').lstrip().rstrip().strip())
        #     print(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[0].strip())
        #     print(str(mianji.text).replace('\n', '').lstrip().rstrip().split('|')[1].strip())
        #     print(str(priceper.text).replace('\n', '').lstrip().rstrip().strip())
        #     print(str(price.text).replace('\n', '').lstrip().rstrip().strip())
#parse(url)
url2="http://sh.lianjia.com/ershoufang/d{}s7"
for i in range(1,101):
    url3=url2.format(i)
    parse(url3)

