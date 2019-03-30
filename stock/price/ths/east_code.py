from selenium import webdriver
import time, os
from bs4 import BeautifulSoup


chromedriver = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(executable_path=chromedriver)

def getHtml(url):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    return soup
def findlist():
    url="http://quote.eastmoney.com/stocklist.html"
    soup= getHtml(url)
    search= soup.find("div",{"id":"quotesearch"})
    ullist=search.find_all("ul")
    for ul in ullist:
        lilist= ul.find_all("li")
        for li in lilist:
            data = []
            a= li.find("a",{"target":"_blank"})
            data.append(a.string)
            data.append(a.attrs["href"])
            stocklist.append(data)


def finddata(soup):
    singledata = {}
    datadiv=soup.find("div",{"class":"qphox layout mb7 clearfix"})
    if(datadiv==None):
        datadiv=soup.find("div",{"class":"qphox layout mb7"})
        if(datadiv!=None):
            singledata= finddata2(datadiv,singledata)
        return singledata
    strong=datadiv.find("div",{"id":"arrowud"}).strong
    singledata["color"]=strong.attrs["class"][-1]
    singledata["number"]=strong.string
    ullist=datadiv.find_all("ul")
    for ul in ullist:
        lilist=ul.find_all("li")
        for li in lilist:
            singledata[li.span.string]=li.span.nextSibling.string
    return singledata

def finddata2(datadiv,singledata):
    strong=datadiv.find("strong",{"id":"price9"})
    singledata["color"] = strong.attrs["class"][-1]
    singledata["number"] = strong.string
    trlist=datadiv.find_all("tr")
    i=1
    for tr in trlist:
        tdlist=tr.find_all("td")
        for td in tdlist:
            if(td.attrs=={}):
                singledata[td.string]=tr.find("td",{"id":"gt"+str(i)}).string
                i = i + 1
    return singledata
aa=findlist()


# soup=getHtml(url)
# singledata=finddata(soup)
# finddata2(datadiv,singledata)