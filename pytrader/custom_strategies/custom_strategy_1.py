import time
import datetime
from typing import List, Dict

from dateutil import tz
from pandas import DataFrame

from easyquant import DefaultLogHandler
from easyquant import StrategyTemplate
from easyquant.context import Context
from easyquant.event_engine import Event
from easytrader.model import Position


class Strategy(StrategyTemplate):
    name = 'example strategy'

    watch_stocks = ["002230"]

    def init(self):
        for stock_code in self.watch_stocks:
            self.quotation_engine.watch(stock_code)

    def on_bar(self, context: Context, data: Dict[str, DataFrame]):
        self.log.info("on_bar")

    def on_close(self, context: Context):
        self.log.info("on_close")

    def on_open(self, context: Context):
        pass

    def shutdown(self):
        self.log.info("shutdown")
