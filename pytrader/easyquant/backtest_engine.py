import os
import os
import signal
import sys
from datetime import datetime, timedelta
from threading import Lock

from logbook import Logger, StreamHandler

from easytrader.mock_trader import MockTrader
from .context import Context
from .event_engine import EventEngine
from .log_handler.default_handler import MockLogHandler
from .push_engine.quotation_engine import QuotationEngine
from .quotation import use_quotation
from .strategy.strategyTemplate import StrategyTemplate

StreamHandler(sys.stdout).push_application()

PY_MAJOR_VERSION, PY_MINOR_VERSION = sys.version_info[:2]
if (PY_MAJOR_VERSION, PY_MINOR_VERSION) < (3, 5):
    raise Exception('Python 版本需要 3.5 或以上, 当前版本为 %s.%s 请升级 Python' % (PY_MAJOR_VERSION, PY_MINOR_VERSION))


class PositionLog(object):
    amount = "0股"
    avgCost = ""
    dailyGains = ""
    date = "2021-12-08"
    gain = ""
    gainPercentStr = ""
    holdCost = ""
    margin = ""
    price = ""
    security = ""
    todayAmount = ""
    totalValue = 0
    value = 17.52


class BackTestEngine:
    """回测引擎"""

    def __init__(self,
                 strategy_class,
                 start_date: str,
                 end_date: str,
                 bar_type="5m",
                 quotation='jqdata'):
        """初始化事件 / 行情 引擎并启动事件引擎
        """
        self.broker = 'mock'
        self.bar_type = bar_type
        self.quotation = use_quotation(quotation)
        self.user = MockTrader()
        self.context = Context(self.user, self.quotation)
        self.log = MockLogHandler(context=self.context)

        self.event_engine = EventEngine()
        self.start_date = start_date
        self.end_date = end_date

        self.quotation_engine = QuotationEngine(self.quotation, self.event_engine, bar_type=bar_type)
        self.strategy: StrategyTemplate = strategy_class(self.user, self.log, self)

        # 加载锁
        self.lock = Lock()

        # shutdown 函数
        self.shutdown_signals = [
            signal.SIGINT,  # 键盘信号
            signal.SIGTERM,  # kill 命令
        ]
        if sys.platform != 'win32':
            self.shutdown_signals.extend([signal.SIGHUP, signal.SIGQUIT])

        for s in self.shutdown_signals:
            # 捕获退出信号后的要调用的,唯一的 shutdown 接口
            signal.signal(s, self.shutdown)

        self.records = []
        self.log.info('启动回测引擎')

    def start(self):
        """ 启动回测 """
        self.user.set_quotation(self.quotation)
        start_date_time = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date_time = datetime.strptime(self.end_date, '%Y-%m-%d')

        current_dt = start_date_time

        while current_dt <= end_date_time:
            # 交易日
            if not self.context.is_trade_date(current_dt.strftime("%Y-%m-%d")):
                current_dt = current_dt + timedelta(days=1)
                continue

            # TODO 待优化
            self.context.user.set_time(current_dt)
            # open
            self.context.change_dt(current_dt + timedelta(hours=9, minutes=30))
            self.strategy.on_open(self.context)

            self.mock_quotation(current_dt, self.strategy)

            self.context.change_dt(current_dt + timedelta(hours=15, minutes=30))
            self.strategy.on_close(self.context)

            current_dt = current_dt + timedelta(days=1)
            # 记录交易

            self.user.get_balance()

    def mock_quotation(self, end_date: datetime, strategy: StrategyTemplate):

        current_time = end_date + timedelta(hours=9, minutes=30)
        end_date = end_date + timedelta(hours=15)

        if "m" in self.bar_type:
            minute = int(self.bar_type.replace("m", ""))
            # 9点半开始
            while current_time <= end_date:
                self.context.change_dt(current_time)
                # 更新
                strategy.on_bar(self.context, self.quotation_engine.fetch_quotation(end_date=current_time))
                current_time += timedelta(minutes=minute)
        else:
            # day = int
            self.context.change_dt(end_date)
            quotation_data = self.quotation_engine.fetch_quotation(end_date=end_date)
            self.user.update_balance(quotation_data)
            # 更新持仓
            strategy.on_bar(self.context, quotation_data)

    def shutdown(self, sig, frame):
        """
        关闭进程前的处理
        :return:
        """
        self.log.debug("开始关闭进程...")
