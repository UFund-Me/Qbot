'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-12 18:59:15
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-12 19:39:28
FilePath: /Qbot/qbot/strategies/rl_strategy_bt.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 在这个强化学习策略示例中，我们使用了Backtrader框架和RLkit库来实现强化学习模型，并将其应用于交易决策中。
在策略初始化时，我们使用BacktraderEnv来创建环境，将其传入强化学习模型中。
在每个交易点，我们使用强化学习模型来预测动作，并根据环境的反馈进行学习。

请注意，这只是一个简单的示例，实际交易需要更多的参数和逻辑处理。在实际交易前，请务必进行充分的测试和评估。

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import numpy as np
import pandas as pd
import tushare as ts

from datetime import date, datetime
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
from rlkit.envs.backtrader_env import BacktraderEnv
from rlkit.envs.normalized_env import normalize

class RLStrategy(bt.Strategy):
    params = (('period', 10), ('neurons', 50), ('lookback', 20))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.lookback = self.p.lookback
        self.env = normalize(BacktraderEnv(self))
        self.obs = self.env.reset()

    def next(self):
        if self.order:
            return
        if not self.position:
            action = self.model.predict(self.obs.reshape(1, -1))[0]
            self.obs, reward, done, info = self.env.step(action)
            if action > 0:
                self.buy(size=100)
        else:
            if self.dataclose[0] > self.position.price * 1.05:
                self.sell(size=self.position.size)

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
    cerebro.addstrategy(RLStrategy)

    # 设置数据源
    # data = btfeeds.GenericCSVData(
    #     dataname='mydata.csv',
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
