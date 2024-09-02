# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import json
import re
from datetime import datetime
from numbers import Number
from threading import Thread

from easytrader.follower import BaseFollower
from easytrader.log import logger
from easytrader.utils.misc import parse_cookies_str


class XueQiuFollower(BaseFollower):
    LOGIN_PAGE = "https://www.xueqiu.com"
    LOGIN_API = "https://xueqiu.com/snowman/login"
    TRANSACTION_API = "https://xueqiu.com/cubes/rebalancing/history.json"
    PORTFOLIO_URL = "https://xueqiu.com/p/"
    WEB_REFERER = "https://www.xueqiu.com"

    def __init__(self):
        super().__init__()
        self._adjust_sell = None
        self._users = None

    def login(self, user=None, password=None, **kwargs):
        """
        雪球登陆， 需要设置 cookies
        :param cookies: 雪球登陆需要设置 cookies， 具体见
            https://smalltool.github.io/2016/08/02/cookie/
        :return:
        """
        cookies = kwargs.get("cookies")
        if cookies is None:
            raise TypeError(
                "雪球登陆需要设置 cookies， 具体见"
                "https://smalltool.github.io/2016/08/02/cookie/"
            )
        headers = self._generate_headers()
        self.s.headers.update(headers)

        self.s.get(self.LOGIN_PAGE)

        cookie_dict = parse_cookies_str(cookies)
        self.s.cookies.update(cookie_dict)

        logger.info("登录成功")

    def follow(  # type: ignore
        self,
        users,
        strategies,
        total_assets=10000,
        initial_assets=None,
        adjust_sell=False,
        track_interval=10,
        trade_cmd_expire_seconds=120,
        cmd_cache=True,
        slippage: float = 0.0,
    ):
        """跟踪 joinquant 对应的模拟交易，支持多用户多策略
        :param users: 支持 easytrader 的用户对象，支持使用 [] 指定多个用户
        :param strategies: 雪球组合名, 类似 ZH123450
        :param total_assets: 雪球组合对应的总资产， 格式 [组合1对应资金, 组合2对应资金]
            若 strategies=['ZH000001', 'ZH000002'],
                设置 total_assets=[10000, 10000], 则表明每个组合对应的资产为 1w 元
            假设组合 ZH000001 加仓 价格为 p 股票 A 10%,
                则对应的交易指令为 买入 股票 A 价格 P 股数 1w * 10% / p 并按 100 取整
        :param adjust_sell: 是否根据用户的实际持仓数调整卖出股票数量，
            当卖出股票数大于实际持仓数时，调整为实际持仓数。目前仅在银河客户端测试通过。
            当 users 为多个时，根据第一个 user 的持仓数决定
        :type adjust_sell: bool
        :param initial_assets: 雪球组合对应的初始资产,
            格式 [ 组合1对应资金, 组合2对应资金 ]
            总资产由 初始资产 × 组合净值 算得， total_assets 会覆盖此参数
        :param track_interval: 轮训模拟交易时间，单位为秒
        :param trade_cmd_expire_seconds: 交易指令过期时间, 单位为秒
        :param cmd_cache: 是否读取存储历史执行过的指令，防止重启时重复执行已经交易过的指令
        :param slippage: 滑点，0.0 表示无滑点, 0.05 表示滑点为 5%
        """
        super().follow(
            users=users,
            strategies=strategies,
            track_interval=track_interval,
            trade_cmd_expire_seconds=trade_cmd_expire_seconds,
            cmd_cache=cmd_cache,
            slippage=slippage,
        )

        self._adjust_sell = adjust_sell

        self._users = self.warp_list(users)

        strategies = self.warp_list(strategies)
        total_assets = self.warp_list(total_assets)
        initial_assets = self.warp_list(initial_assets)

        if cmd_cache:
            self.load_expired_cmd_cache()

        self.start_trader_thread(self._users, trade_cmd_expire_seconds)

        for strategy_url, strategy_total_assets, strategy_initial_assets in zip(
            strategies, total_assets, initial_assets
        ):
            assets = self.calculate_assets(
                strategy_url, strategy_total_assets, strategy_initial_assets
            )
            try:
                strategy_id = self.extract_strategy_id(strategy_url)
                strategy_name = self.extract_strategy_name(strategy_url)
            except Exception:
                logger.error(
                    "抽取交易id和策略名失败, 无效模拟交易url: %s", strategy_url
                )
                raise
            strategy_worker = Thread(
                target=self.track_strategy_worker,
                args=[strategy_id, strategy_name],
                kwargs={"interval": track_interval, "assets": assets},
            )
            strategy_worker.start()
            logger.info("开始跟踪策略: %s", strategy_name)

    def calculate_assets(self, strategy_url, total_assets=None, initial_assets=None):
        # 都设置时优先选择 total_assets
        if total_assets is None and initial_assets is not None:
            net_value = self._get_portfolio_net_value(strategy_url)
            total_assets = initial_assets * net_value
        if not isinstance(total_assets, Number):
            raise TypeError("input assets type must be number(int, float)")
        if total_assets < 1e3:
            raise ValueError(
                "雪球总资产不能小于1000元，当前预设值 {}".format(total_assets)
            )
        return total_assets

    @staticmethod
    def extract_strategy_id(strategy_url):
        return strategy_url

    def extract_strategy_name(self, strategy_url):
        base_url = "https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol={}"
        url = base_url.format(strategy_url)
        rep = self.s.get(url)
        info_index = 0
        return rep.json()[info_index]["name"]

    def extract_transactions(self, history):
        if history["count"] <= 0:
            return []
        rebalancing_index = 0
        raw_transactions = history["list"][rebalancing_index]["rebalancing_histories"]
        transactions = []
        for transaction in raw_transactions:
            if transaction["price"] is None:
                logger.info(
                    "该笔交易无法获取价格，疑似未成交，跳过。交易详情: %s", transaction
                )
                continue
            transactions.append(transaction)

        return transactions

    def create_query_transaction_params(self, strategy):
        params = {"cube_symbol": strategy, "page": 1, "count": 1}
        return params

    # noinspection PyMethodOverriding
    def none_to_zero(self, data):
        if data is None:
            return 0
        return data

    # noinspection PyMethodOverriding
    def project_transactions(self, transactions, assets):
        for transaction in transactions:
            weight_diff = self.none_to_zero(transaction["weight"]) - self.none_to_zero(
                transaction["prev_weight"]
            )

            initial_amount = abs(weight_diff) / 100 * assets / transaction["price"]

            transaction["datetime"] = datetime.fromtimestamp(
                transaction["created_at"] // 1000
            )

            transaction["stock_code"] = transaction["stock_symbol"].lower()

            transaction["action"] = "buy" if weight_diff > 0 else "sell"

            transaction["amount"] = int(round(initial_amount, -2))
            if transaction["action"] == "sell" and self._adjust_sell:
                transaction["amount"] = self._adjust_sell_amount(
                    transaction["stock_code"], transaction["amount"]
                )

    def _adjust_sell_amount(self, stock_code, amount):
        """
        根据实际持仓值计算雪球卖出股数
          因为雪球的交易指令是基于持仓百分比，在取近似值的情况下可能出现不精确的问题。
        导致如下情况的产生，计算出的指令为买入 1049 股，取近似值买入 1000 股。
        而卖出的指令计算出为卖出 1051 股，取近似值卖出 1100 股，超过 1000 股的买入量，
        导致卖出失败
        :param stock_code: 证券代码
        :type stock_code: str
        :param amount: 卖出股份数
        :type amount: int
        :return: 考虑实际持仓之后的卖出股份数
        :rtype: int
        """
        stock_code = stock_code[-6:]
        user = self._users[0]
        position = user.position
        try:
            stock = next(s for s in position if s["证券代码"] == stock_code)
        except StopIteration:
            logger.info(
                "根据持仓调整 %s 卖出额，发现未持有股票 %s, 不做任何调整",
                stock_code,
                stock_code,
            )
            return amount

        available_amount = stock["可用余额"]
        if available_amount >= amount:
            return amount

        adjust_amount = available_amount // 100 * 100
        logger.info(
            "股票 %s 实际可用余额 %s, 指令卖出股数为 %s, 调整为 %s",
            stock_code,
            available_amount,
            amount,
            adjust_amount,
        )
        return adjust_amount

    def _get_portfolio_info(self, portfolio_code):
        """
        获取组合信息
        """
        url = self.PORTFOLIO_URL + portfolio_code
        portfolio_page = self.s.get(url)
        match_info = re.search(r"(?<=SNB.cubeInfo = ).*(?=;\n)", portfolio_page.text)
        if match_info is None:
            raise Exception("cant get portfolio info, portfolio url : {}".format(url))
        try:
            portfolio_info = json.loads(match_info.group())
        except Exception as e:
            raise Exception("get portfolio info error: {}".format(e))
        return portfolio_info

    def _get_portfolio_net_value(self, portfolio_code):
        """
        获取组合信息
        """
        portfolio_info = self._get_portfolio_info(portfolio_code)
        return portfolio_info["net_value"]
