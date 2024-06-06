# -*-coding=utf-8-*-

"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-02-13 23:24:15
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-09 23:59:44
FilePath: /Qbot/pytrader/doc/05.kdj_macd_in_A_market/batch_kdj_macd.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
Description:

Copyright (c) 2023 by Charmve, All Rights Reserved.
"""

import datetime
import os.path
import pickle  # noqa F401
import sys

import backtrader as bt
from backtrader.indicators import EMA


class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.volume = self.datas[0].volume

        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 9个交易日内最高价
        self.high_nine = bt.indicators.Highest(self.data.high, period=9)
        # 9个交易日内最低价
        self.low_nine = bt.indicators.Lowest(self.data.low, period=9)
        # 计算rsv值
        self.rsv = 100 * bt.DivByZero(
            self.data_close - self.low_nine, self.high_nine - self.low_nine, zero=None
        )
        # 计算rsv的3周期加权平均值，即K值
        self.K = bt.indicators.EMA(self.rsv, period=3, plot=False)
        # D值=K值的3周期加权平均值
        self.D = bt.indicators.EMA(self.K, period=3, plot=False)
        # J=3*K-2*D
        self.J = 3 * self.K - 2 * self.D

        # MACD策略参数
        me1 = EMA(self.data, period=12)
        me2 = EMA(self.data, period=26)
        self.macd = me1 - me2
        self.signal = EMA(self.macd, period=9)
        bt.indicators.MACDHisto(self.data)

    @staticmethod
    def percent(today, yesterday):
        """
        差值占比

        Arguments:
            today {float} -- 今天的数据
            yesterday {float} -- 昨天的数据

        Returns:
            float -- 差值占比
        """
        return float(today - yesterday) / today

    def next(self):
        if not self.position:
            # 买入基于MACD策略
            condition1 = self.macd[-1] - self.signal[-1]
            condition2 = self.macd[0] - self.signal[0]
            if condition1 < 0 and condition2 > 0:
                self.order = self.buy()

        else:
            # 卖出基于KDJ策略
            condition1 = self.J[-1] - self.D[-1]
            condition2 = self.J[0] - self.D[0]
            if condition1 > 0 or condition2 < 0:
                self.order = self.sell()


def run_cerebro(stock_file, result):
    """
    运行策略
    :param stock_file: 股票数据文件位置
    :param result: 回测结果存储变量
    """

    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    # 加载数据到模型中
    data = bt.feeds.GenericCSVData(
        dataname=stock_file,
        fromdate=datetime.datetime(2010, 1, 1),
        todate=datetime.datetime(2020, 5, 10),
        dtformat="%Y%m%d",
        datetime=2,
        open=3,
        high=4,
        low=5,
        close=6,
        volume=10,
        reverse=True,
    )
    cerebro.adddata(data)

    # 本金10000，每次交易100股
    init_cash = 100000.0
    print("初始资金: ", init_cash)
    cerebro.broker.setcash(init_cash)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 万五佣金
    cerebro.broker.setcommission(commission=0.0005)

    # 运行策略
    cerebro.run()

    # 剩余本金
    money_left = cerebro.broker.getvalue()
    print("剩余本金: ", money_left)

    # 获取股票名字
    stock_name = stock_file.split("\\")[-1].split(".csv")[0]

    # 将最终回报率以百分比的形式返回
    result[stock_name] = float(money_left - init_cash) / init_cash


files_path = "./thoudsand_stocks/"
result = {}

# 遍历所有股票数据
for stock in os.listdir(files_path):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, files_path + stock)
    print(datapath)
    try:
        run_cerebro(datapath, result)
    except Exception as e:
        print(e)

# 计算
pos = []
neg = []
for data in result:
    res = result[data]
    if res > 0:
        pos.append(res)
    else:
        neg.append(res)
print(f"正收益数量: {len(pos)}, 负收益数量:{len(neg)}")
