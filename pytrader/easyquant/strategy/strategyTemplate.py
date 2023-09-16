# coding:utf-8
import sys
import traceback
from typing import Dict

from pandas import DataFrame

from ..context import Context
from ..event_engine import Event
from ..easytrader.webtrader import WebTrader


class StrategyTemplate:
    name = 'DefaultStrategyTemplate'

    def __init__(self, user: WebTrader, log_handler, main_engine):
        self.user = user
        self.main_engine = main_engine
        # 优先使用自定义 log 句柄, 否则使用主引擎日志句柄
        self.log = self.log_handler() or log_handler
        self._context: Context = main_engine.context
        self.quotation_engine = main_engine.quotation_engine
        self.init()

    def on_bar(self, context: Context, data: Dict[str, DataFrame]):
        pass

    def init(self):
        # 进行相关的初始化操作
        pass

    def strategy(self, context: Context, event: Event):
        """        :param context:
:param event event.data 为所有股票的信息，结构如下
        {'162411':
        {'ask1': '0.493',
         'ask1_volume': '75500',
         'ask2': '0.494',
         'ask2_volume': '7699281',
         'ask3': '0.495',
         'ask3_volume': '2262666',
         'ask4': '0.496',
         'ask4_volume': '1579300',
         'ask5': '0.497',
         'ask5_volume': '901600',
         'bid1': '0.492',
         'bid1_volume': '10765200',
         'bid2': '0.491',
         'bid2_volume': '9031600',
         'bid3': '0.490',
         'bid3_volume': '16784100',
         'bid4': '0.489',
         'bid4_volume': '10049000',
         'bid5': '0.488',
         'bid5_volume': '3572800',
         'buy': '0.492',
         'close': '0.499',
         'high': '0.494',
         'low': '0.489',
         'name': '华宝油气',
         'now': '0.493',
         'open': '0.490',
         'sell': '0.493',
         'turnover': '420004912',
         'volume': '206390073.351'}}
        """

    def run(self, event):
        try:
            if event.event_type == "bar":
                self.on_bar(self._context, event.data)
            else:
                self.strategy(self._context, event)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.log.error(repr(traceback.format_exception(exc_type,
                                                           exc_value,
                                                           exc_traceback)))

    def clock(self, event):
        """在交易时间会定时推送 clock 事件
        :param event: event.data.clock_event 为 [0.5, 1, 3, 5, 15, 30, 60] 单位为分钟,  ['open', 'close'] 为开市、收市
            event.data.trading_state  bool 是否处于交易时间
        """
        if event.data.clock_event == 'open':
            # 开市了
            self.on_open(self._context)
        elif event.data.clock_event == 'close':
            # 收市了
            self.log.info('close')
            self.on_close(self._context)
        elif event.data.clock_event == 5:
            # 5 分钟的 clock
            self.log.info("5分钟")

    def on_close(self, context: Context):
        pass

    def on_open(self, context: Context):
        pass

    def log_handler(self):
        """
        优先使用在此自定义 log 句柄, 否则返回None, 并使用主引擎日志句柄
        :return: log_handler or None
        """
        return None

    def shutdown(self):
        """
        关闭进程前调用该函数
        :return:
        """
        pass
