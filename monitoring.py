# coding:utf-8
# 1000元实盘练习程序
# 服务器端监控程序


import numpy as np
import pandas as pd
# import akshare as ak
import efinance as ef
import run
import kline
import backtest
from utils.send_email import send_email
import talib
import os
import datetime
import time
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.blocking import BlockingScheduler


# 检测k线有无method所定义的形态
@run.change_dir
def test(codes, method):
    # print("检测k线形态")
    results = {}
    for code in codes:
        date = []
        filename = "./data2/" + code[2:] + ".csv"
        # print("测试1", code)
        if os.path.exists(filename):
            data = pd.read_csv(filename)
            # print("测试2", data.info(), data.head(), len(data))
            result = method(data.开盘.values, data.最高.values, data.最低.values, data.收盘.values)
            pos = ()
            pos = list(np.nonzero(result))
            if len(pos[0]) != 0:
                date.append(data.日期[pos[0][-1]])
                results[code] = date
    return results
    
    
# 获取指定股票代码集合的k线符合method形态的位置
def getPosition(codes):
    methods = {
    "上吊线":talib.CDLHANGINGMAN,
    "黄昏星":talib.CDLEVENINGDOJISTAR,
    "看跌吞没":talib.CDLENGULFING,
    "乌云盖顶":talib.CDLDARKCLOUDCOVER,
    "高位孕线":talib.CDLHARAMI,
    "三只乌鸦":talib.CDLIDENTICAL3CROWS,
    "下降三法":talib.CDLRISEFALL3METHODS
    }
    
    today = datetime.datetime.now()
    for name, method in methods.items():
        results = test(codes, method)
        if results:
            print(name, results)
            date = list(results.values())
            date = datetime.datetime.strptime(date[0][0], '%Y-%m-%d %H:%M')
            days = (today - date).days
            print(days)
            # 如果是今天出现的形态
            code = list(results.keys())[0]
            # 报告两天内出现的
            if days <= 2:
                report(date, name, code)
    
    
# 获取股票60分钟线数据
@run.change_dir
def getRecentData(codes, refresh = False, savePath = "./data2/"):
    if refresh == True:
        for code in codes:
            stock_data = ef.stock.get_quote_history(code[2:], klt = 60)
            filename = savePath + code[2:] + ".csv"
            stock_data.to_csv(filename)
    else:
        return
        
        
# 出现卖出形态，向指定邮箱发送警告邮件
@run.change_dir
def report(date, name, code):
    # print("测试", code)
    filename = "./data2/" + code[2:] + ".csv"
    # print(filename)
    if os.path.exists(filename):
        data = pd.read_csv(filename)
        # print(data.info(), data.tail())
        lastestdata = ef.stock.get_latest_stock_info([code[2:]])
        price = lastestdata.最新价.values[0]
        # print(code, date, name, price)
        date = date.strftime('%Y-%m-%d %H:%M')
        title = "报告:" + code[2:] + "出现" + name + "形态"
        content = "股票" + code[2:] + "在" + date + "出现" + name + "形态，股票现价" + str(price)
        print(title, content)
        
        mail_sender = "1144262839@qq.com"
        send_email(mail_sender, mail_receivers, message_text)
        # mail.sentMail(title, content)
        
        
# 进行一次检测
@run.change_dir
def task(codes):
    getRecentData(codes = codes, refresh = True, savePath = "./data2/")
    getPosition(codes)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now, "执行了一次")
    time.sleep(s)

"""    
# 运行死循环，定期检测，每隔s秒检测一次
@run.change_dir
def run(codes, s):
    if s <= 0:
        print("时间间隔需大于0，程序将退出\n")
        return
    while True:
        task(codes)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now, "执行了一次")
        time.sleep(s)
"""


# 每间隔s分钟监控codes股票形态
def run(codes, s):
    scheduler = BlockingScheduler(timezone="Asia/Chongqing")
    scheduler.add_job(task, "cron", day_of_week = "mon-fri", hour = "9-15", minute = "*/"+str(s), args = [codes])
    scheduler.start()


if __name__ == "__main__":
    code = "sh601668"
    codes = [code]
    s = 20
    run(codes, s)
    