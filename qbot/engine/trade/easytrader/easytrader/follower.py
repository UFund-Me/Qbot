# -*- coding: utf-8 -*-
import abc
import datetime
import os
import pickle
import queue
import re
import threading
import time
from typing import List

import requests

from easytrader import exceptions
from easytrader.log import logger


class BaseFollower(metaclass=abc.ABCMeta):
    """
    slippage: 滑点，取值范围为 [0, 1]
    """

    LOGIN_PAGE = ""
    LOGIN_API = ""
    TRANSACTION_API = ""
    CMD_CACHE_FILE = "cmd_cache.pk"
    WEB_REFERER = ""
    WEB_ORIGIN = ""

    def __init__(self):
        self.trade_queue = queue.Queue()
        self.expired_cmds = set()

        self.s = requests.Session()
        self.s.verify = False

        self.slippage: float = 0.0

    def login(self, user=None, password=None, **kwargs):
        """
        登陆接口
        :param user: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return:
        """
        headers = self._generate_headers()
        self.s.headers.update(headers)

        # init cookie
        self.s.get(self.LOGIN_PAGE)

        # post for login
        params = self.create_login_params(user, password, **kwargs)
        rep = self.s.post(self.LOGIN_API, data=params)

        self.check_login_success(rep)
        logger.info("登录成功")

    def _generate_headers(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/54.0.2840.100 Safari/537.36",
            "Referer": self.WEB_REFERER,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.WEB_ORIGIN,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        return headers

    def check_login_success(self, rep):
        """检查登录状态是否成功
        :param rep: post login 接口返回的 response 对象
        :raise 如果登录失败应该抛出 NotLoginError """
        pass

    def create_login_params(self, user, password, **kwargs) -> dict:
        """生成 post 登录接口的参数
        :param user: 用户名
        :param password: 密码
        :return dict 登录参数的字典
        """
        return {}

    def follow(
        self,
        users,
        strategies,
        track_interval=1,
        trade_cmd_expire_seconds=120,
        cmd_cache=True,
        slippage: float = 0.0,
        **kwargs
    ):
        """跟踪平台对应的模拟交易，支持多用户多策略

        :param users: 支持easytrader的用户对象，支持使用 [] 指定多个用户
        :param strategies: 雪球组合名, 类似 ZH123450
        :param total_assets: 雪球组合对应的总资产， 格式 [ 组合1对应资金, 组合2对应资金 ]
            若 strategies=['ZH000001', 'ZH000002'] 设置 total_assets=[10000, 10000], 则表明每个组合对应的资产为 1w 元，
            假设组合 ZH000001 加仓 价格为 p 股票 A 10%, 则对应的交易指令为 买入 股票 A 价格 P 股数 1w * 10% / p 并按 100 取整
        :param initial_assets:雪球组合对应的初始资产, 格式 [ 组合1对应资金, 组合2对应资金 ]
            总资产由 初始资产 × 组合净值 算得， total_assets 会覆盖此参数
        :param track_interval: 轮询模拟交易时间，单位为秒
        :param trade_cmd_expire_seconds: 交易指令过期时间, 单位为秒
        :param cmd_cache: 是否读取存储历史执行过的指令，防止重启时重复执行已经交易过的指令
        :param slippage: 滑点，0.0 表示无滑点, 0.05 表示滑点为 5%
        """
        self.slippage = slippage

    def _calculate_price_by_slippage(self, action: str, price: float) -> float:
        """
        计算考虑滑点之后的价格
        :param action: 交易动作， 支持 ['buy', 'sell']
        :param price: 原始交易价格
        :return: 考虑滑点后的交易价格
        """
        if action == "buy":
            return price * (1 + self.slippage)
        if action == "sell":
            return price * (1 - self.slippage)
        return price

    def load_expired_cmd_cache(self):
        if os.path.exists(self.CMD_CACHE_FILE):
            with open(self.CMD_CACHE_FILE, "rb") as f:
                self.expired_cmds = pickle.load(f)

    def start_trader_thread(
        self,
        users,
        trade_cmd_expire_seconds,
        entrust_prop="limit",
        send_interval=0,
    ):
        trader = threading.Thread(
            target=self.trade_worker,
            args=[users],
            kwargs={
                "expire_seconds": trade_cmd_expire_seconds,
                "entrust_prop": entrust_prop,
                "send_interval": send_interval,
            },
        )
        trader.setDaemon(True)
        trader.start()

    @staticmethod
    def warp_list(value):
        if not isinstance(value, list):
            value = [value]
        return value

    @staticmethod
    def extract_strategy_id(strategy_url):
        """
        抽取 策略 id，一般用于获取策略相关信息
        :param strategy_url: 策略 url
        :return: str 策略 id
        """
        pass

    def extract_strategy_name(self, strategy_url):
        """
        抽取 策略名，主要用于日志打印，便于识别
        :param strategy_url:
        :return: str 策略名
        """
        pass

    def track_strategy_worker(self, strategy, name, interval=10, **kwargs):
        """跟踪下单worker
        :param strategy: 策略id
        :param name: 策略名字
        :param interval: 轮询策略的时间间隔，单位为秒"""
        while True:
            try:
                transactions = self.query_strategy_transaction(
                    strategy, **kwargs
                )
            # pylint: disable=broad-except
            except Exception as e:
                logger.exception("无法获取策略 %s 调仓信息, 错误: %s, 跳过此次调仓查询", name, e)
                time.sleep(3)
                continue
            for transaction in transactions:
                trade_cmd = {
                    "strategy": strategy,
                    "strategy_name": name,
                    "action": transaction["action"],
                    "stock_code": transaction["stock_code"],
                    "amount": transaction["amount"],
                    "price": transaction["price"],
                    "datetime": transaction["datetime"],
                }
                if self.is_cmd_expired(trade_cmd):
                    continue
                logger.info(
                    "策略 [%s] 发送指令到交易队列, 股票: %s 动作: %s 数量: %s 价格: %s 信号产生时间: %s",
                    name,
                    trade_cmd["stock_code"],
                    trade_cmd["action"],
                    trade_cmd["amount"],
                    trade_cmd["price"],
                    trade_cmd["datetime"],
                )
                self.trade_queue.put(trade_cmd)
                self.add_cmd_to_expired_cmds(trade_cmd)
            try:
                for _ in range(interval):
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("程序退出")
                break

    @staticmethod
    def generate_expired_cmd_key(cmd):
        return "{}_{}_{}_{}_{}_{}".format(
            cmd["strategy_name"],
            cmd["stock_code"],
            cmd["action"],
            cmd["amount"],
            cmd["price"],
            cmd["datetime"],
        )

    def is_cmd_expired(self, cmd):
        key = self.generate_expired_cmd_key(cmd)
        return key in self.expired_cmds

    def add_cmd_to_expired_cmds(self, cmd):
        key = self.generate_expired_cmd_key(cmd)
        self.expired_cmds.add(key)

        with open(self.CMD_CACHE_FILE, "wb") as f:
            pickle.dump(self.expired_cmds, f)

    @staticmethod
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def _execute_trade_cmd(
        self, trade_cmd, users, expire_seconds, entrust_prop, send_interval
    ):
        """分发交易指令到对应的 user 并执行
        :param trade_cmd:
        :param users:
        :param expire_seconds:
        :param entrust_prop:
        :param send_interval:
        :return:
        """
        for user in users:
            # check expire
            now = datetime.datetime.now()
            expire = (now - trade_cmd["datetime"]).total_seconds()
            if expire > expire_seconds:
                logger.warning(
                    "策略 [%s] 指令(股票: %s 动作: %s 数量: %s 价格: %s)超时，指令产生时间: %s 当前时间: %s, 超过设置的最大过期时间 %s 秒, 被丢弃",
                    trade_cmd["strategy_name"],
                    trade_cmd["stock_code"],
                    trade_cmd["action"],
                    trade_cmd["amount"],
                    trade_cmd["price"],
                    trade_cmd["datetime"],
                    now,
                    expire_seconds,
                )
                break

            # check price
            price = trade_cmd["price"]
            if not self._is_number(price) or price <= 0:
                logger.warning(
                    "策略 [%s] 指令(股票: %s 动作: %s 数量: %s 价格: %s)超时，指令产生时间: %s 当前时间: %s, 价格无效 , 被丢弃",
                    trade_cmd["strategy_name"],
                    trade_cmd["stock_code"],
                    trade_cmd["action"],
                    trade_cmd["amount"],
                    trade_cmd["price"],
                    trade_cmd["datetime"],
                    now,
                )
                break

            # check amount
            if trade_cmd["amount"] <= 0:
                logger.warning(
                    "策略 [%s] 指令(股票: %s 动作: %s 数量: %s 价格: %s)超时，指令产生时间: %s 当前时间: %s, 买入股数无效 , 被丢弃",
                    trade_cmd["strategy_name"],
                    trade_cmd["stock_code"],
                    trade_cmd["action"],
                    trade_cmd["amount"],
                    trade_cmd["price"],
                    trade_cmd["datetime"],
                    now,
                )
                break

            actual_price = self._calculate_price_by_slippage(
                trade_cmd["action"], trade_cmd["price"]
            )
            args = {
                "security": trade_cmd["stock_code"],
                "price": actual_price,
                "amount": trade_cmd["amount"],
                "entrust_prop": entrust_prop,
            }
            try:
                response = getattr(user, trade_cmd["action"])(**args)
            except exceptions.TradeError as e:
                trader_name = type(user).__name__
                err_msg = "{}: {}".format(type(e).__name__, e.args)
                logger.error(
                    "%s 执行 策略 [%s] 指令(股票: %s 动作: %s 数量: %s 价格(考虑滑点): %s 指令产生时间: %s) 失败, 错误信息: %s",
                    trader_name,
                    trade_cmd["strategy_name"],
                    trade_cmd["stock_code"],
                    trade_cmd["action"],
                    trade_cmd["amount"],
                    actual_price,
                    trade_cmd["datetime"],
                    err_msg,
                )
            else:
                logger.info(
                    "策略 [%s] 指令(股票: %s 动作: %s 数量: %s 价格(考虑滑点): %s 指令产生时间: %s) 执行成功, 返回: %s",
                    trade_cmd["strategy_name"],
                    trade_cmd["stock_code"],
                    trade_cmd["action"],
                    trade_cmd["amount"],
                    actual_price,
                    trade_cmd["datetime"],
                    response,
                )

    def trade_worker(
        self, users, expire_seconds=120, entrust_prop="limit", send_interval=0
    ):
        """
        :param send_interval: 交易发送间隔， 默认为0s。调大可防止卖出买入时买出单没有及时成交导致的买入金额不足
        """
        while True:
            trade_cmd = self.trade_queue.get()
            self._execute_trade_cmd(
                trade_cmd, users, expire_seconds, entrust_prop, send_interval
            )
            time.sleep(send_interval)

    def query_strategy_transaction(self, strategy, **kwargs):
        params = self.create_query_transaction_params(strategy)

        rep = self.s.get(self.TRANSACTION_API, params=params)
        history = rep.json()

        transactions = self.extract_transactions(history)
        self.project_transactions(transactions, **kwargs)
        return self.order_transactions_sell_first(transactions)

    def extract_transactions(self, history) -> List[str]:
        """
        抽取接口返回中的调仓记录列表
        :param history: 调仓接口返回信息的字典对象
        :return: [] 调参历史记录的列表
        """
        return []

    def create_query_transaction_params(self, strategy) -> dict:
        """
        生成用于查询调参记录的参数
        :param strategy: 策略 id
        :return: dict 调参记录参数
        """
        return {}

    @staticmethod
    def re_find(pattern, string, dtype=str):
        return dtype(re.search(pattern, string).group())

    @staticmethod
    def re_search(pattern, string, dtype=str):
        return dtype(re.search(pattern,string).group(1))

    def project_transactions(self, transactions, **kwargs):
        """
        修证调仓记录为内部使用的统一格式
        :param transactions: [] 调仓记录的列表
        :return: [] 修整后的调仓记录
        """
        pass

    def order_transactions_sell_first(self, transactions):
        # 调整调仓记录的顺序为先卖再买
        sell_first_transactions = []
        for transaction in transactions:
            if transaction["action"] == "sell":
                sell_first_transactions.insert(0, transaction)
            else:
                sell_first_transactions.append(transaction)
        return sell_first_transactions
