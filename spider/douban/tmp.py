import requests
from bs4 import BeautifulSoup

def getContent(bsItem):
    content=[]
    content.append(item.find('a')['href'])
    film=item.find_all('span',{'class':'title'})
    film[0]=film[0].string
    if len(film) > 1:
        film[1]=film[1].string.replace(u'\xa0','').replace(r'/','')
    else:
        film.append('无外语名')
    content.append(film)
    content.append(item.find('span',{'class':'rating_num'}).string)
    content.append(item.find('span',{'class':'','property':''}).string)
    return content

starturl = 'https://movie.douban.com/top250'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            }
params={'start':0}

s = requests.Session()
s.headers.update(headers)
curpage = 0
with open('doubanfilm.txt','w',encoding='utf-8') as f:
    while(curpage<250):
        params['start'] = curpage
        resp = s.get(starturl,params=params)
        bs = BeautifulSoup(resp.text,'html.parser')
        for item in bs.find_all('div',{"class":'info'}):
            f.write(str(getContent(item))+'\n')
        curpage += 25
print('bug end')
s.close()        