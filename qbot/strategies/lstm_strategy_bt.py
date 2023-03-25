'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-12 18:58:02
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-12 19:36:27
FilePath: /Qbot/qbot/strategies/lstm_strategy_bt.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 在这个LSTM策略示例中，我们使用了Keras和Backtrader框架来实现LSTM模型，并将其应用于交易决策中。
在策略初始化时，我们使用MinMaxScaler对数据进行归一化处理，并使用train_test_split方法将数据分为训练集和测试集。
我们使用训练集来训练LSTM模型，并使用测试集来进行预测。在每个交易点，我们使用LSTM模型来预测未来的价格走势，
如果预测价格高于当前价格，则进行买入操作。

请注意，这只是一个简单的示例，实际交易需要更多的参数和逻辑处理。在实际交易前，请务必进行充分的测试和评估。

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import pandas as pd
import numpy as np
import tushare as ts

from datetime import date, datetime

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler

class LSTMPredict(bt.Strategy):
    params = (('period', 10), ('neurons', 50), ('train_size', 0.8), ('lookback', 20))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.lookback = self.p.lookback
        self.train_size = self.p.train_size
        self.train_data, self.test_data = self._prepare_data()
        self.model = self._build_model()
        self.model.fit(self.train_data['X'], self.train_data['Y'], epochs=50, batch_size=1, verbose=2)

    def _prepare_data(self):
        data = np.array(self.dataclose)
        data = np.reshape(data, (-1, 1))
        data = self.scaler.fit_transform(data)
        train_size = int(len(data) * self.train_size)
        train_data = data[:train_size]
        test_data = data[train_size:]
        return {'X': self._prepare_X(train_data), 'Y': self._prepare_Y(train_data)}, {'X': self._prepare_X(test_data)}

    def _prepare_X(self, data):
        X, Y = [], []
        for i in range(self.lookback, len(data)):
            X.append(data[i - self.lookback:i, 0])
            Y.append(data[i, 0])
        X, Y = np.array(X), np.array(Y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X

    def _prepare_Y(self, data):
        Y = []
        for i in range(self.lookback, len(data)):
            Y.append(data[i, 0])
        Y = np.array(Y)
        Y = np.reshape(Y, (Y.shape[0], 1))
        return Y

    def _build_model(self):
        model = Sequential()
        model.add(LSTM(units=self.p.neurons, input_shape=(self.lookback, 1)))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def next(self):
        if self.order:
            return
        if not self.position:
            X = self.test_data['X']
            X = np.reshape(X, (X.shape[0], X.shape[1], 1))
            y_pred = self.model.predict(X)
            y_pred = self.scaler.inverse_transform(y_pred)
            if self.dataclose[0] < y_pred[-1]:
                self.buy(size=100)
        else:
            if self.dataclose[0] > self.position.price * 1.05:
                self.sell(size=self.position.size)

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
    cerebro.addstrategy(LSTMPredict)

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


