# -*-coding=utf-8-*-

import os
import subprocess
import time
import urllib.request  # noqa F401

import pandas as pd
import pync
import tushare as ts

from utils.larkbot import LarkBot


def show_notification(title, text):
    os.system(
        """
              osascript -e 'display notification "{}" with title "{}"'
              """.format(
            text, title
        )
    )


def show_notification_2(title, text):
    cmd = 'display notification "' + text + '" with title "' + title + '"'
    subprocess.call(["osascript", "-e", cmd])


"""
使用mac系统定时任务crontab设置告警通知的执行时间。
crontab设置过程
    1. 输入crontab -e进入设置文本。
    2. 填写 */3 9-12,13-15 * * 1-5 /usr/local/bin/python3 /Users/marx_luo/PythonWorkspace/stock/stock_alarm.py，
    即周一到周五，上午9点到12点，下午1点到3点，每三分钟执行阀值告警。
"""

stocks_pool = [
    {"code": "sz000063", "name": "中兴通讯", "min_threshold": "26", "max_threshold": "38"},
    {"code": "sh000016", "name": "上证50"},
]


def get_data(ts_code):
    pro = ts.pro_api("your token")
    try:
        df = pro.fund_daily(ts_code=ts_code)
    except:  # noqa E722
        time.sleep(0.5)
        print("获取数据失败")
    else:
        print("获取数据成功")

    # 对数据进行处理符合backtrader格式
    columns = ["trade_date", "open", "high", "low", "close", "vol"]
    df = df[columns]
    # 转换日期格式
    df["trade_date"] = df["trade_date"].apply(lambda x: pd.to_datetime(str(x)))
    bt_col_dict = {"vol": "volume", "trade_date": "datetime"}
    df = df.rename(columns=bt_col_dict)
    df = df.set_index("datetime")
    # openinterest 默认为0
    df["openinterest"] = 0
    # 由于获取的数据的第一行是最新数据，需要重新排列，否则最新日期的均线数据为空
    df = df.sort_index()
    return df


def check_strategy():

    return True


def check(code, low, high):
    # for ind, stock in enumerate(stocks_pool):
    # 	response = str(urllib.request.urlopen(f"http://hq.sinajs.cn/list={stock['code']}").read())
    # 	stockData = response.split("\"")[1].split(",")

    df = ts.get_realtime_quotes(code)
    # df = get_data('510300.SH') # 获取沪深300ETF数据
    # print(df)
    e = df[["code", "name", "price", "date", "time"]]
    p = df["price"]
    print(e)
    if float(p[0]) > low and float(p[0]) < high:
        return True
    else:
        return False


while True:
    WEBHOOK_SECRET = "wNMVU3ewSm2F0G2TwTX4Fd"
    bot = LarkBot(secret=WEBHOOK_SECRET)
    if check("sh", 3200, 10000) or check("601318", 0, 49):
        bot.send(content="[Signal💡] 中国平安 低于 ¥49")

        priceNow = 48
        pync.notify(
            f'{"中国平安"}当前价格为{priceNow}', title=f'{"中国平安"}股票已低于设定值{49}',
        )
        pync.notify(
            'Reminder - Drink Water, Sir', 
            title='Qbot', 
            open='https://ufund-me.github.io/',
            # appIcon='https://raw.githubusercontent.com/UFund-Me/Qbot/main/gui/imgs/UFund.png',
            # appIcon='https://ufund-me.github.io/img/UFund.png',
            # appIcon='https://ufund-me.github.io/img/logo.ico',
            appIcon='./gui/imgs/logo.ico'
        )
        # show_notification("Title", "notification")
        # pync.notify(
        #     f'{stocks_pool["name"]}当前价格{priceNow}',
        #     title=f'{stocks_pool["name"]}股票已低于设定值{stocks_pool["min_threshold"]}',
        # )

        # if linux
        # os.system('play ./qbot/sounds/alert-bells.wav')
        # if MacOs
        os.system("afplay ./qbot/sounds/bell.wav")

        exit()
    time.sleep(1)
