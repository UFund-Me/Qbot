'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-12 18:57:23
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-12 19:37:14
FilePath: /Qbot/qbot/strategies/sma_cross_strategy_bt.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

在这个例子中，我们使用了Backtrader框架和Alpaca API来实现自动化交易。我们首先定义了策略`SmaCross`，该策略基于两个简单移动平均线的交叉来进行买卖点的判断。在`next`方法中，我们检查当前是否持有头寸，如果没有，我们计算可用资金并计算购买股票的数量，然后买入该股票。如果当前持有头寸，则判断是否需要卖出。

在数据源方面，我们使用了Alpaca API作为数据源，并设置了证券交易所、证券代码、时间间隔、历史数据范围等参数。在引擎方面，我们使用Cerebro引擎，并将数据源和策略添加到引擎中。我们还设置了初始资金、交易费用等参数，并添加了性能分析器来输出交易性能指标。

请注意，这只是一个简单的示例，实际交易需要更多的参数和逻辑处理。在实际交易前，请务必进行充分的测试和评估。

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import pandas as pd
import tushare as ts

from datetime import date, datetime

# import alpaca_backtrader_api

class SmaCross(bt.Strategy):
    params = (('pfast', 10), ('pslow', 30),)

    def __init__(self):
        sma1 = btind.SMA(period=self.p.pfast)
        sma2 = btind.SMA(period=self.p.pslow)
        self.crossover = btind.CrossOver(sma1, sma2)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.broker.cash * 0.95)
                self.size = int(amount_to_invest / self.data.close)
                self.buy(size=self.size)
        elif self.position.size > 0:
            if self.crossover < 0:
                self.close()

# # 设置证券交易所
# alpaca_endpoint = '<https://paper-api.alpaca.markets>'
# alpaca_key_id = 'my_alpaca_key_id'
# alpaca_secret_key = 'my_alpaca_secret_key'
# data_format = btfeeds.TimeFrame.Days

# # 设置数据源
# data = alpaca_backtrader_api.AlpacaData(
#     dataname='AAPL',
#     timeframe=data_format,
#     fromdate=datetime.datetime(2021, 1, 1),
#     todate=datetime.datetime(2021, 9, 30),
#     historical=True,
#     apikey=alpaca_key_id,
#     secretkey=alpaca_secret_key,
#     endpoint=alpaca_endpoint,
#     compression=1
# )

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
    cerebro.addstrategy(SmaCross)

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

