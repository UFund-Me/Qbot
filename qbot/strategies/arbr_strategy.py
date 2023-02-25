#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ****************************************************************************
#  Description:  情绪指标，简称 ARBR 或 BRAR，由人气指标（AR）和意愿指标（BR）构成。
#  AR 和 BR 都是对通过对历史股价走势的分析，反映市场当前情况下多空双方的力量强弱对比，
#  推断市场交易情绪，从而对趋势的形成与反转作出预判。
#
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************


import matplotlib.pyplot as plt
import numpy as np  # noqa F401
import pandas as pd
import talib as ta
import tushare as ts
from pylab import mpl

# %matplotlib inline
# 正常显示画图时出现的中文和负号


mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

# 设置token

token = "6f747880359ef14fe2fd5fc0c2c08a4e09a47e7ac161d643ae7036c0"
pro = ts.pro_api(token)

index = {
    "上证综指": "000001.SH",
    "深证成指": "399001.SZ",
    "沪深300": "000300.SH",
    "创业板指": "399006.SZ",
    "上证50": "000016.SH",
    "中证500": "000905.SH",
    "中小板指": "399005.SZ",
    "上证180": "000010.SH",
}

# 获取当前交易的股票代码和名称
def get_code():
    df = pro.stock_basic(exchange="", list_status="L")
    codes = df.ts_code.values
    names = df.name.values
    stock = dict(zip(names, codes))
    stocks = dict(stock, **index)
    return stocks


# 默认设定时间周期为当前时间往前推120个交易日
# 日期可以根据需要自己改动
def get_data(code, n=120):
    from datetime import datetime, timedelta

    t = datetime.now()
    t0 = t - timedelta(n)
    start = t0.strftime("%Y%m%d")
    end = t.strftime("%Y%m%d")

    # 如果代码在字典index里，则取的是指数数据
    if code in index.values():
        df = pro.index_daily(ts_code=code, start_date=start, end_date=end)
    # 否则取的是个股数据
    else:
        df = pro.daily(ts_code=code, start_date=start, end_date=end)

    # 将交易日期设置为索引值
    df.index = pd.to_datetime(df.trade_date)
    df = df.sort_index()

    # 计算收益率
    return df


# 计算AR、BR指标


def arbr(stock, n=120):
    code = get_code()[stock]
    df = get_data(code, n)[["open", "high", "low", "close"]]
    df["HO"] = df.high - df.open
    df["OL"] = df.open - df.low
    df["HCY"] = df.high - df.close.shift(1)
    df["CYL"] = df.close.shift(1) - df.low

    # 计算AR、BR指标
    df["AR"] = ta.SUM(df.HO, timeperiod=26) / ta.SUM(df.OL, timeperiod=26) * 100
    df["BR"] = ta.SUM(df.HCY, timeperiod=26) / ta.SUM(df.CYL, timeperiod=26) * 100
    return df[["close", "AR", "BR"]].dropna()


# 对价格和ARBR进行可视化


def plot_arbr(stock, n=120):
    df = arbr(stock, n)
    df["close"].plot(color="r", figsize=(14, 5))
    plt.xlabel("")
    plt.title(stock + "价格走势", fontsize=15)
    df[["AR", "BR"]].plot(figsize=(14, 5))
    plt.xlabel("")
    plt.show()


plot_arbr("上证综指")
plot_arbr("上证综指", n=250)
plot_arbr("创业板指", n=250)
plot_arbr("沪深300", n=250)
plot_arbr("东方通信", n=250)
