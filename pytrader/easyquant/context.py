# coding: utf-8
import datetime
from typing import List

from easyquant.quotation import Quotation
from easytrader.webtrader import WebTrader
from easytrader.model import *

from talib._ta_lib import *
import talib


class Context:
    """
    上下文
    """

    def __init__(self, user: WebTrader, quotation: Quotation, current_dt=datetime.datetime.now(), trade_mode=True):
        self.change_dt(current_dt)
        self.user = user
        self.quotation = quotation
        self.trade_days = self.quotation.get_all_trade_days()
        self.is_trade_mode = trade_mode

    def is_trade_date(self, date: str):
        return date in self.trade_days

    def change_dt(self, current_dt:datetime.datetime):
        self.current_dt = current_dt
        self.previous_date = self.current_dt - datetime.timedelta(days=1)

    def fetch_bars(self,  stock_code: str, max_num=120, unit='1d',
                   fields=['date', 'open', 'high', 'low', 'close'],
                   end_dt=None):
        """
        获取K线
        :param stock_code:
        :param max_num:
        :param unit:  bar的时间单位, 支持如下周期：'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w', '1M'。'1w' 表示一周，‘1M' 表示一月
        :param fields:
        :param end_dt:
        :return:
        """
        return self.quotation.get_bars(stock_code, max_num,
                                       unit=unit,fields=fields,
                                       end_dt=end_dt if end_dt else self.current_dt)

    def fetch_minute_bars(self, stock_code: str, minute=5, max_num=80):
        """
        获取分钟K线
        :param stock_code:
        :param minute:
        :param max_num:
        :return:
        """
        return self.quotation.get_bars(stock_code, max_num,
                                       unit=str(minute) + "m",
                                       end_dt=self.current_dt)

    def calculate_minute_cci(self, stock_code: str, minute=5, max_num=80, time_period=14):
        """
        分钟级cci
        :param stock_code:
        :param minute:
        :param max_num:
        :param time_period:
        :return:
        """
        df = self.fetch_minute_bars(stock_code, max_num=max_num, minute=minute)
        return self.calculate_cci(df, time_period=time_period)

    def calculate_cci(self, df, time_period=14):
        return CCI(df.high, df.low, df.close, timeperiod=time_period)

    # def fetch_minute_bar_df(self, stock_code: str, minute=5, max_num=80):
    #     """
    #     获取分钟级K线的pandas dataframe 数据
    #     :param max_num:
    #     :param minute:
    #     :param stock_code:
    #     :return:
    #     """
    #     data = self.fetch_minute_bars(stock_code, minute=minute, max_num=max_num)
    #     df = DataFrame(data[stock_code],
    #                    columns=['date', 'open', 'close', 'high', 'low', 'volume', 'unknown', 'percents'])
    #     df['close'] = df['close'].astype('float')
    #     df['open'] = df['open'].astype('float')
    #     df['high'] = df['high'].astype('float')
    #     df['low'] = df['low'].astype('float')
    #     df['volume'] = df['volume'].astype('float')
    #     return df

    def calculate_minute_rsi(self, stock_code: str, minute=5, max_num=80, time_period=6):
        """
        计算RSI
        :param stock_code:
        :param minute:
        :param max_num:
        :param time_period:
        :return:
        """
        df = self.fetch_minute_bars(stock_code, minute=minute, max_num=max_num)
        return self.calculate_rsi(df, time_period=time_period)

    def calculate_rsi(self, df, time_period=6):
        return RSI(df.close, timeperiod=time_period)

    @property
    def balance(self) -> List[Balance]:
        return self.user.get_balance()

    @property
    def position(self) -> List[Position]:
        return self.user.get_position()

    @property
    def entrust(self) -> List[Entrust]:
        """获取当日委托列表"""
        return self.user.get_entrust()

    @property
    def current_deal(self) -> List[Deal]:
        """获取当日成交列表"""
        return self.user.get_current_deal()

    def buy(self, security, price=0, amount=0, volume=0, entrust_prop=0):
        """买入卖出股票
        :param security: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop:
        """
        return self.user.buy(security, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def sell(self, security, price=0, amount=0, volume=0, entrust_prop=0):
        """卖出股票
        :param security: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop:
        """
        return self.user.sell(security, price=price, amount=amount, volume=volume, entrust_prop=entrust_prop)

    def __getattr__(self, func_name):
        def talib_func(*args, **kwargs):
            func = getattr(talib, func_name)
            return func(*args, **kwargs)

        return talib_func
