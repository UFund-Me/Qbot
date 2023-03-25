'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-12 18:56:23
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-12 19:36:14
FilePath: /Qbot/qbot/strategies/multi_strategy_bt.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 在这个示例中，我们使用了backtrader的内置数据源GenericCSVData，读取了名为mydata.csv的数据文件。
        在初始化策略时，我们使用了SimpleMovingAverage和RelativeStrengthIndex等指标，用于判断买卖点。
        在每个交易点，我们使用log函数来输出交易信息。在运行引擎后，我们使用ShapreRatio性能分析器来输出交易性能指标。

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers
import pandas as pd
import tushare as ts

from datetime import date, datetime

class MultiStrategy(bt.Strategy):
    params = (
        ('exitbars', 5),
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = btind.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )
        self.rsi = btind.RelativeStrengthIndex()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status == order.Completed:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        if not self.position:
            if (self.rsi[0] < 50 and
                    self.rsi[-1] >= 50 and
                    self.dataclose[0] > self.sma[0]):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if (self.rsi[0] > 50 and
                    self.rsi[-1] <= 50 and
                    self.dataclose[0] < self.sma[0]):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), dt=None)

def get_data(code, start="2020-01-01", end="2023-01-31"):
    df = ts.get_k_data(code, autype="qfq", start=start, end=end)
    df.index = pd.to_datetime(df.date)
    df["openinterest"] = 0
    df = df[["open", "high", "low", "close", "volume", "openinterest"]]
    return df

dataframe = get_data("600018")
start = datetime(2020, 1, 1)
end = datetime(2021, 12, 31)

if __name__ == "__main__":

    # 创建Cerebro引擎
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiStrategy)

    # 设置数据源
    # data = btfeeds.GenericCSVData(
    #     dataname='/Users/charmve/Qbot/pytrader/doc/04.kdj_with_macd/002859.csv',
    #     datetime=0,
    #     high=1,
    #     low=2,
    #     open=3,
    #     close=4,
    #     volume=5,
    #     openinterest=-1,
    # )

    data = bt.feeds.PandasData(dataname=dataframe, fromdate=start, todate=end)
    print(data)

    # 将数据添加到引擎中
    cerebro.adddata(data)

    # 设置初始资金
    cerebro.broker.setcash(10000.0)

    # 设置交易手续费
    cerebro.broker.setcommission(commission=0.001)

    # 添加性能分析器
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

    # 运行引擎
    # cerebro.run()
    thestrats = cerebro.run()

    # 输出性能指标
    thestrat = thestrats[0]
    print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis()['sharperatio'])
   
    # Plot the result
    cerebro.plot()