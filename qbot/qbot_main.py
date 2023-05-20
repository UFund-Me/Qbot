'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-10 21:12:31
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-23 21:24:23
FilePath: /Qbot/qbot/qbot_main.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 股票量化交易策略：选股、模拟交易过程

也许不用自己写了 https://zhuanlan.zhihu.com/p/552428276

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import imp
import os, sys

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
top_path = os.path.dirname(os.path.abspath(sys.argv[0]))
print('{top_path}/..')
sys.path.append('{top_path}/..')
# sys.path.append('{BASE_DIR}/..')

from strategies.bigger_than_ema_bt import BiggerThanEmaStrategy, get_data
from strategies.klines_bt import KlinesStrategy, get_k_data
from strategies.sma_cross_strategy_bt import SmaCross
from strategies.lstm_strategy_bt import LSTMPredict
# from strategies.rl_strategy_bt import RLStrategy
from strategies.multi_strategy_bt import MultiStrategy

# from strategies.boll_strategy_bt import BollStrategy

# from pytrader.strategies import lgb_strategy, StochRSI, svm_strategy, signal_strategy, rsi_departure_strategy

import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import tushare as ts
import time
import subprocess
from loguru import logger
# from utils.larkbot import LarkBot

from datetime import date, datetime

import os

top_path = os.path.dirname(os.path.abspath(sys.argv[0]))
sounds_file = os.path.join(top_path, "./sounds/bell.wav")


def get_realtime_data(code):
    # 获取实时行情数据
    # quote = api.get_security_quotes([(0, symbol)])
    quote = ts.get_realtime_quotes(code)
    quote = quote.rename(columns={"pre_close" : "close"})

    quote.index = pd.to_datetime(quote.date)
    # quote["date"] = quote.date

    quote["openinterest"] = 0
    quote["nullvalue"] = float('NaN')

    quote['open'] = quote['open'].astype('float')
    quote['close'] = quote['close'].astype('float')
    quote['high'] = quote['high'].astype('float')
    quote['low'] = quote['low'].astype('float')
    quote['volume'] = quote['volume'].astype('float')
    quote['openinterest'] = quote["openinterest"].astype('float')

    ret_data = quote[["date", "open", "close", "high", "low", "volume", "openinterest"]]
    # quote["datetime"] = ''.join(quote["date"] + ' ' + quote["time"])
    # ret_data = quote[["code", "name", "price", "date", "time", "open", "pre_close", "high", "low", "volume", "amount"]]
    # print(ret_data)

    # data = {
    #     "datetime": ''.join(quote["date"] + ' ' + quote["time"]),
    #     "open": quote['open'],
    #     "close": quote['close'],
    #     "high": quote['high'],
    #     "low": quote['low'],
    #     "price": quote['price'],
    #     "volume": quote['volume'],
    #     "amount": quote['amount'],
    # }
    # print(data)

    return ret_data

# def get_historical_data(code, start="2020-06-01", end="2023-03-18"):
def get_historical_data(code, start="2021-02-05", end="2023-03-18"):
    df = ts.get_k_data(code, autype="qfq", start=start, end=end)
    df.index = pd.to_datetime(df.date)
    df["openinterest"] = 0
    df = df[["date", "open", "high", "low", "close", "volume", "openinterest"]]
    return df


start = datetime(2020, 1, 1)
end = datetime(2023, 3, 14)
code = symbol = '601318' # 中国平安

if __name__ == "__main__":
    WEBHOOK_SECRET = "wNMVU3ewSm2F0G2TwTX4Fd"
    # bot = LarkBot(secret=WEBHOOK_SECRET)
    

    dataframe = get_historical_data(code)
    print("historical data:\n", dataframe)

    # 将策略应用到实盘交易中
    while True:
        # 获取实时行情数据
        os.system(f"afplay {sounds_file}")
        
        df_mew = get_realtime_data(code)
        print("update realtime data:\n", df_mew)
        
        dataframe = pd.concat([dataframe, df_mew])
        # dataframe.append(get_realtime_data(code))

        # 更新至历史数据库

        print("feeds data:\n", dataframe)

        # 将数据源转换为Backtrader数据源格式
        data = bt.feeds.PandasData(dataname=dataframe, fromdate=start, todate=end)
        # data = bt.feeds.PandasData(dataname=pd.DataFrame(dataframe).set_index('date'))

        # 创建Cerebro引擎
        cerebro = bt.Cerebro()
        # 为Cerebro引擎添加策略
        cerebro.addstrategy(BiggerThanEmaStrategy)

        # TODO(Charmve)
        ## 增加组合策略
        # cerebro.addstrategy(svm_strategy)
        # cerebro.addstrategy(MultiStrategy)

        # 将最新的数据添加到引擎中
        cerebro.adddata(data, name=symbol)

        # 设置初始资金
        cerebro.broker.setcash(10000.0)

        # 每笔交易使用固定交易量
        cerebro.addsizer(bt.sizers.FixedSize, stake=10)

        # 设置交易手续费
        cerebro.broker.setcommission(commission=0.001)

        # 添加性能分析器
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')

        # 获取回测开始时的总资金
        print("期初资金: %.2f" % cerebro.broker.getvalue())

        # 运行引擎
        # cerebro.run()
        thestrats = cerebro.run()

        # 获取最后一笔交易信息
        # last_trade = cerebro.broker.getbroker().gethistory()[-1]
        # print('Last trade:', last_trade)

        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        # cerebro.plot(style = "candlestick")  # 绘图

        # 获取回测结束后的总资金
        print("期末资金: %.2f" % cerebro.broker.getvalue())

        # 输出性能指标
        thestrat = thestrats[0]
        print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis()['sharperatio'])
    
        # cerebro.plotinfo.plotname = "收盘价大于简单移动平均价"
        # Plot the result
        # cerebro.plot()

        # 等待一段时间后重新获取数据
        time.sleep(2)