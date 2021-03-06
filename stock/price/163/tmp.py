import requests,re,time
from lxml import etree
import sqlite3
import pandas as pd
import numpy as np

class StockCode(object):
	def __init__(self):
		self.start_url_sh = "http://quote.eastmoney.com/stocklist.html#sh"
		self.start_url_sz = "http://quote.eastmoney.com/stocklist.html#sz"
		self.headers = {
			"User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
		}
 
	def parse_url(self):
		# 发起请求，获取响应
		response_sh = requests.get(self.start_url_sh, headers=self.headers)
		if response_sh.status_code == 200:
			sh=response_sh.content
		response_sz = requests.get(self.start_url_sz, headers=self.headers)
		if response_sz.status_code == 200:
			sz=response_sz.content
		return etree.HTML(sh+sz)
 
	def get_code_list(self, response):
		# 得到股票代码的列表
		node_list = response.xpath('//*[@id="quotesearch"]/ul[1]/li')
		code_list = []
		for node in node_list:
			try:
				code = re.match(r'.*?\((\d+)\)', etree.tostring(node).decode()).group(1)
				print(code)
				code_list.append(code)
			except:
				continue
		return code_list
 
	def run(self):
		html = self.parse_url()
		return self.get_code_list(html)
class Download_HistoryStock(object):
 
	def __init__(self, code):
		self.code = code
		self.start_url = "http://quotes.money.163.com/trade/lsjysj_" + self.code + ".html"
		# print self.start_url
		self.headers = {
			"User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
		}
 
	def parse_url(self):
 
		response = requests.get(self.start_url)
		# print response.status_code
		if response.status_code == 200:
			return etree.HTML(response.content)
		return False
 
	def get_date(self, response):
		# 得到开始和结束的日期
		start_date = ''.join(response.xpath('//input[@name="date_start_type"]/@value')[0].split('-'))
		end_date = ''.join(response.xpath('//input[@name="date_end_type"]/@value')[0].split('-'))
		return start_date,end_date
 
	def download(self, start_date, end_date):
		download_url = "http://quotes.money.163.com/service/chddata.html?code=0"+self.code+"&start="+start_date+"&end="+end_date+"&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
		data = requests.get(download_url)
		f = open(self.code + '.csv', 'wb')
 
		for chunk in data.iter_content(chunk_size=10000):
			if chunk:
				f.write(chunk)
		print('股票---',self.code,'历史数据正在下载')
 
	def run(self):
		try:
			html = self.parse_url()
			start_date,end_date = self.get_date(html)
			self.download(start_date, end_date)
		except Exception as e:
			print(e)

if __name__ == '__main__':
	code = StockCode()
	code_list = code.run()
	print(len(code_list))
	conn = sqlite3.connect('test.db')
	# df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3']})
	df = pd.DataFrame({'stockcode' : code_list})
	df.to_sql('stockcode', con=conn, if_exists='replace')
	# for temp_code in code_list:
	# 	time.sleep(1)
	# 	download = Download_HistoryStock(temp_code)
	# 	download.run()

