# -*- coding: utf-8 -*-
import os
import time
import uuid
from typing import List

from easytrader import exceptions, webtrader
from easytrader.model import Balance, Deal, Entrust, Position


class MockTrader(webtrader.WebTrader):
    config_path = os.path.dirname(__file__) + "/config/mock.json"

    def __init__(self, **kwargs):
        super(MockTrader, self).__init__()

        # 资金换算倍数
        self.multiple = 1000000

        self.assets = [
            Balance(
                asset_balance=self.multiple,
                current_balance=self.multiple,
                enable_balance=self.multiple,
                frozen_balance=0,
                market_value=0,
                pre_interest=0.25,
                money_type=u"人民币",
            )
        ]

        self.positions: List[Position] = []

        self.entrusts: List[Entrust] = []

        self.deals: List[Deal] = []

    def auto_login(self, **kwargs):
        pass

    def get_balance(self) -> List[Balance]:
        """
        获取账户资金状况
        :return:
        """
        # self._update_balance()
        return self.assets

    def update_balance(self, quotation_data):
        prices = {}
        for code in quotation_data:
            prices[code] = quotation_data[code][-1:].close[0]

        market_value = 0
        for position in self.positions:
            price = prices[position.stock_code]
            position.update(price)
            market_value += position.market_value
        self.assets[0].market_value = market_value
        self.assets[0].update(market_value, self.assets[0].enable_balance)

    def set_quotation(self, quotation):
        self.quotation = quotation

    def get_price(self, stock_code, time):
        # 获取价格
        return self.quotation.get_price(stock_code, time)

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
        return self.positions

    def get_entrust(self) -> List[Entrust]:
        """
        获取委托单(目前返回20次调仓的结果)
        操作数量都按1手模拟换算的
        :return:
        """
        return self.entrusts

    def get_current_deal(self) -> List[Deal]:
        """获取当日成交列表"""
        # return self.do(self.config['current_deal'])
        return self.deals

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
        cost = self.calculate_cost(amount, price, entrust_bs)
        if not volume:
            volume = float(price) * amount  # 可能要取整数

        total_cost = volume + cost
        if balance.current_balance < total_cost and entrust_bs == "B":
            raise exceptions.TradeError(u"没有足够的现金进行操作")
        if amount == 0:
            raise exceptions.TradeError(u"数量不能为0")

        entrust_no = str(uuid.uuid1())
        self.entrust.append(
            Entrust(
                entrust_no=entrust_no,
                bs_type=entrust_bs,
                entrust_status="已成交",
                report_time=self.time.strftime("%Y-%m-%d %H:%M:%S"),
                stock_code=security,
                stock_name=security,
                entrust_amount=amount,
                entrust_price=price,
                cost=cost,
            )
        )

        self.deals.append(
            Deal(
                deal_no=str(uuid.uuid1()),
                entrust_no=entrust_no,
                bs_type=entrust_bs,
                stock_code=security,
                stock_name=security,
                deal_amount=amount,
                deal_price=price,
                entrust_amount=amount,
                entrust_price=price,
                deal_time=self.time.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        balance = self.assets[0]

        position = self.find_hold_position(security)

        if entrust_bs == "B":
            # 更新持仓
            balance.enable_balance = balance.enable_balance - total_cost
            balance.current_balance = max(0, balance.current_balance - total_cost)
            balance.asset_balance -= total_cost
            if position:
                position.cost_price = (
                    position.current_amount * position.cost_price + volume
                ) / (position.current_amount + amount)
                position.current_amount += amount
            else:
                self.positions.append(
                    Position(
                        current_amount=amount,
                        enable_amount=amount,
                        income_balance=0,
                        cost_price=total_cost / amount,
                        last_price=price,
                        market_value=volume,
                        position_str="random",
                        stock_code=security,
                        stock_name=security,
                    )
                )
        else:
            # 卖出
            if position:
                position.current_amount -= amount
                # 更新持仓
                balance.enable_balance = balance.enable_balance + volume - cost

    def find_hold_position(self, code: str) -> Position:
        for position in self.positions:
            if position.stock_code == code:
                return position
        return None

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


if __name__ == "__main__":
    trader = MockTrader()
    trader.prepare("../eastmoney.json")
    print(trader.get_position())
    trader.buy("002230", price=55, amount=100)
