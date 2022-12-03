# coding: utf-8
import datetime
from collections import deque
from threading import Thread

import pandas as pd
import arrow
from dateutil import tz

import time

from ..context import Context
from ..easydealutils import time as etime
from ..event_engine import Event, EventEngine


class Clock:
    def __init__(self, trading_time, clock_event):
        self.trading_state = trading_time
        self.clock_event = clock_event


class ClockIntervalHandler:
    def __init__(self, clock_engine, interval, trading=True, call=None):
        """
        :param interval: float(minute)
        :param trading: 在交易阶段才触发
        :return:
        """
        self.clock_engine = clock_engine
        self.clock_type = interval
        self.interval = interval
        self.second = int(interval * 60)
        self.trading = trading
        self.call = call or (lambda: None)

    def is_active(self):
        if self.trading:
            if not self.clock_engine.trading_state:
                return False
        return int(self.clock_engine.now) % self.second == 0

    def __eq__(self, other):
        if isinstance(other, ClockIntervalHandler):
            return self.interval == other.interval
        else:
            return False

    def __hash__(self):
        return self.second


class DailyHandler:

    def __init__(self, func, time: str):
        """
        :param clock_type:
        :param time: 具体执行时间,一个字符串格式的时间,有两种方式：(1) 24小时内的任意时间，例如"10:00", "01:00"；在tick频率的策略中，可以精确到秒(2)time="every_bar",只能在 run_daily 中调用,运行时间和您设置的频率一致，按天会在交易日的开盘时调用一次，按分钟会在交易时间每分钟运行。
        :param is_trading_date: bool(是否只有在交易日触发)
        :param makeup: 注册时,如果已经过了触发时机,是否立即触发
        :return:
        """
        self.time = time
        self.call = func or (lambda: None)

    def tick(self, context: Context):
        # if etime.is_trade_date(context.current_dt):
        #     # 仅在交易日触发时的判断
        #     return False
        if context.current_dt.strftime("%H:%M") == self.time:
            self.call(context)


class ClockMomentHandler:
    def __init__(self, clock_engine, clock_type, moment=None, is_trading_date=True, makeup=False, call=None):
        """
        :param clock_type:
        :param moment: datetime.time
        :param is_trading_date: bool(是否只有在交易日触发)
        :param makeup: 注册时,如果已经过了触发时机,是否立即触发
        :return:
        """
        self.clock_engine = clock_engine
        self.clock_type = clock_type
        self.moment = moment
        self.is_trading_date = is_trading_date
        self.makeup = makeup
        self.call = call or (lambda: None)
        self.next_time = datetime.datetime.combine(
            self.clock_engine.now_dt.date(),
            self.moment,
        )

        if not self.makeup and self.is_active():
            self.update_next_time()

    def update_next_time(self):
        """
        下次激活时间
        :return:
        """
        if self.is_active():
            if self.is_trading_date:
                next_date = etime.get_next_trade_date(self.clock_engine.now_dt)
            else:
                next_date = self.next_time.date() + datetime.timedelta(days=1)

            self.next_time = datetime.datetime.combine(
                next_date,
                self.moment
            )

    def is_active(self):
        if self.is_trading_date and not etime.is_trade_date(self.clock_engine.now_dt):
            # 仅在交易日触发时的判断
            return False
        return self.next_time <= self.clock_engine.now_dt


class ClockEngine:
    """
    时间推送引擎
    1. 提供统一的 now 时间戳.
    """
    EventType = 'clock_tick'

    def __init__(self, event_engine: EventEngine, context: Context, tzinfo=None, mock=False):
        """
        :param event_engine:
        :param event_engine: tzinfo
        :return:
        """
        # 默认使用当地时间的时区
        self.tzinfo = tzinfo or tz.tzlocal()

        self.event_engine = event_engine
        self.is_active = True
        self.clock_engine_thread = Thread(target=self.clock_tick, name="ClockEngine.clocktick")
        self.sleep_time = 1
        self.trading_state = True if (etime.is_tradetime(datetime.datetime.now()) and etime.is_trade_date(
            datetime.datetime.now())) else False
        self.clock_moment_handlers = deque()
        self.clock_interval_handlers = set()
        self.context = context

        self._init_clock_handler()
        self.daily_handers = set()

    def _init_clock_handler(self):
        """
        注册默认的时钟事件
        :return:
        """

        # 开盘事件
        def _open():
            self.trading_state = True

        self._register_moment('open', datetime.time(9, tzinfo=self.tzinfo), makeup=True, call=_open)

        # 中午休市
        self._register_moment('pause', datetime.time(11, 30, tzinfo=self.tzinfo), makeup=True)

        # 下午开盘
        self._register_moment('continue', datetime.time(13, tzinfo=self.tzinfo), makeup=True)

        # 收盘事件
        def close():
            self.trading_state = False

        self._register_moment('close', datetime.time(15, tzinfo=self.tzinfo), makeup=True, call=close)

        # 间隔事件
        # for interval in (0.5, 1, 5, 15, 30, 60):
        #     self.register_interval(interval)

    @property
    def now(self):
        """
        now 时间戳统一接口
        :return:
        """
        return time.time()

    @property
    def now_dt(self):
        return datetime.datetime.now()

    def start(self):
        self.clock_engine_thread.start()

    def clock_tick(self):
        while self.is_active:
            self.context.change_dt(self.now_dt)
            self.tock()
            time.sleep(self.sleep_time)

    def tock(self):
        # if not etime.is_trade_date(self.now_dt):
        #     return  # 假日暂停时钟引擎
        self._tock()

    def _tock(self):

        for daily_hander in self.daily_handers:
            daily_hander.tick(self.context)

        # 间隔事件
        for handler in self.clock_interval_handlers:
            if handler.is_active():
                handler.call()
                self.push_event_type(handler)
        # 时刻事件
        while self.clock_moment_handlers:
            clock_handler = self.clock_moment_handlers.pop()
            if clock_handler.is_active():
                clock_handler.call()
                self.push_event_type(clock_handler)
                clock_handler.update_next_time()
                self.clock_moment_handlers.appendleft(clock_handler)
            else:
                self.clock_moment_handlers.append(clock_handler)
                break

    def push_event_type(self, clock_handler):
        event = Event(event_type=self.EventType, data=Clock(self.trading_state, clock_handler.clock_type))
        self.event_engine.put(event)

    def stop(self):
        self.is_active = False

    def is_tradetime_now(self):
        """
        :return:
        """
        return etime.is_tradetime(self.now_dt)

    def run_daily(self, func, time: str):
        self.daily_handers.add(DailyHandler(func, time))

    def register_moment(self, clock_type, moment, makeup=False):
        return self._register_moment(clock_type, moment, makeup=makeup)

    def _register_moment(self, clock_type, moment, is_trading_date=True, makeup=False, call=None):
        handlers = list(self.clock_moment_handlers)
        handler = ClockMomentHandler(self, clock_type, moment, is_trading_date, makeup, call)
        handlers.append(handler)

        # 触发事件重新排序
        handlers.sort(key=lambda h: h.next_time, reverse=True)
        self.clock_moment_handlers = deque(handlers)
        return handler

    def register_interval(self, interval_minute, trading=True):
        return self._register_interval(interval_minute, trading)

    def _register_interval(self, interval_minute, trading=True, call=None):
        handler = ClockIntervalHandler(self, interval_minute, trading, call)
        self.clock_interval_handlers.add(handler)
        return handler
