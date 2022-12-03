# -*- coding: utf-8 -*-
import json
import numbers
import os
import pickle
import re
import time
import random
from typing import List

import requests

from easytrader import exceptions, webtrader
from easytrader.log import logger
from easytrader.model import Balance, Position, Entrust, Deal
from easytrader.utils.misc import parse_cookies_str

import ddddocr


class EastMoneyTrader(webtrader.WebTrader):
    config_path = os.path.dirname(__file__) + "/config/jywg.json"
    validate_key = None

    _HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Host": "jywg.18.cn",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Cache-Control": "no-cache",
        "Referer": "https://jywg.18.cn/Login?el=1&clear=1",
        # "X-Requested-With": "XMLHttpRequest",
    }

    random_number = '0.9033461201665647898'
    session_file = 'eastmoney_trader.session'

    def __init__(self, **kwargs):
        super(EastMoneyTrader, self).__init__()

        # 资金换算倍数
        self.multiple = (
            kwargs["initial_assets"] if "initial_assets" in kwargs else 1000000
        )
        if not isinstance(self.multiple, numbers.Number):
            raise TypeError("initial assets must be number(int, float)")
        if self.multiple < 1e3:
            raise ValueError("雪球初始资产不能小于1000元，当前预设值 {}".format(self.multiple))

        if not self._reload_session():
            self.s = requests.Session()
            self.s.verify = False
            self.s.headers.update(self._HEADERS)

        self.account_config = None

    def _recognize_verification_code(self):
        ocr = ddddocr.DdddOcr()
        self.random_number = '0.903%d' % random.randint(100000, 900000)
        req = self.s.get("%s%s" % (self.config['yzm'], self.random_number))
        code = ocr.classification(req.content)
        if len(code) == 4:
            return code
        # code length should be 4
        time.sleep(1)
        return self._recognize_verification_code()

    def _save_session(self):
        """
        save session to a cache file
        """
        # always save (to update timeout)
        with open(self.session_file, "wb") as f:
            pickle.dump((self.validate_key, self.s), f)
            print('updated session cache-file %s' % self.session_file)

    def _reload_session(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, "rb") as f:
                    self.validate_key, self.s = pickle.load(f)
                    return True
            except:
                print('load session failed')
        return False

    def auto_login(self, **kwargs):
        if self.validate_key:
            try:
                self.heartbeat()
                print('already logined in')
                return
            except:
                print('heartbeat failed, login again')

        """
        自动登录
        :return:
        """
        password = self.account_config['password']
        basedir = os.path.split(os.path.realpath(__file__))[0]
        stdout = os.popen(os.path.join(basedir, "./utils/base.exe %s" % password))
        password = stdout.read().strip()
        while True:
            identifyCode = self._recognize_verification_code()
            login_res = self.s.post(self.config['authentication'], data={
                'duration': 1800,
                'password': password,
                'identifyCode': identifyCode,
                'type': 'Z',
                'userId': self.account_config['user'],
                'randNumber': self.random_number,
            }).json()

            if login_res['Status'] != 0:
                logger.info('auto login error, try again later')
                print(login_res)
                time.sleep(3)
            else:
                break

        self._get_valid_key()

        # 保存session
        self._save_session()

    def _get_valid_key(self):
        content = self.s.get(self.config['authentication_check']).text
        key = "input id=\"em_validatekey\" type=\"hidden\" value=\""
        begin = content.index(key) + len(key)
        end = content.index("\" />", begin)
        self.validate_key = content[begin: end]

    def _prepare_account(self, user="", password="", **kwargs):
        """
        转换参数到登录所需的字典格式
        :param cookies: 雪球登陆需要设置 cookies， 具体见
            https://smalltool.github.io/2016/08/02/cookie/
        :param portfolio_code: 组合代码
        :param portfolio_market: 交易市场， 可选['cn', 'us', 'hk'] 默认 'cn'
        :return:
        """
        self.account_config = {
            "user": user,
            "password": password,
        }

    def _virtual_to_balance(self, virtual):
        """
        虚拟净值转化为资金
        :param virtual: 雪球组合净值
        :return: 换算的资金
        """
        return virtual * self.multiple

    def _get_html(self, url):
        return self.s.get(url).text

    def _search_stock_info(self, code):
        """
        通过雪球的接口获取股票详细信息
        :param code: 股票代码 000001
        :return: 查询到的股票 {u'stock_id': 1000279, u'code': u'SH600325',
            u'name': u'华发股份', u'ind_color': u'#d9633b', u'chg': -1.09,
            u'ind_id': 100014, u'percent': -9.31, u'current': 10.62,
            u'hasexist': None, u'flag': 1, u'ind_name': u'房地产', u'type': None,
            u'enName': None}
            ** flag : 未上市(0)、正常(1)、停牌(2)、涨跌停(3)、退市(4)
        """
        data = {
            "code": str(code),
            "size": "300",
            "key": "47bce5c74f",
            "market": self.account_config["portfolio_market"],
        }
        r = self.s.get(self.config["search_stock_url"], params=data)
        stocks = json.loads(r.text)
        stocks = stocks["stocks"]
        stock = None
        if len(stocks) > 0:
            stock = stocks[0]
        return stock

    def _get_assets(self):
        return self._request_data("assets")

    def _request_data(self, api_name: str, params=None):
        api = self._get_api_url(api_name)
        result = self.s.get(api, params=params).json()
        if result['Status'] == 0:
            return result['Data']
        # TODO 错误处理
        return None

    def _get_api_url(self, key):
        return self.config[key] % self.validate_key

    def _get_position(self):
        """
        获取持仓
        :return:
        """
        return self._request_data("get_stock_list")

    def get_balance(self) -> List[Balance]:
        """
        获取账户资金状况
        :return:
        """
        assets = self._get_assets()

        if not assets:
            raise exceptions.TradeError(u"获取资金失败")

        assets = assets[0]

        # {'Message': None, 'Status': 0, 'Data': [{'Zzc': '1.00', 'Zxsz': '0.00', 'Kyzj': '1.00', 'Kqzj': '1.00',
        # 'Djzj': '0.00', 'Zjye': '1.00', 'Money_type': 'RMB', 'Drckyk': None, 'Ljyk': None, 'F303S': None}]}
        return [
            Balance(
                asset_balance=float(assets['Zzc']),
                current_balance=float(assets['Kqzj']),
                enable_balance=float(assets['Kyzj']),
                frozen_balance=float(assets['Djzj']),
                market_value=float(assets['Zzc']) - float(assets['Kyzj']),
                money_type=u"人民币")
        ]

    @staticmethod
    def _time_strftime(time_stamp):
        try:
            local_time = time.localtime(time_stamp / 1000)
            return time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        # pylint: disable=broad-except
        except Exception:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def get_position(self) -> List[Position]:
        """
        获取持仓
        :return:
        """
        server_positions = self._request_data("get_stock_list")
        if server_positions is None:
            raise exceptions.TradeError(u"获取持仓失败")

        balance = self.get_balance()[0]
        print(balance)
        position_list = []

        # TODO 验证
        for pos in server_positions:
            position_list.append(
                Position(
                    current_amount=int(pos["Zqsl"]),
                    enable_amount=int(pos["Kysl"]),
                    income_balance=0,
                    cost_price=float(pos["Cbjg"]),
                    last_price=float(pos["Zxjg"]),
                    market_value=float(pos["Zxjg"]) * int(pos["Zqsl"]),
                    position_str="random",
                    stock_code=pos["Zqdm"],
                    stock_name=pos["Zqmc"],
                ))
        return position_list

    def get_entrust(self) -> List[Entrust]:
        """
        获取委托单(目前返回20次调仓的结果)
        操作数量都按1手模拟换算的
        :return:
        """
        xq_entrust_list = self._request_data("get_orders_data")
        entrust_list = []
        for xq_entrusts in xq_entrust_list:
            entrust_list.append(
                Entrust(
                    entrust_no=xq_entrusts["Wtbh"],
                    bs_type=xq_entrusts["Mmlb"],
                    entrust_status=xq_entrusts["Wtzt"],
                    report_time=self._format_time(xq_entrusts["Bpsj"]),
                    stock_code=xq_entrusts["Zqdm"],
                    stock_name=xq_entrusts["Zqmc"],
                    entrust_amount=int(xq_entrusts["Wtsl"]),
                    entrust_price=float(xq_entrusts["Wtjg"]),
                )
            )
        return entrust_list

    def get_current_deal(self) -> List[Deal]:
        """获取当日成交列表"""
        # return self.do(self.config['current_deal'])
        data_list = self._request_data("get_deal_data")
        result = []
        for item in data_list:
            result.append(
                Deal(
                    deal_no=item["Cjbh"],
                    entrust_no=item["Wtbh"],
                    bs_type=item["Mmlb"],
                    stock_code=item["Zqdm"],
                    stock_name=item["Zqmc"],
                    deal_amount=int(item["Cjsl"]),
                    deal_price=float(item["Cjjg"]),
                    entrust_amount=int(item["Wtsl"]),
                    entrust_price=float(item["Wtjg"]),
                    deal_time=self._format_time(item["Cjsj"]),
                )
            )
        return result

    def _format_time(self, time):
        return "%s:%s:%s" % (time[0:2], time[2:4], time[4:])

    def cancel_entrust(self, entrust_no):

        """

        :param entrust_no:
        :return:
        """
        # TODO
        return True

    def _trade(self, security, price=0, amount=0, volume=0, entrust_bs="B"):
        """
        调仓
        :param security:
        :param price:
        :param amount:
        :param volume:
        :param entrust_bs:
        :return:
        """
        balance = self.get_balance()[0]
        if not volume:
            volume = int(float(price) * amount)  # 可能要取整数
        if balance.current_balance < volume and entrust_bs == "B":
            raise exceptions.TradeError(u"没有足够的现金进行操作")
        if amount == 0:
            raise exceptions.TradeError(u"数量不能为0")

        response = self.s.post(self._get_api_url('submit'), data={
            "stockCode": security,
            "price": price,
            "amount": amount,
            "zqmc": "unknown",
            "tradeType": entrust_bs
        }).json()

        if response['Status'] != 0:
            raise exceptions.TradeError('下单失败, %s' % json.dumps(response))

        logger.info('下单成功')

    def buy(self, security, price=0, amount=0, volume=0, entrust_prop=0):
        """买入卖出股票
        :param security: 股票代码
        :param price: 买入价格
        :param amount: 买入股数
        :param volume: 买入总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop:
        """
        return self._trade(security, price, amount, volume, "B")

    def sell(self, security, price=0, amount=0, volume=0, entrust_prop=0):
        """卖出股票
        :param security: 股票代码
        :param price: 卖出价格
        :param amount: 卖出股数
        :param volume: 卖出总金额 由 volume / price 取整， 若指定 price 则此参数无效
        :param entrust_prop:
        """
        return self._trade(security, price, amount, volume, "S")


if __name__ == '__main__':
    trader = EastMoneyTrader()
    trader.prepare('../eastmoney.json')
    print(trader.get_position())
    trader.buy('002230', price=55, amount=100)
