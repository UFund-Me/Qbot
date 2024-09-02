# coding:utf-8
import datetime
import os
import time
import unittest
from unittest import mock

from easytrader.xq_follower import XueQiuFollower


class TestXueQiuTrader(unittest.TestCase):
    def test_adjust_sell_amount_without_enable(self):
        follower = XueQiuFollower()

        mock_user = mock.MagicMock()
        follower._users = [mock_user]

        follower._adjust_sell = False
        amount = follower._adjust_sell_amount("169101", 1000)
        self.assertEqual(amount, amount)

    def test_adjust_sell_should_only_work_when_sell(self):
        follower = XueQiuFollower()
        follower._adjust_sell = True
        test_transaction = {
            "weight": 10,
            "prev_weight": 0,
            "price": 10,
            "stock_symbol": "162411",
            "created_at": int(time.time() * 1000),
        }
        test_assets = 1000

        mock_adjust_sell_amount = mock.MagicMock()
        follower._adjust_sell_amount = mock_adjust_sell_amount

        follower.project_transactions(
            transactions=[test_transaction], assets=test_assets
        )
        mock_adjust_sell_amount.assert_not_called()

        mock_adjust_sell_amount.reset_mock()
        test_transaction["prev_weight"] = test_transaction["weight"] + 1
        follower.project_transactions(
            transactions=[test_transaction], assets=test_assets
        )
        mock_adjust_sell_amount.assert_called()

    def test_adjust_sell_amount(self):
        follower = XueQiuFollower()

        mock_user = mock.MagicMock()
        follower._users = [mock_user]
        mock_user.position = TEST_POSITION

        follower._adjust_sell = True
        test_cases = [
            ("169101", 600, 600),
            ("169101", 700, 600),
            ("000000", 100, 100),
            ("sh169101", 700, 600),
        ]
        for stock_code, sell_amount, excepted_amount in test_cases:
            amount = follower._adjust_sell_amount(stock_code, sell_amount)
            self.assertEqual(amount, excepted_amount)

    def test_slippage_with_default(self):
        follower = XueQiuFollower()
        mock_user = mock.MagicMock()

        # test default no slippage
        test_price = 1.0
        test_trade_cmd = {
            "strategy": "test_strategy",
            "strategy_name": "test_strategy",
            "action": "buy",
            "stock_code": "162411",
            "amount": 100,
            "price": 1.0,
            "datetime": datetime.datetime.now(),
        }
        follower._execute_trade_cmd(
            trade_cmd=test_trade_cmd,
            users=[mock_user],
            expire_seconds=10,
            entrust_prop="limit",
            send_interval=10,
        )
        _, kwargs = getattr(mock_user, test_trade_cmd["action"]).call_args
        self.assertAlmostEqual(kwargs["price"], test_price)

    def test_slippage(self):
        follower = XueQiuFollower()
        mock_user = mock.MagicMock()

        test_price = 1.0
        follower.slippage = 0.05

        # test buy
        test_trade_cmd = {
            "strategy": "test_strategy",
            "strategy_name": "test_strategy",
            "action": "buy",
            "stock_code": "162411",
            "amount": 100,
            "price": 1.0,
            "datetime": datetime.datetime.now(),
        }
        follower._execute_trade_cmd(
            trade_cmd=test_trade_cmd,
            users=[mock_user],
            expire_seconds=10,
            entrust_prop="limit",
            send_interval=10,
        )
        excepted_price = test_price * (1 + follower.slippage)
        _, kwargs = getattr(mock_user, test_trade_cmd["action"]).call_args
        self.assertAlmostEqual(kwargs["price"], excepted_price)

        # test sell
        test_trade_cmd["action"] = "sell"
        follower._execute_trade_cmd(
            trade_cmd=test_trade_cmd,
            users=[mock_user],
            expire_seconds=10,
            entrust_prop="limit",
            send_interval=10,
        )
        excepted_price = test_price * (1 - follower.slippage)
        _, kwargs = getattr(mock_user, test_trade_cmd["action"]).call_args
        self.assertAlmostEqual(kwargs["price"], excepted_price)


class TestXqFollower(unittest.TestCase):
    def setUp(self):
        self.follower = XueQiuFollower()
        cookies = os.getenv("EZ_TEST_XQ_COOKIES")
        if not cookies:
            return
        self.follower.login(cookies=cookies)

    def test_extract_transactions(self):
        result = self.follower.extract_transactions(TEST_XQ_PORTOFOLIO_HISTORY)
        self.assertTrue(len(result) == 1)


TEST_POSITION = [
    {
        "Unnamed: 14": "",
        "买入冻结": 0,
        "交易市场": "深Ａ",
        "卖出冻结": 0,
        "参考市价": 1.464,
        "参考市值": 919.39,
        "参考成本价": 1.534,
        "参考盈亏": -43.77,
        "可用余额": 628,
        "当前持仓": 628,
        "盈亏比例(%)": -4.544,
        "股东代码": "0000000000",
        "股份余额": 628,
        "证券代码": "169101",
    }
]

TEST_XQ_PORTOFOLIO_HISTORY = {
    "count": 1,
    "page": 1,
    "totalCount": 17,
    "list": [
        {
            "id": 1,
            "status": "pending",
            "cube_id": 1,
            "prev_bebalancing_id": 1,
            "category": "user_rebalancing",
            "exe_strategy": "intraday_all",
            "created_at": 1,
            "updated_at": 1,
            "cash_value": 0.1,
            "cash": 100.0,
            "error_code": "1",
            "error_message": None,
            "error_status": None,
            "holdings": None,
            "rebalancing_histories": [
                {
                    "id": 1,
                    "rebalancing_id": 1,
                    "stock_id": 1023662,
                    "stock_name": "华宝油气",
                    "stock_symbol": "SZ162411",
                    "volume": 0.0,
                    "price": None,
                    "net_value": 0.0,
                    "weight": 0.0,
                    "target_weight": 0.1,
                    "prev_weight": None,
                    "prev_target_weight": None,
                    "prev_weight_adjusted": None,
                    "prev_volume": None,
                    "prev_price": None,
                    "prev_net_value": None,
                    "proactive": True,
                    "created_at": 1554339333333,
                    "updated_at": 1554339233333,
                    "target_volume": 0.00068325,
                    "prev_target_volume": None,
                },
                {
                    "id": 2,
                    "rebalancing_id": 1,
                    "stock_id": 1023662,
                    "stock_name": "华宝油气",
                    "stock_symbol": "SZ162411",
                    "volume": 0.0,
                    "price": 0.55,
                    "net_value": 0.0,
                    "weight": 0.0,
                    "target_weight": 0.1,
                    "prev_weight": None,
                    "prev_target_weight": None,
                    "prev_weight_adjusted": None,
                    "prev_volume": None,
                    "prev_price": None,
                    "prev_net_value": None,
                    "proactive": True,
                    "created_at": 1554339333333,
                    "updated_at": 1554339233333,
                    "target_volume": 0.00068325,
                    "prev_target_volume": None,
                },
            ],
            "comment": "",
            "diff": 0.0,
            "new_buy_count": 0,
        }
    ],
    "maxPage": 17,
}
