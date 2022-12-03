import time
import datetime
from typing import List, Dict

from dateutil import tz
from pandas import DataFrame

from easyquant import DefaultLogHandler
from easyquant import StrategyTemplate
from easyquant.context import Context
from easyquant.event_engine import Event


class Strategy(StrategyTemplate):
    name = '测试策略1'
    # 每次T的数量
    t_amount = 5000
    # 股票
    watch_stocks = ["164906"]
    last_buy_time = 0
    last_sail_time = 0
    min_transaction_interval = 1000 * 5 * 60

    def init(self):
        for stock_code in self.watch_stocks:
            self.quotation_engine.watch(stock_code)

        # 注册时钟事件
        clock_type = "盘尾"
        # now = datetime.datetime(2016, 7, 14, 8, 59, 50, tzinfo=tzinfo)

        # self.clock_engine.run_daily(self.on_bar, "00:45")

        # 开盘前(9:00)运行:
        #
        # run_monthly/run_weekly/run_daily中指定time='09:00'运行的函数
        # before_trading_start
        # 盘中运行:
        #
        # run_monthly/run_weekly/run_daily中在指定交易时间执行的函数, 执行时间为这分钟的第一秒. 例如: run_daily(func, '14:50') 会在每天的14:50:00(精确到秒)执行
        # handle_data
        # 按日回测/模拟, 在9:30:00(精确到秒)运行, data为昨天的天数据
        # 按分钟回测/模拟, 在每分钟的第一秒运行, 每天执行240次, 不包括11:30和15:00这两分钟, data是上一分钟的分钟数据. 例如: 当天第一次执行是在9:30:00, data是昨天14:59至15:00这一分钟的分钟数据, 当天最后一次执行是在14:59:00, data是14:58至14:59:00这一分钟的分钟数据.
        # 收盘后(15:00后半小时内)运行:
        #
        # run_monthly/run_weekly/run_daily中指定time='15:30'运行的函数
        # after_trading_end

        # moment = datetime.time(14, 56, 30, tzinfo=tz.tzlocal())
        #
        # self.clock_engine.register_moment(clock_type, moment)
        #
        # # 注册时钟间隔事件, 不在交易阶段也会触发, clock_type == minute_interval
        # minute_interval = 1.5
        # self.clock_engine.register_interval(minute_interval, trading=False)

    def on_bar(self, context: Context, data: Dict[str, DataFrame]):
        positions = self.user.get_position()

        for stock_code in self.watch_stocks:
            # self.log.info('行情数据: %s %s' % (stock_code, data[stock_code]))
            stock_pos = list(filter(lambda pos: pos.stock_code == stock_code, positions))
            if len(stock_pos) == 0:
                self.log.info('持仓不包含%s' % stock_code)
                continue
            stock_pos = stock_pos[0]

            self.log.info('%s 名称：%s 市值:%s 盈亏: %s' %
                          (stock_code, stock_pos.stock_name, stock_pos.market_value,
                           stock_pos.market_value - stock_pos.cost_price * stock_pos.current_amount))

            # 获取分钟行情数据
            df = data[stock_code]
            latest = df[-1:]
            print(latest.close[0])
            cci = context.calculate_cci(df, time_period=14)
            rsi6 = context.calculate_rsi(df, time_period=6)

            # 最新的RSI 和 CCI
            rsi6 = rsi6.values[:-10:-1]
            cci_last_10 = cci.values[:-10:-1]
            self.log.info('%s CCI:%s' % (stock_code, cci_last_10[0:3]))
            self.log.info('%s RSI6:%s' % (stock_code, rsi6[0:3]))

            last_cci = cci_last_10[0]
            last_rsi = rsi6[0]
            if last_cci > 100 and last_rsi > 60:
                self.log.info("cci enter high space")
                # 持仓为0
                if stock_pos.current_amount == 0:
                    continue
                # 获取上两个cci
                if last_cci > cci_last_10[1] and last_cci > cci_last_10[2]:
                    # 还在上升
                    self.log.info("上升中，继续持仓")
                else:
                    # 如果卖过1次，需要等买了后再卖
                    now = time.time()
                    if now - self.last_sail_time < self.min_transaction_interval:
                        self.log.info("CCI拐点，卖出，但是该周期已卖，跳过")
                        continue
                    self.log.info("CCI拐点，卖出")
                    self.user.sell(stock_code, price=latest.close[0],
                                   amount=min(self.t_amount, stock_pos.current_amount))
                    self.last_sail_time = now

            elif last_cci < -100 and last_rsi < 40:
                self.log.info("enter low space")
                # 上穿-200时买入
                if cci_last_10[1] < -200 < last_cci:
                    now = time.time()
                    if now - self.last_buy_time < self.min_transaction_interval:
                        self.log.info("CCI上穿-200，但是该周期已买，跳过")
                        continue
                    self.log.info("CCI上穿-200，抄底买入")
                    self.user.buy(stock_code, price=latest.close[0],
                                  amount=self.t_amount)
                    self.last_buy_time = now

            self.log.info('\n')

    def on_close(self, context: Context):
        pass

    def on_open(self, context: Context):
        pass

    def log_handler(self):
        """自定义 log 记录方式"""
        return DefaultLogHandler(self.name, log_type='stdout', filepath='demo1.log')

    def shutdown(self):
        """
        关闭进程前的调用
        :return:
        """
        self.log.info("假装在关闭前保存了策略数据")
