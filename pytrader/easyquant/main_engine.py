import importlib
import os
import pathlib
import signal
import sys
import threading
import time
from collections import OrderedDict
from threading import Lock, Thread

import easytrader
from logbook import Logger, StreamHandler

from .context import Context
from .event_engine import EventEngine
from .log_handler.default_handler import DefaultLogHandler
from .push_engine.clock_engine import ClockEngine
from .push_engine.quotation_engine import QuotationEngine
from .quotation import use_quotation

# TOP_DIR = Path(__file__).parent.parent.parent.joinpath("pytrader")

log = Logger(os.path.basename(__file__))
StreamHandler(sys.stdout).push_application()

PY_MAJOR_VERSION, PY_MINOR_VERSION = sys.version_info[:2]
if (PY_MAJOR_VERSION, PY_MINOR_VERSION) < (3, 5):
    raise Exception(
        "Python 版本需要 3.5 或以上, 当前版本为 %s.%s 请升级 Python"
        % (PY_MAJOR_VERSION, PY_MINOR_VERSION)
    )

ACCOUNT_OBJECT_FILE = "account.session"


class MainEngine:
    """主引擎，负责行情 / 事件驱动引擎 / 交易"""

    def __init__(
        self,
        broker=None,
        need_data=None,
        bar_type="5m",
        quotation="default",
        log_handler=DefaultLogHandler(),
        tzinfo=None,
    ):
        """初始化事件 / 行情 引擎并启动事件引擎"""
        self.log = log_handler
        self.bar_type = bar_type
        self.broker = broker
        self.quotation = use_quotation(quotation)

        # 登录账户
        if (broker is not None) and (need_data is not None):
            self.user = easytrader.use(broker)
            need_data_file = pathlib.Path(need_data)
            if need_data_file.exists():
                self.user.prepare(need_data)
            else:
                log_handler.warn("券商账号信息文件 %s 不存在, easytrader 将不可用" % need_data)
        else:
            self.user = None
            self.log.info("选择了无交易模式")

        self.context = Context(self.user, self.quotation)

        self.event_engine = EventEngine()
        self.clock_engine = ClockEngine(self.event_engine, self.context, tzinfo)

        self.quotation_engine = QuotationEngine(
            self.quotation, self.event_engine, bar_type=bar_type
        )

        # 保存读取的策略类
        self.strategies = OrderedDict()
        self.strategy_list = list()

        # 是否要动态重载策略
        self.is_watch_strategy = False
        # 修改时间缓存
        self._cache = {}
        # # 文件进程映射
        # self._process_map = {}
        # 文件模块映射
        self._modules = {}
        self._names = None
        # 加载锁
        self.lock = Lock()
        # 加载线程
        self._watch_thread = Thread(
            target=self._load_strategy, name="MainEngine.watch_reload_strategy"
        )

        # shutdown 函数
        self.before_shutdown = []  # 关闭引擎前的 shutdown
        self.main_shutdown = []  # 引擎自身要执行的 shutdown
        self.after_shutdown = []  # 关闭引擎后的 shutdown
        self.shutdown_signals = [
            signal.SIGINT,  # 键盘信号
            signal.SIGTERM,  # kill 命令
        ]
        if sys.platform != "win32":
            self.shutdown_signals.extend([signal.SIGHUP, signal.SIGQUIT])

        for s in self.shutdown_signals:
            # 捕获退出信号后的要调用的,唯一的 shutdown 接口
            signal.signal(s, self._shutdown)

        self.log.info("启动主引擎")

    def start(self):
        """启动主引擎"""
        self.event_engine.start()
        self._add_main_shutdown(self.event_engine.stop)

        self.quotation_engine.start()
        self._add_main_shutdown(self.quotation_engine.stop)

        self.clock_engine.start()
        self._add_main_shutdown(self.clock_engine.stop)

    def load(self, names, strategy_file):
        with self.lock:
            mtime = os.path.getmtime(os.path.join("strategies", strategy_file))

            # 是否需要重新加载
            reload = False

            strategy_module_name = os.path.basename(strategy_file)[:-3]
            # new_module = lambda strategy_module_name: importlib.import_module(
            #     "." + strategy_module_name, "strategies"
            # )

            # E731 do not assign a lambda expression, use a def
            def new_module(strategy_module_name):
                return importlib.import_module("." + strategy_module_name, "strategies")

            strategy_module = self._modules.get(
                strategy_file,  # 从缓存中获取 module 实例
                new_module(strategy_module_name),  # 创建新的 module 实例
            )

            if self._cache.get(strategy_file, None) == mtime:
                # 检查最后改动时间
                return
            elif self._cache.get(strategy_file, None) is not None:
                # 注销策略的监听
                old_strategy = self.get_strategy(strategy_module.Strategy.name)
                if old_strategy is None:
                    for s in self.strategy_list:
                        print(s.name)
                self.log.warn(u"卸载策略: %s" % old_strategy.name)
                self.strategy_listen_event(old_strategy, "unlisten")
                time.sleep(2)
                reload = True
            # 重新加载
            if reload:
                strategy_module = importlib.reload(strategy_module)

            self._modules[strategy_file] = strategy_module

            strategy_class = getattr(strategy_module, "Strategy")
            if names is None or strategy_class.name in names:
                self.strategies[strategy_module_name] = strategy_class
                # 缓存加载信息
                new_strategy = strategy_class(
                    user=self.user, log_handler=self.log, main_engine=self
                )
                self.strategy_list.append(new_strategy)
                self._cache[strategy_file] = mtime
                self.strategy_listen_event(new_strategy, "listen")
                self.log.info(u"加载策略: %s" % strategy_module_name)

    def strategy_listen_event(self, strategy, _type="listen"):
        """
        所有策略要监听的事件都绑定到这里
        :param strategy: Strategy()
        :param _type: "listen" OR "unlisten"
        :return:
        """
        func = {
            "listen": self.event_engine.register,
            "unlisten": self.event_engine.unregister,
        }.get(_type)

        # 行情引擎的事件
        func(self.quotation_engine.EventType, strategy.run)

        # 时钟事件
        func(ClockEngine.EventType, strategy.clock)

    def load_strategy(self, names=None):
        """动态加载策略
        :param names: 策略名列表，元素为策略的 name 属性"""
        s_folder = "strategies"
        self._names = names
        strategies = os.listdir(s_folder)
        strategies = filter(
            lambda file: file.endswith(".py") and file != "__init__.py", strategies
        )
        # importlib.import_module(s_folder)
        for strategy_file in strategies:
            self.load(self._names, strategy_file)
        # 如果线程没有启动，就启动策略监视线程
        if self.is_watch_strategy and not self._watch_thread.is_alive():
            self.log.warn("启用了动态加载策略功能")
            self._watch_thread.start()

    def _load_strategy(self):
        while True:
            try:
                self.load_strategy(self._names)
                time.sleep(2)
            except Exception as e:
                print(e)

    def get_strategy(self, name):
        for strategy in self.strategy_list:
            if strategy.name == name:
                return strategy
        return None

    def add_before_shutdown(self, shutdown):

        if not hasattr(shutdown, "__call__"):
            n = shutdown.__name__ if hasattr(shutdown, "__name__") else str(shutdown)
            raise ValueError("%s 不是可调用对象 " % n)

        self.before_shutdown.append(shutdown)

    def add_after_shutdown(self, shutdown):
        if not hasattr(shutdown, "__call__"):
            n = shutdown.__name__ if hasattr(shutdown, "__name__") else str(shutdown)
            raise ValueError("%s 不是可调用对象 " % n)

        self.after_shutdown.append(shutdown)

    def _add_main_shutdown(self, shutdown):
        if not hasattr(shutdown, "__call__"):
            n = shutdown.__name__ if hasattr(shutdown, "__name__") else str(shutdown)
            raise ValueError("%s 不是可调用对象 " % n)

        self.main_shutdown.append(shutdown)

    def _shutdown(self, sig, frame):
        """
        关闭进程前的处理
        :return:
        """
        self.log.debug("开始关闭进程...")
        # 所有 shutdown 前的触发点
        for st in self.before_shutdown:
            st()

        # 引擎自身的 shutdown
        for st in self.main_shutdown:
            st()

        # 等待所有线程关闭, 直到只留下主线程
        c = threading.active_count()
        while threading.active_count() != c:
            time.sleep(2)

        # 调用策略的 shutdown
        self.log.debug("开始关闭策略...")
        for s in self.strategy_list:
            s.shutdown()

        # 所有 shutdown 后的触发点
        for st in self.after_shutdown:
            st()

        # 退出
        time.sleep(0.1)
        sys.exit(1)
