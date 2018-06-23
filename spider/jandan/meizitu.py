import imageio
import json
import  os
import random
import  re
import  requests
import shutil
import time
from  bs4 import BeautifulSoup
from  urllib  import  request
from urllib.request import urlretrieve
from multiprocessing import Pool

url="http://www.meizitu.com/a/list_1_{}.html"
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"


}
my_headers = [
    'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
    'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
header={"User-Agent":random.choice(my_headers)}
#writeGif(filename, images, duration=0.5, subRectangles=False)
def meizi(url):
    res=requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')
    lis=soup.find_all('div','con')
    for i in lis:
        r = requests.get(i.find('a').get('href'),headers=headers)
        time.sleep(2)
        s = BeautifulSoup(r.content, 'lxml')
        for j in s.find('div','postContent').find_all('p')[1].find_all('img'):
            img=str(j.get('src'))
            name = img[-18:].replace('/','_')
            folder = img[-18:-10].replace('/','_')
            html = requests.get(img, headers=headers)
            time.sleep(2)
            print(html)
            if not os.path.isdir("E:\\picture\\"+folder):
                os.makedirs("E:\\picture\\"+folder)
            else:
                pass
            if not os.path.exists("E:\\picture\\"+folder+"\\"+name) :
                print('---------正在写入jpg--------------')
                with open("E:\\picture\\"+folder+"\\"+name, 'wb+') as file:
                    file.write(html.content)
                    file.close()
                print('---------写入完成jpg--------------')
            else:
                pass




                        # img=str(i['src'])
        # gif = i.get('org_src')
        # html = requests.get('http:' + img, stream=True)
        # name = img.split(r'/')[-1]
        #



        # if not os.path.exists("E:\\picture\\"+name) :
        #     if gif:
        #         print('---------正在写入gif--------------')
        #         with open("E:\\picture\\"+name, 'wb') as f:
        #             f.write(requests.get('http:' + gif).content)
        #             f.close()
        #         print('---------写入完成gif--------------')
        #     else:
        #         print('---------正在写入jpg--------------')
        #         with open("E:\\picture\\"+name, 'ab') as file:
        #             file.write(html.content)
        #             file.close()
        #         print('---------写入完成jpg--------------')
        #

#
#meizi(url)
if  __name__ == '__main__':
    pool = Pool()
    pool.map(meizi, [url.format(i) for i in range(1, 10)])
#
#for i in range(1, 5):
#    urls = url.format(i)
#    meizi(urls)









    # html = requests.get('http:'+img, stream=True)
    # name=img.split(r'/')[-1]
    # print('http:'+img)
    # if str(name).split('.')[-1] == 'gif':
    # with open(name, 'wb') as f:
    #     f.write(requests.get('http:'+img).content)
    #     f.close()
    # with open(name, 'wb') as f:
    #     html.raw.decode_content = True
    #     shutil.copyfileobj(html.raw, f)
    #     f.close()

    # with imageio.get_writer(name, mode='I') as writer:
    #         image = imageio.imread(html.content)
    #         writer.append_data(image)

    # with Image.open(name, 'wb') as file:
    # gifmaker.makedelta(file, html.content)
    # .save('filename.gif', save_all=True)
    #        file.close()
    # else:
    #     with open(name, 'ab') as file:
    #         file.write(html.content)
    #         file.close()



