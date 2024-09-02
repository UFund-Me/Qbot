# coding: utf-8
import unittest

from easytrader.xqtrader import XueQiuTrader


class TestXueQiuTrader(unittest.TestCase):
    def test_prepare_account(self):
        user = XueQiuTrader()
        params_without_cookies = dict(
            portfolio_code="ZH123456", portfolio_market="cn"
        )
        with self.assertRaises(TypeError):
            user._prepare_account(**params_without_cookies)

        params_without_cookies.update(cookies="123")
        user._prepare_account(**params_without_cookies)
        self.assertEqual(params_without_cookies, user.account_config)
