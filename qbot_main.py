'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-23 18:19:46
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-24 10:28:16
FilePath: /Qbot/qbot_main.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

from email.policy import default
import os
import sys
import logging
import tushare as ts
import talib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 指定默认字体
plt.rcParams['font.sans-serif']=['Arial Unicode MS']
# mpl.rcParams['font.sans-serif'] = ['KaiTi']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# font = fm.FontProperties(fname='./pytrader/doc/15.rl_learning/font/wqy-microhei.ttc')
font = fm.FontProperties(fname='./font/wqy-microhei.ttc')

# from tensorflow.keras.models import load_model
# from strategies.lstm_strategy_bt import LSTMPredict

from utils.larkbot import LarkBot
import pync

top_path = os.path.dirname(os.path.abspath(sys.argv[0]))
sounds_file = os.path.join(top_path, "./qbot/sounds/bell.wav")

def send_signal_sounds(type="buy"):
    if type == "buy":
        # if linux
        # os.system('play ./qbot/sounds/alert-bells.wav')
        # if MacOs
        os.system(f"afplay {sounds_file}")
    elif type == "sell":
        os.system(f"afplay {sounds_file}")

def send_signal_message_screen(symbol, price, type=default):
    pync.notify(
            f'{symbol}当前价格为{price}',
            title=f'Qbot - {symbol}{type}',
            open="https://ufund-me.github.io/",
            appIcon="./gui/imgs/logo.ico",
        )

# 设置股票代码和均线周期
# symbol = '600000.SH'

# 设置股票代码
# stocks_pool = update_stocks()
stocks_pool = [
    {"code": "sz000063", "name": "中兴通讯", "min_threshold": "26", "max_threshold": "38"},
    {"code": "sh000016", "name": "上证50"},
    {"coce": "601318", "name": "中国平安"},
]
symbol = '600519'
ma_short = 5
ma_mid = 10
ma_long = 20
boll_period = 20
default_weights = [{"KDJ": 0.3, "RSI": 0.15, "BOLL": 0.3, "MA": 0.25, "LSTM": 0.1}]

# # 本金10000，每次交易100股
# broker.setcash(10000)
# broker.addsizer(stake=100)
# # 万五佣金
# broker.setcommission(commission=0.0005)

broker_config = [{"setcash": 100000, "ballance": 100000, "stake": 100, "commission": 0.0005}]

WEBHOOK_SECRET = "wNMVU3ewSm2F0G2TwTX4Fd"
bot = LarkBot(secret=WEBHOOK_SECRET)

# 获取历史行情数据
data = ts.get_hist_data(symbol)
data = data.rename(columns={"pre_close" : "close"})

# 计算LSTM预测价格
# lstm_model = load_model('lstm_model.h5')
# predic_price = lstm_model.predict(np.array([self.data.iloc[i-30:i]['close'].values]))

# 初始化图表
plt.ion()

# 标记买入卖出信号
buy_signal = [{"index": "", "values": ""}]
sell_signal = [{"index": "", "values": ""}]

# 获取回测开始时的总资金
print("期初资金: %.2f" % broker_config[0]["setcash"])

while True:
    # try:
    if broker_config[0]["ballance"] < broker_config[0]["ballance"] * 0.16:
        print("⚠️ 亏损大于 16%，停止交易程序。")
        exit()
    # 获取当前时刻的实时行情数据
    # for ind, stock in enumerate(stocks_pool):
    stock_data = ts.get_realtime_quotes(symbol)
    latest_price = float(stock_data['price'].iloc[0])
    stock_data = stock_data.rename(columns={"pre_close" : "close"})
    stock_data["datetime"] = ''.join(stock_data["date"] + ' ' + stock_data["time"])
    print(
        "===> date_time: ", stock_data['datetime'].iloc[-1], 
        ", code: ", stock_data['code'].iloc[-1], 
        ", latest_price: ", stock_data['price'].iloc[-1])

    # 将字符串类型的数据转换为float类型
    for col in ['open', 'high', 'low', 'price', 'close']:
        stock_data[col] = stock_data[col].astype(float)

    # 将实时行情数据添加到历史行情数据中
    data = pd.concat([data, stock_data])
    # data = data.append(stock_data, ignore_index=True)

    # 计算不同的技术指标
    close_prices = data['close']
    stack_name = data["name"][0]

    ma_short_data = talib.SMA(close_prices, timeperiod=ma_short)
    ma_mid_data = talib.SMA(close_prices, timeperiod=ma_mid)
    ma_long_data = talib.SMA(close_prices, timeperiod=ma_long)
    print("5日、10日和20日均线: " , ma_short_data.iloc[-1], ma_mid_data.iloc[-1], ma_long_data.iloc[-1], close_prices.iloc[0])

    # 背离率
    # bias1 = (close_prices.iloc[-1] - ma_short_data) / ma_short_data * 100
    # bias2 = (close_prices.iloc[-1] - ma_mid_data) / ma_mid_data * 100
    # bias3 = (close_prices.iloc[-1] - ma_long_data) / ma_long_data * 100
    bias1 = (close_prices - ma_short_data) / ma_short_data * 100
    bias2 = (close_prices - ma_mid_data) / ma_mid_data * 100
    bias3 = (close_prices - ma_long_data) / ma_long_data * 100
    print("BIAS指标: ", bias1.iloc[-1], bias2.iloc[-1], bias3.iloc[-1])

    upper, middle, lower = talib.BBANDS(close_prices, timeperiod=boll_period)
    print("BOLL BANDS: ", upper.iloc[-1], middle.iloc[-1], lower.iloc[-1])
    rsi = talib.RSI(close_prices, timeperiod=14)
    print("RSI指标: ", rsi.iloc[-1])
    kdj_k, kdj_d = talib.STOCH(
        data['high'],
        data['low'],
        data['close'],
        fastk_period=9,
        slowk_period=3,
        slowd_period=3
    )
    kdj_j = 3 * kdj_k - 2 * kdj_d
    print("KDJ指标: " , kdj_k.iloc[-1], kdj_d.iloc[-1], kdj_j.iloc[-1])

    # 计算MADC指标
    madc = talib.MACD(data['close'])
    print("MADC指标: ", madc[0][:1])

    # 判断交易信号
    signal = ''
    # if(bias1 > bias2 and bias1 < bias2[-2]) \
    #             and (bias1 > bias3[-1] and bias1[-2] < bias3[-2]):
    if (bias1.iloc[-1] > bias2.iloc[-1] and bias1.iloc[-1] > bias3.iloc[-1]) or (bias1.iloc[-1] == bias2.iloc[-1] and bias1.iloc[-1] == bias3.iloc[-1]):
        signal = 'Buy Signal'
        print(f"💡[{stack_name}] 股票bias1线上穿bias2和bias3：{latest_price}，买入信号")
        bot.send(content=f"💡 买入信号: {data['price'].iloc[-1]} 股票bias1线上穿bias2和bias3：. 当前价格 {latest_price}.")
        send_signal_sounds(type="buy")
        buy_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
    elif (bias1.iloc[-1] < bias2.iloc[-1] and bias1.iloc[-1] < bias3.iloc[-1]):
    # elif close_prices < lower:
        signal = 'Sell Signal'
        bot.send(content=f"💡 ，卖出信号: {data['price'].iloc[-1]} 股票bias1线下穿bias2和bias3：. 当前价格 {latest_price}.")
        print(f"💡[{stack_name}]股票bias1线下穿bias2和bias3：{latest_price}，卖出信号")
        buy_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]

    # 判断均线交叉情况并发出交易信号
    if ma_short_data.iloc[-1] > ma_mid_data.iloc[-1] and ma_short_data.iloc[-1] > ma_long_data.iloc[-1]:
        print(f"💡[{stack_name}]股票价格上穿5日、10日和20日均线：{latest_price}，买入信号")
        send_signal_sounds(type="buy")
        # 发出交易信号，例如发送邮件或短信等
    elif ma_short_data.iloc[-1] < ma_mid_data.iloc[-1] and ma_short_data.iloc[-1] < ma_long_data.iloc[-1]:
        print(f"💡[{stack_name}]股票价格下穿5日、10日和20日均线：{latest_price}，卖出信号")
        send_signal_sounds(type="sell")
        send_signal_message_screen(stack_name, latest_price, type='')
        # 发出交易信号，例如发送邮件或短信等
    
    # 第三个策略：K线上穿D线
    if kdj_k.iloc[-1] > kdj_d.iloc[-1] and kdj_k.iloc[-1] < kdj_d.iloc[-1] and kdj_k.iloc[-1] < 80:
        # signal += 0.2
        print(f"💡[{stack_name}]股票K线上穿D线：{latest_price}，买入信号")
        buy_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
        send_signal_sounds(type="buy")
        # 发出交易信号，例如发送邮件或短信等
    elif kdj_k.iloc[-1] < kdj_d.iloc[-1] and kdj_k.iloc[-1] < kdj_d.iloc[-1]:
        sell_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
        print(f"💡[{stack_name}]股票K线下穿D线：{latest_price}，卖出信号")

    if rsi.iloc[-1] > 80:
        buy_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
        send_signal_sounds(type="buy")
        print(f"💡[{stack_name}]股票趋势指标RSI大于 80：{latest_price}，买入信号")
    elif rsi.iloc[-1] < 20:
        sell_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
        print(f"💡[{stack_name}]股票趋势指标RSI小于 20：{latest_price}，卖出信号")
    
    # 判断价格是否低于BOLL底
    if latest_price < lower.iloc[-1]:
        print(f"💡[{stack_name}]股票价格低于BOLL底：{latest_price} < {lower.iloc[-1]}")
        send_signal_sounds(type="buy")
        buy_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
        # 发出交易信号，例如发送邮件或短信等
    
    # 判断价格是否低于LSTM预测价格
    predic_price = 10
    if latest_price < predic_price:
        print(f"💡[{stack_name}]股票价格低于预测价格：{latest_price} < {predic_price}")
        send_signal_sounds(type="buy")
        buy_signal = [{"index": data['datetime'].iloc[-1], "values": {latest_price}}]
        # 发出交易信号，例如发送邮件或短信等
    
    # 绘制实时数据图
    plt.clf()
    plt.plot(data['close'].iloc[-1], label='Close')
    
    # 画出5日均线、10日均线和20日均线图
    plt.plot(ma_short_data.iloc[-1], label='MA5')
    plt.plot(ma_mid_data.iloc[-1], label='MA10')
    plt.plot(ma_long_data.iloc[-1], label='MA20')

    # 标记买入卖出信号
    # buy_signal = [{"index": "2020-09-22", "values": "23213"}]
    # sell_signal = [{"index": "2020-08-22", "values": "1233"}]
    plt.plot(buy_signal[0]["index"], str(buy_signal[0]["values"]), '^', markersize=8, color='green', label='Buy Signal')
    plt.plot(sell_signal[0]["index"], str(sell_signal[0]["values"]), 'v', markersize=8, color='red', label='Sell Signal')

    plt.plot(bias1.iloc[-1], label='Bias1')
    plt.plot(bias2.iloc[-1], label='Bias2')
    plt.plot(bias3.iloc[-1], label='Bias3')
    plt.plot(upper.iloc[-1], label='Upper')
    plt.plot(middle.iloc[-1], label='Middle')
    plt.plot(lower.iloc[-1], label='Lower')
    plt.plot(rsi.iloc[-1], label='RSI')
    plt.plot(kdj_k.iloc[-1], label='KDJ_K')
    plt.plot(kdj_d.iloc[-1], label='KDJ_D')

    # 添加图例和标题
    # plt.title('2020东京奥运会金牌数分布')
    # plt.title(f'Real-time Stock Price Monitoring [{data["name"][0]} ({symbol})]', fontproperties='YaHei')
    # plt.legend(loc='upper left')
    plt.title('Real-time Stock Price Monitoring')
    plt.legend(loc='best')

    plt.draw()
    plt.pause(10)

    # 计算每日收益
    # broker_config[0]["ballance"] = broker_config[0]["ballance"] + benefits - broker_config[0]s["stake"] * trade_times * broker_config["commission"]
    # print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis()['sharperatio'])
    
    # except Exception as e:
    #     print('Error:', e)