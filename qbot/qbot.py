'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-23 15:07:38
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-24 02:42:20
FilePath: /Qbot/qbot/qbot.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import tushare as ts
import talib
import pandas as pd
import numpy as np
import time

# 设置股票代码和起止日期
# code = '600000.SH'
code = '601318'
start_date = '20230320'
end_date = time.strftime('%Y%m%d',time.localtime(time.time()))

def get_data(code, start="2023-02-01", end="2023-03-21"):
    df = ts.get_k_data(code, autype="qfq", start=start, end=end)
    df.index = pd.to_datetime(df.date)
    df["openinterest"] = 0
    df = df[["open", "high", "low", "close", "volume", "openinterest"]]
    return df

# 从tushare获取股票数据
# data = ts.get_k_data(code, start=start_date, end=end_date)
# print(data)

data = get_data("600018")

# 计算均线、BIAS和BOLL指标
data['ma5'] = talib.MA(data['close'], timeperiod=5)
data['ma10'] = talib.MA(data['close'], timeperiod=10)
data['ma20'] = talib.MA(data['close'], timeperiod=20)
data['bias1'] = (data['close'] - data['ma5']) / data['ma5'] * 100
data['bias2'] = (data['close'] - data['ma10']) / data['ma10'] * 100
data['bias3'] = (data['close'] - data['ma20']) / data['ma20'] * 100
data['upper'], data['middle'], data['lower'] = talib.BBANDS(data['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
data['k'], data['d'] = talib.STOCH(data['high'], data['low'], data['close'], fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
data['rsi'] = talib.RSI(data['close'], timeperiod=14)

# 初始化买卖信号
signals = np.zeros(len(data))

# 第一个策略：均线和BIAS指标信号
condition1 = (data['ma5'] > data['ma10']) & (data['ma5'] > data['ma20']) & (data['bias1'] > data['bias2']) & (data['bias1'] > data['bias3'])
signals += 0.2 * condition1.astype(int)

# 第二个策略：股价低于BOLL线底
condition2 = (data['close'] < data['lower'])
signals += 0.3 * condition2.astype(int)

# 第三个策略：K线上穿D线
condition3 = (data['k'] > data['d']) & (data['k'].shift() < data['d'].shift())
signals += 0.2 * condition3.astype(int)

# 第四个策略：RSI指标信号
condition4 = (data['rsi'] > 80) | (data['rsi'] < 20)
signals += 0.3 * condition4.astype(int)

# print("signals: ", signals)

# 根据信号生成交易指令，并计算收益率
orders = np.zeros_like(signals)
orders[signals > 0] = 1   # 买入信号
orders[signals < 0] = -1  # 卖出信号
returns = np.diff(data['close']) * orders[:-1]

# 输出结果
print('Total returns:', returns.sum())
print('Positive trades:', len(returns[returns > 0]))
print('Negative trades:', len(returns[returns < 0]))
