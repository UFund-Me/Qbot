# coding: utf-8
import datetime
import time
from threading import Thread

from ..event_engine import EventEngine, Event
from ..quotation import Quotation


class QuotationEngine:
    EventType = 'bar'
    PushInterval = 3600

    def __init__(self, quotation: Quotation, event_engine: EventEngine, bar_type='5m'):
        """

        :param quotation:
        :param event_engine:
        :param bar_type: K线类型
        """
        self.event_engine = event_engine
        self.quotation_source = quotation
        self.is_active = True

        self.quotation_thread = Thread(target=self.push_quotation, name="QuotationEngine.%s" % self.EventType)
        self.quotation_thread.setDaemon(False)

        self.bar_type = bar_type
        if "m" in bar_type:
            minute = int(bar_type.replace("m", ""))
            self.PushInterval = minute * 60

        self.init()

    def start(self):
        self.quotation_thread.start()

    def stop(self):
        self.is_active = False

    def push_quotation(self):
        while self.is_active:
            try:
                response_data = self.fetch_quotation()
            except:
                self.wait()
                continue
            event = Event(event_type=self.EventType, data=response_data)
            self.event_engine.put(event)
            self.wait()

    def init(self):
        # do something init
        pass

    def wait(self):
        # for receive quit signal
        for _ in range(int(self.PushInterval) + 1):
            time.sleep(1)

    stocks = []

    def watch(self, stock_code: str):
        self.stocks.append(stock_code)

    def un_watch(self, stock_code: str):
        self.stocks.remove(stock_code)

    def fetch_quotation(self, end_date=None):
        bars = {}
        for code in self.stocks:
            bars[code] = self.quotation_source.get_bars(code, 200, unit=self.bar_type,
                                                        end_dt=end_date if end_date else datetime.datetime.now())

        return bars
