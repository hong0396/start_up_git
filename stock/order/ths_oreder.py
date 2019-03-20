# -*- coding: utf-8 -*-
# author:llx  time: 2018/4/24

from pywinauto.application import Application
import SendKeys
import pandas as pd
from datetime import datetime
import time as time_wait


def buy(path, code, price, num):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["Edit"].TypeKeys(code)
    app[u"网上股票交易系统5.0"]["Edit2"].TypeKeys(price)
    app[u"网上股票交易系统5.0"]["Edit3"].TypeKeys(num)
    app[u"网上股票交易系统5.0"][u"买入[B]"].click()



def sell(path, code, price, num):
    app = Application().connect(path=path)
    # app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["Edit4"].TypeKeys(code)
    app[u"网上股票交易系统5.0"]["Edit5"].TypeKeys(price)
    app[u"网上股票交易系统5.0"]["Edit6"].TypeKeys(num)
    app[u"网上股票交易系统5.0"][u"卖出[S]"].click()


def cancel_all(path):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].click_input()
    SendKeys.SendKeys('R')
    app[u"网上股票交易系统5.0"][u"全撤(Z /)"].click()


def cancel_sell(path):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].click_input()
    SendKeys.SendKeys('R')
    app[u"网上股票交易系统5.0"][u"撤卖(C)"].click()


def cancel_buy(path):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].click_input()
    SendKeys.SendKeys('R')
    app[u"网上股票交易系统5.0"][u"撤买(X)"].click()


def available_money(path):
    app = Application().connect(path=path)
    # app[u"网上股票交易系统5.0"]["Static19"].click_input()
    # SendKeys.SendKeys('{F5}')
    money = float(app[u"网上股票交易系统5.0"]["Static19"].texts()[0])
    return money


def inquire_position(path):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].click_input()
    SendKeys.SendKeys('W')
    SendKeys.SendKeys('{F5}')
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].TypeKeys('^c')
    data = pd.read_clipboard()
    return data


def inquire_deal(path):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].click_input()
    SendKeys.SendKeys('E')
    SendKeys.SendKeys('{F5}')
    time_wait.sleep(0.5)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].TypeKeys('^c')

    try:
        data = pd.read_clipboard()
        day = str(datetime.now().date())
        time = [pd.to_datetime(day + " " + i) for i in data["成交时间"]]
        data.index = time
        return data
    except:
        return None


def inquire_commit(path):
    app = Application().connect(path=path)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].click_input()
    SendKeys.SendKeys('R')
    SendKeys.SendKeys('{F5}')
    time_wait.sleep(0.5)
    app[u"网上股票交易系统5.0"]["CVirtualGridCtrl"].TypeKeys('^c')
    try:
        data = pd.read_clipboard()
        day = str(datetime.now().date())
        time = [pd.to_datetime(day + " " + i) for i in data["委托时间"]]
        data.index = time
        return data
    except:
        return None


if __name__ == '__main__':

    # path = r"D:\Program Files\weituo\zhongxin\xiadan.exe"
    path = r"D:\Program Files\weituo\zhongtai\xiadan.exe"
    code = "510900"
    price = "1.215"
    num = "100"
    buy(path, code, price, num)  # 下买单
    # sell(path, code, price, num)  # 下卖单
    # cancel_all(path)  # 撤所有未成交
    # cancel_sell(path)  # 撤卖单
    # cancel_buy(path)  # 撤买单
    # money = available_money(path)  # 查询账户余额
    # print money  # 下单前查询，之后稍等才可以查到正确数据
    # posion_data = inquire_position(path)  # 查询持仓详情
    # print posion_data
    # deal_data = inquire_deal(path)  # 查询成交详情
    # print deal_data
    # commit_data = inquire_commit(path)  # 查询委托详情
    # print commit_data


    # about_dlg = app.window_(title_re = u"关于", class_name = "#32770")
