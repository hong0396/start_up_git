#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import requests,time,os,xlwt,xlrd,random
from bs4 import BeautifulSoup
 
class East(object):
    def __init__(self):
        self.Url = 'http://quote.eastmoney.com/stocklist.html'
        self.Data = []
        self.Date = time.strftime('%Y%m%d')
        self.Record = 'E:\\'+'Data'+self.Date+'.xls'
        print (self.Record)
        if os.path.exists(self.Record):
            print ('Record exist...')
        else:
            print ('Get data ...')
            self.get_data()
 
 
    def write_excel(self):
        lis=self.Data
        listkeys = lis[0].keys()  # 找到所有的键值
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        number = 0
 
        for key in list(listkeys):  # 键值需要强制转换成list类型
            sheet.write(0, number, key)
            number = number + 1
 
        x = 1
        for one_dict in lis:  # 遍历列表中所有的字典
            y = 0
            for key in list(listkeys):  # 找到所有键值对应的数据
                sheet.write(x, y, one_dict[key])  # 存入
                y = y + 1
            x = x + 1
 
        wbk.save(self.Record[:-3]+'xls')#保存文件
 
    #爬虫获取数据
    def get_data(self):
        time.sleep(random.randint(1,5)+random.random()) #随机延时?.?s  以防封IP
        #请求数据
        orihtml = requests.get(self.Url).text
        #创建 beautifulsoup 对象
        soup = BeautifulSoup(orihtml,'lxml')
        #采集每一个股票的信息
        count = 0
        for a in soup.find('div',class_='quotebody').find_all('a',{'target':'_blank'}):
            record_d = {}
            #代号
            num = a.get_text().split('(')[1].strip(')')  #获取股票代号
 
            if not (num.startswith('00') or num.startswith('60')):#沪市A股以60开头，深市A股以00开头
                continue#不处理
            record_d['代码']=num
            #详情页
            detail_url = a['href']
            record_d['链接']=detail_url
 
            cwzburl = detail_url
            #发送请求
            try:
                cwzbhtml = requests.get(cwzburl,timeout=30).content  #爬取股票详情页  content是二进制表示    test是unicode型
            except Exception as e:
                print ('perhaps timeout:',e)
                continue
            #创建soup对象
            cwzbsoup = BeautifulSoup(cwzbhtml,'lxml')
 
            #名称
            if len(cwzbsoup.select('div.qphox.header-title h2')):
                name = cwzbsoup.select('div.qphox.header-title h2')[0].get_text() #获取股票名称
                record_d['名称']=name
            else:#有个别股票不能利用此规则读出名称
                continue
 
            try:
                cwzb_list = cwzbsoup.select('div.pad5 table.line23 td') #找到含有div class=pad5的标签，并在该标签下找到含有table class="line23 w100p bt txtUL"的标签 并在该标签下找到所有含td的标签
            except Exception as e:
                print ('error:',e)
                continue
 
            for joke in cwzb_list:
                record_d[joke.get_text().split('：')[0]] = joke.get_text().split('：')[1]#把数据按照键值存入字典
                temp = joke.get_text().split('：')[0]
 
 
            # 去除退市股票以及不能采集到完整数据的股票
            if  (not len(self.Data)) or ((record_d.keys() == self.Data[0].keys()) and (record_d[temp] != '-')):
                self.Data.append(record_d)
                count = count + 1
                print(record_d['名称'])
                # print(record_d['收益(一)'])
        self.write_excel()#数据写入excel
 
 
 
def main():
    test = East()
 
 
 
if __name__ == '__main__':
    main()