# coding:utf-8

import time
import requests
from lxml import etree
# import pymysql as mdb
import datetime

# For Python 3.6+
# coding:utf-8

# 从代理ip网站上总共要爬取的ip页数。一般每页20条，小项目(20-30个代理ip即可完成的)可以设置为1-2页。
page_num = 1

# 对已经检测成功的ip测试轮次。普通爬虫服务设置1轮足矣，若希望减少抓取数据缺失，可适当提高轮次，然而可能ip也将更少。
examine_round = 1

# 超时时间。代理ip在测试过程中的超时时间。
timeout = 1.5

#如果超过这个时间就在数据库里删除
delet_timeout = 3

# 数据库链接地址
host = '127.0.0.1'

# 数据库链接端口
port = 3306

# 数据库链接用户名
user = 'root'

# 数据库密码
passwd = '******'

# 数据库名
DB_NAME = 'proxies'

# 表名
TABLE_NAME = 'valid_ip'

# 数据库字符
charset = 'utf8'
class IPFactory:
    """
    代理ip抓取/评估/存储一体化。
    """
    def __init__(self):
        self.page_num = page_num
        self.round = examine_round
        self.timeout = timeout
        self.all_ip = set()
        self.delet_timeout = delet_timeout
        # 创建数据库
        #self.create_db()

        # # 抓取全部ip
        # current_ips = self.get_all_ip()
        # # 获取有效ip
        # valid_ip = self.get_the_best(current_ips, self.timeout, self.round)
        # print valid_ip

    def create_db(self):
        """
        创建数据库用于保存有效ip
        """
        # 创建数据库/表语句
        # 创建数据库
        drop_db_str = 'drop database if exists ' + DB_NAME + ' ;'
        create_db_str = 'create database ' + DB_NAME + ' ;'
        # 选择该数据库
        use_db_str = 'use ' + DB_NAME + ' ;'
        # 创建表格
        create_table_str = "CREATE TABLE " + TABLE_NAME + """(
          `content` varchar(30) NOT NULL,
          `test_times` int(5) NOT NULL DEFAULT '0',
          `failure_times` int(5) NOT NULL DEFAULT '0',
          `success_rate` float(5,2) NOT NULL DEFAULT '0.00',
          `avg_response_time` float NOT NULL DEFAULT '0',
          `score` float(5,2) NOT NULL DEFAULT '0.00'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        # 连接数据库
        conn = mdb.connect(host, user, passwd)
        cursor = conn.cursor()
        try:
            cursor.execute(drop_db_str)
            cursor.execute(create_db_str)
            cursor.execute(use_db_str)
            cursor.execute(create_table_str)
            conn.commit()
        except OSError:
            print ("无法创建数据库！")
        finally:
            cursor.close()
            conn.close()

    def get_content(self, url, url_xpath, port_xpath):
        """
        使用xpath解析网页内容,并返回ip列表。
        """
        # 返回列表
        ip_list = []

        try:
            # 设置请求头信息
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

            # 获取页面数据
            results = requests.get(url, headers=headers, timeout=4)
            tree = etree.HTML(results.text)

            # 提取ip:port
            url_results = tree.xpath(url_xpath)
            port_results = tree.xpath(port_xpath)
            urls = [line.strip() for line in url_results]
            ports = [line.strip() for line in port_results]

            if len(urls) == len(ports):
                for i in range(len(urls)):
                    # 匹配ip:port对
                    full_ip = urls[i]+":"+ports[i]
                    # 此处利用all_ip对过往爬取的ip做了记录，下次再爬时如果发现
                    # 已经爬过，就不再加入ip列表。
                    if full_ip in self.all_ip:
                        continue
                    # 存储
                    ip_list.append(full_ip)
        except Exception as e:
            print ('get proxies error: ', e)

        return ip_list

    def get_all_ip(self):
        """
        各大网站抓取的ip聚合。
        """
        # 有2个概念：all_ip和current_all_ip。前者保存了历次抓取的ip，后者只保存本次的抓取。
        current_all_ip = set()

        ##################################
        # 66ip网
        ###################################
        url_xpath_66 = '/html/body/div[last()]//table//tr[position()>1]/td[1]/text()'
        port_xpath_66 = '/html/body/div[last()]//table//tr[position()>1]/td[2]/text()'
        for i in range(self.page_num):
            url_66 = 'http://www.66ip.cn/' + str(i+1) + '.html'
            results = self.get_content(url_66, url_xpath_66, port_xpath_66)
            self.all_ip.update(results)
            current_all_ip.update(results)
            # 停0.5s再抓取
            time.sleep(0.5)

        ##################################
        # xici代理
        ###################################
        url_xpath_xici = '//table[@id="ip_list"]//tr[position()>1]/td[position()=2]/text()'
        port_xpath_xici = '//table[@id="ip_list"]//tr[position()>1]/td[position()=3]/text()'
        for i in range(self.page_num):
            url_xici = 'http://www.xicidaili.com/nn/' + str(i+1)
            results = self.get_content(url_xici, url_xpath_xici, port_xpath_xici)
            self.all_ip.update(results)
            current_all_ip.update(results)
            time.sleep(0.5)

        ##################################
        # mimiip网
        ###################################
        url_xpath_mimi = '//table[@class="list"]//tr[position()>1]/td[1]/text()'
        port_xpath_mimi = '//table[@class="list"]//tr[position()>1]/td[2]/text()'
        for i in range(self.page_num):
            url_mimi = 'http://www.mimiip.com/gngao/' + str(i+1)
            results = self.get_content(url_mimi, url_xpath_mimi, port_xpath_mimi)
            self.all_ip.update(results)
            current_all_ip.update(results)
            time.sleep(0.5)

        ##################################
        # kuaidaili网
        ###################################
        url_xpath_kuaidaili = '//td[@data-title="IP"]/text()'
        port_xpath_kuaidaili = '//td[@data-title="PORT"]/text()'
        for i in range(self.page_num):
            url_kuaidaili = 'http://www.kuaidaili.com/free/inha/' + str(i+1) + '/'
            results = self.get_content(url_kuaidaili, url_xpath_kuaidaili, port_xpath_kuaidaili)
            self.all_ip.update(results)
            current_all_ip.update(results)
            time.sleep(0.5)

        return current_all_ip

    def get_valid_ip(self, ip_set, timeout):
        """
        代理ip可用性测试
        """
        # 设置请求地址
        url = 'https://www.baidu.com'

        # 可用代理结果
        results = set()
        # 不可用的代理
        fail_ip = set()
        # 挨个检查代理是否可用
        for p in ip_set:
            proxy = {'http': 'http://'+p}
            try:
                # 请求开始时间
                start = time.time()
                r = requests.get(url, proxies=proxy, timeout=timeout)
                # 请求结束时间
                end = time.time()
                # 判断是否可用
                if r.text is not None:
                    print ('succeed: ' + p + '\t' + " in " + format(end-start, '0.2f') + 's')
                    # 追加代理ip到返回的set中
                    results.add(p)
                else:
                    fail_ip.add(p)
            except OSError:
                print ('timeout:', p)

        return results,fail_ip

    def get_the_best(self, valid_ip, timeout, round):
        """
        N轮检测ip列表，避免"辉煌的15分钟"
        """
        # 循环检查次数
        for i in range(round):
            print ("\n>>>>>>>\tRound\t"+str(i+1)+"\t<<<<<<<<<<")
            # 检查代理是否可用
            valid_ip, _ = self.get_valid_ip(valid_ip, timeout)
            # 停一下
            if i < round-1:
                time.sleep(30)

        # 返回可用数据
        return valid_ip

    def save_to_db(self, valid_ips):
        """
        将可用的ip存储进mysql数据库
        """
        if len(valid_ips) == 0:
            print ("本次没有抓到可用ip。")
            return
        # 连接数据库
        print ("\n>>>>>>>>>>>>>>>>>>>> 代理数据入库处理 Start  <<<<<<<<<<<<<<<<<<<<<<\n")
        print(valid_ips)
        return valid_ips
        print ("\n>>>>>>>>>>>>>>>>>>>> 代理数据入库处理 End  <<<<<<<<<<<<<<<<<<<<<<\n")

    def delete_from_db(self, delet_ips):
        """
        从mysql数据库删除代理
        """
        if len(delet_ips) == 0:
            print ("没有可删除ip。")
            return
        # 连接数据库
        print ("\n>>>>>>>>>>>>>>>>>>>> 代理数据删除处理 Start  <<<<<<<<<<<<<<<<<<<<<<\n")
        conn = mdb.connect(host, user, passwd, DB_NAME)
        cursor = conn.cursor()
        try:
            for item in delet_ips:
                # 检查表中是否存在数据
                item_exist = cursor.execute('SELECT * FROM %s WHERE content="%s"' %(TABLE_NAME, item))

                # 删除代理
                if item_exist == 1:
                    # 删除数据
                    n = cursor.execute('DELETE FROM %s WHERE content="%s"' %(TABLE_NAME, item))
                    conn.commit()

                    # 输出删除状态
                    if n:
                        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" 删除成功。\n")
                    else:
                        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" 删除失败。\n")

                else:
                    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+ item +" 不存在。\n")
        except Exception as e:
            print ("删除失败：" + str(e))
        finally:
            cursor.close()
            conn.close()
        print ("\n>>>>>>>>>>>>>>>>>>>> 代理数据删除 End  <<<<<<<<<<<<<<<<<<<<<<\n")

    def get_proxies(self):
        ip_list = []

        # 连接数据库
        conn = mdb.connect(host, user, passwd, DB_NAME)
        cursor = conn.cursor()

        # 检查数据表中是否有数据
        try:
            ip_exist = cursor.execute('SELECT * FROM %s ' % TABLE_NAME)

            # 提取数据
            result = cursor.fetchall()

            # 若表里有数据　直接返回，没有则抓取再返回
            if len(result):
                for item in result:
                    ip_list.append(item[0])
            else:
                # 获取代理数据
                current_ips = self.get_all_ip()
                valid_ips,_ = self.get_the_best(current_ips, self.timeout, self.round)
                self.save_to_db(valid_ips)
                ip_list.extend(valid_ips)
        except Exception as e:
            print ("从数据库获取ip失败！")
        finally:
            cursor.close()
            conn.close()

        return ip_list
ip_factory = IPFactory()

def ip_get_test_save(timeout,round):

    ip_factory = IPFactory()
    ips = ip_factory.get_all_ip()
    bestIp = ip_factory.get_the_best(ips,timeout,round)
    ip_list=ip_factory.save_to_db(bestIp)
    return ip_list

def test_ip_and_delete ():

    ips = ip_factory.get_proxies()
    _,about_to_deletes = ip_factory.get_valid_ip(ips,timeout=ip_factory.timeout)
    ip_factory.delete_from_db(about_to_deletes)

# if __name__ == '__main__':
#     ip_get_test_save(1.5,1)
#     #test_ip_and_delete()