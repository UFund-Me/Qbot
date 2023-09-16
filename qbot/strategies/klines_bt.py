'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-12 18:44:54
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-05-17 09:35:01
FilePath: /Qbot/qbot/strategies/klines_bt.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
from datetime import datetime
import backtrader
from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import efinance


def get_k_data(stock_code, begin: datetime, end: datetime) -> pd.DataFrame:
    """
    根据efinance工具包获取股票数据
    :param stock_code:股票代码
    :param begin: 开始日期
    :param end: 结束日期
    :return:
    """
    # stock_code = '600519'  # 股票代码，茅台
    k_dataframe: pd.DataFrame = efinance.stock.get_quote_history(
        stock_code, beg=begin.strftime("%Y%m%d"), end=end.strftime("%Y%m%d"))
    k_dataframe = k_dataframe.iloc[:, :9]
    k_dataframe.columns = ['name', 'code', 'date', 'open', 'close', 'high', 'low', 'volume', 'turnover']
    k_dataframe.index = pd.to_datetime(k_dataframe.date)
    k_dataframe.drop(['name', 'code', 'date'], axis=1, inplace=True)
    return k_dataframe


class KlinesStrategy(backtrader.Strategy):  # 策略
    def __init__(self):
        # 初始化交易指令、买卖价格和手续费
        self.close_price = self.datas[0].close  # 这里加一个数据引用，方便后续操作
        self.sma = backtrader.indicators.SimpleMovingAverage(self.datas[0], period=5)  # 借用这个策略，计算5日的均线

    def notify_order(self, order):  # 固定写法，查看订单情况
        # 查看订单情况
        if order.status in [order.Submitted, order.Accepted]:  # 接受订单交易，正常情况
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                logger.debug('已买入, 购入金额 %.2f' % order.executed.price)
            elif order.issell():
                logger.debug('已卖出, 卖出金额 %.2f' % order.executed.price)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.debug('订单取消、保证金不足、金额不足拒绝交易')

    def next(self):  # 固定的函数，框架执行过程中会不断循环next()，过一个K线，执行一次next()
        # 此时调用 self.datas[0]即可查看当天的数据
        # 执行买入条件判断：当天收盘价格突破5日均线
        if self.close_price[0] > self.sma[0]:
            # 执行买入
            logger.debug("buy 500 in {}, 预期购入金额 {}, 剩余可用资金 {}", self.datetime.date(), self.data.close[0],
                         self.broker.getcash())
            self.buy(size=500, price=self.data.close[0])
        # 执行卖出条件已有持仓，且收盘价格跌破5日均线
        if self.position:
            if self.close_price[0] < self.sma[0]:
                # 执行卖出
                logger.debug("sell in {}, 预期卖出金额 {}, 剩余可用资金 {}", self.datetime.date(), self.data.close[0],
                             self.broker.getcash())
                self.sell(size=500, price=self.data.close[0])


if __name__ == '__main__':
    # 获取数据
    start_time = datetime(2015, 1, 1)
    end_time = datetime(2021, 1, 1)
    dataframe = get_k_data('600519', begin=start_time, end=end_time)
    # =============== 为系统注入数据 =================
    # 加载数据
    data = backtrader.feeds.PandasData(dataname=dataframe, fromdate=start_time, todate=end_time)
    # 初始化cerebro回测系统
    cerebral_system = backtrader.Cerebro()  # Cerebro引擎在后台创建了broker(经纪人)实例，系统默认每个broker的初始资金量为10000
    # 将数据传入回测系统
    cerebral_system.adddata(data)  # 导入数据，在策略中使用 self.datas 来获取数据源
    # 将交易策略加载到回测系统中
    cerebral_system.addstrategy(KlinesStrategy)
    # =============== 系统设置 ==================
    # 设置启动资金为 100000
    start_cash = 1000000
    cerebral_system.broker.setcash(start_cash)
    # 设置手续费 万2.5
    cerebral_system.broker.setcommission(commission=0.00025)
    logger.debug('初始资金: {} 回测期间：from {} to {}'.format(start_cash, start_time, end_time))
    # 运行回测系统
    cerebral_system.run()
    # 获取回测结束后的总资金
    portvalue = cerebral_system.broker.getvalue()
    pnl = portvalue - start_cash
    # 打印结果
    logger.debug('净收益: {}', pnl)
    logger.debug("总资金: {}", portvalue)
    cerebral_system.plot(style='candlestick')
    plt.show()
