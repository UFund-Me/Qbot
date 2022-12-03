import time
import datetime
from typing import List, Dict

from dateutil import tz
from pandas import DataFrame

from easyquant import DefaultLogHandler
from easyquant import StrategyTemplate
from easyquant.context import Context
from easyquant.event_engine import Event
from easytrader.model import Position


class Strategy(StrategyTemplate):
    name = '测试策略1'
    # 每次T的数量
    t_amount = 5000
    # 股票
    watch_stocks = ["002230"]
    last_buy_time = 0
    last_sail_time = 0
    cci_down_count = 0
    min_transaction_interval = 1000 * 5 * 60

    def init(self):
        for stock_code in self.watch_stocks:
            self.quotation_engine.watch(stock_code)

    def on_bar(self, context: Context, data: Dict[str, DataFrame]):
        balance = context.balance[0]
        positions = context.position

        for stock_code in self.watch_stocks:

            # 获取分钟行情数据
            df = data[stock_code]
            latest = df[-1:]

            stock_pos = self.get_stock_pos(positions, stock_code)

            current_price = latest.close[0]
            # self.log.info("当前价格： %s" % latest.close[0])
            stock_pos.market_value = stock_pos.current_amount * current_price

            cci = context.calculate_cci(df, time_period=14)
            rsi6 = context.calculate_rsi(df, time_period=6)

            # 最新的RSI 和 CCI
            rsi6 = rsi6.values[:-10:-1]
            cci_last_10 = cci.values[:-10:-1]
            ma_20 = df.close[:-24:-1].mean()
            # self.log.info('%s CCI:%s' % (stock_code, cci_last_10[0:3]))
            # self.log.info('%s RSI6:%s' % (stock_code, rsi6[0:3]))

            last_cci = cci_last_10[0]

            last_rsi = rsi6[0]
            if last_rsi > 80 or rsi6[1] > 80:
                # self.log.info("cci enter high space")
                # 持仓为0
                if stock_pos.current_amount == 0:
                    continue
                # 获取上两个cci
                if last_rsi > rsi6[1]:
                    # 还在上升
                    continue
                    # self.log.info("上升中，继续持仓")
                else:
                    # self.log.info('%s CCI:%s' % (stock_code, cci_last_10[0:3]))
                    self.log.info('%s RSI6:%s' % (stock_code, rsi6[0:3]))
                    # 如果卖过1次，需要等买了后再卖
                    amount = stock_pos.current_amount
                    self.log.info("RSI拐点，卖出 %s元 %s股" % (latest.close[0], amount))
                    self.user.sell(stock_code, price=latest.close[0],
                                   amount=amount)
                    self.log.info('%s 盈亏: %s ' % (stock_code,
                                                  amount * (latest.close[0] - stock_pos.cost_price)))
                    return
            elif last_rsi < 35 or rsi6[1] < 35:
                # self.log.info("enter low space")
                # 上穿-200时买入
                if last_rsi > rsi6[1]:
                    buy_amount = balance.enable_balance / 100 / latest.close[0] / 1.003
                    buy_amount = int(buy_amount) * 100

                    if buy_amount == 0:
                        self.log.info("没钱买入")
                        continue
                    self.log.info('%s RSI6:%s' % (stock_code, rsi6[0:3]))
                    # self.log.info('%s CCI:%s' % (stock_code, cci_last_10[0:3]))
                    self.log.info("RSI上穿，抄底买入 %s元 %s股" % (latest.close[0], buy_amount))

                    self.user.buy(stock_code, price=latest.close[0], amount=buy_amount)
                    return

            # TODO 跌破10日线止损
            if latest.close[0] < ma_20 and stock_pos.current_amount > 0 and stock_pos.cost_price > latest.close[0]:
                self.log.info("跌破20日线，止损 %s元 " % latest.close[0])
                amount = stock_pos.current_amount
                self.user.sell(stock_code, price=latest.close[0],
                               amount=stock_pos.current_amount)
                self.log.info('%s 盈亏: %s ' % (stock_code,
                                              amount * (latest.close[0] - stock_pos.cost_price)))


    def get_stock_pos(self, positions, stock_code):
        stock_pos = list(filter(lambda pos: pos.stock_code == stock_code, positions))
        if len(stock_pos) == 0:
            stock_pos = Position(current_amount=0,
                                 enable_amount=0,
                                 income_balance=0,
                                 cost_price=0,
                                 last_price=0,
                                 market_value=0,
                                 position_str="random",
                                 stock_code=stock_code,
                                 stock_name=stock_code)
        else:
            stock_pos = stock_pos[0]
        return stock_pos

    def on_close(self, context: Context):
        pass

    def on_open(self, context: Context):
        pass

    def shutdown(self):
        """
        关闭进程前的调用
        :return:
        """
        self.log.info("假装在关闭前保存了策略数据")
