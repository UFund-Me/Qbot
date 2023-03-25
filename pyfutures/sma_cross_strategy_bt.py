#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-13 21:54:27
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-13 21:54:37
FilePath: /Qbot/pyfutures/cross_strategy_bt.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 采用了AlgoPlus这个第三方包对接ctp期货接口。
建议在国内期货实时交易时段运行ctpExampleLiveSimulation.py，
进行实盘模拟交易，其接收的是1分钟bar或k线实时数据。

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
"""

# 免责声明：作者不保证本程序的正确性，不要据此进行实盘交易，一切后果自负


from datetime import datetime, time, timedelta

import backtrader as bt
import pytz

#################
from AlgoPlus.CTP.FutureAccount import (
    MD_LOCATION,
    SIMNOW_SERVER,
    TD_LOCATION,
    FutureAccount,
    get_simnow_account,
)
from backtrader_ctp_api.ctpstore import CTPStore

# 说明在交易日上午8点45到下午3点，以及晚上8点45到凌晨2点45分，可进行实时行情模拟交易。 （）

# 中国期货交易时段 (日盘/夜盘)，只有在交易时段才能进行实时模拟仿真，其他时段只能进行非实时模拟仿真。双休日不能进行模拟仿真
DAY_START = time(8, 45)  # 日盘8：45开始
DAY_END = time(15, 0)  # 下午3点结束

NIGHT_START = time(20, 45)  # 夜盘晚上8点45开始
NIGHT_END = time(2, 45)  # 凌晨2点45结束

# 是否在交易时段
def is_trading_period():
    """"""
    current_time = datetime.now().time()

    trading = False
    if (
        (current_time >= DAY_START and current_time <= DAY_END)
        or (current_time >= NIGHT_START)
        or (current_time <= NIGHT_END)
    ):
        trading = True

    return trading


class SmaCross(bt.Strategy):
    lines = ("sma",)
    params = dict(
        smaperiod=5,
        bbperiod5=26,
        trade=False,
        stake=10,
        exectype=bt.Order.Market,
        stopafter=0,
        valid=None,
        cancel=0,
        donotcounter=False,
        sell=False,
        usebracket=False,
    )

    def __init__(self):

        self.buy_order = None
        self.live_data = False

        self.move_average = bt.ind.MovingAverageSimple(
            self.data, period=self.params.smaperiod
        )

    def prenext(self):
        print("in prenext")

        for d in self.datas:
            print(
                self.data0.datetime.datetime(0),
                "o h l c ",
                d.open[0],
                d.high[0],
                d.low[0],
                d.close[0],
                " vol ",
                d.volume[0],
            )

    def next(self):
        print("in next")

        for d in self.datas:
            print(
                self.data0.datetime.datetime(0),
                "o h l c ",
                d.open[0],
                d.high[0],
                d.low[0],
                d.close[0],
                " vol ",
                d.volume[0],
            )
        if self.position:
            self.buy()
        else:
            self.sell()

    def notify_order(self, order):
        print("订单状态 %s" % order.getstatusname(), self.broker.getvalue())

    def notify_data(self, data, status, *args, **kwargs):
        dn = data._name
        dt = datetime.now()
        msg = f"Data Status: {data._getstatusname(status)}"
        print(dt, dn, msg)
        if data._getstatusname(status) == "LIVE":
            self.live_data = True
        else:
            self.live_data = False


###########################################################
# 主程序开始
##################
if __name__ == "__main__":

    ctp_setting = get_simnow_account(
        investor_id="089131",  # SimNow账户
        password="350888",  # SimNow账户密码
        server_name="电信1"
        if is_trading_period()
        else "TEST",  # 电信1 、电信2、移动、 TEST , 其中TEST在非交易时段用
    )

    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    store = CTPStore(ctp_setting)

    data = store.getdata(
        dataname="ag2105",
        timeframe=bt.TimeFrame.Minutes,  # ag2105是白银期货
        num_init_backfill=20
        if is_trading_period()
        else 0,  # 初始回填bar数，使用TEST服务器进行模拟实盘时，要设为0
        tz=pytz.timezone("Asia/Shanghai"),
    )

    cerebro.adddata(data)

    cerebro.broker.setcash(10000.0)  # 设置初始资金
    cerebro.run()
