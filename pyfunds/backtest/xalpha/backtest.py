# -*- coding: utf-8 -*-
"""
modules for dynamical backtesting framework
"""

import pandas as pd

from xalpha.info import fundinfo, mfundinfo, cashinfo
from xalpha.trade import trade
from xalpha.multiple import mul, mulfix
from xalpha.cons import yesterdayobj, avail_dates
from xalpha.exceptions import TradeBehaviorError, FundTypeError
from xalpha.cons import opendate_set, next_onday, convert_date
from xalpha.universal import vinfo


class GlobalRegister:
    def __init__(self):
        pass


class BTE:
    """
    BackTestEnvironment, currently only fund is supported
    vinfo is partially supported, however stock refactor is not carefully considered
    To use such powerful dynamical backtesting, one need to subclass ``BTE``

    """

    def __init__(self, start, end=None, totmoney=1000000, verbose=False, **kws):
        self.start = convert_date(start)
        self.verbose = verbose
        self.kws = kws
        self.totmoney = totmoney
        self.g = GlobalRegister()
        self.trades = {}  # codes: infoobj
        self.infos = {}  # codes: infoobj
        self.lastdates = {}  # codes: date
        if end is None:
            end = yesterdayobj()
        self.end = end
        self.sys = None

    def prepare(self):
        """
        initialization function for the backtest, like variable assignment and data preparation

        :return:
        """
        pass

    def run(self, date):
        """
        core method to be implemented in subclass,
        input the date, and access other informations from self
        then decide whether do some self.buy and self.sell

        :param date: datetime obj
        :return:
        """
        raise NotImplementedError("Please implement your `run` function in your class")

    def backtest(self):
        """
        run the whole backtest

        :return:
        """
        self.prepare()
        dates = pd.bdate_range(self.start, self.end)
        for d in dates:  # 考虑到暂时只支持基金，只在国内交易日运行
            if d.strftime("%Y-%m-%d") in opendate_set:
                self.run(d)

    def get_current_mul(self):
        """
        get ``xa.mul`` of the whole setup

        :return:
        """
        if self.trades:
            return mul(*[v for _, v in self.trades.items()])
        else:
            return

    def get_current_mulfix(self, totmoney=None):
        """
        get ``xa.mulfix`` of the whole setup

        :return:
        """
        if self.trades:
            if totmoney is None:
                totmoney = self.totmoney
            return mulfix(
                *[v for _, v in self.trades.items()],
                totmoney=totmoney,
                cashobj=cashinfo(start=self.start),
            )
        else:
            return

    def set_fund(self, code, value_label=0, round_label=0, dividend_label=0):
        """
        set property of fund

        :param code: F123456, code in backtest must start with F for fund
        :param value_label: 0,1
        :param round_label: 0,1
        :param dividend_label: 0,1
        :return:
        """
        if code in self.infos:
            self.infos[code].value_label = value_label
            self.infos[code].round_label = round_label
            self.infos[code].dividend_label = dividend_label
        else:
            self.infos[code] = self.get_info(code)
            self.infos[code].value_label = value_label
            self.infos[code].round_label = round_label
            self.infos[code].dividend_label = dividend_label

    def get_info(self, code):
        """
        get the correct new info object based on Fcode

        :param code:
        :return:
        """
        if code in self.infos:
            return self.infos[code]
        if code.startswith("F"):
            try:
                return fundinfo(code[1:])
            except FundTypeError:
                return mfundinfo(code[1:])
        elif code.startswith("M"):
            return mfundinfo(code[1:])
        else:
            return vinfo(
                code, start=(self.start - pd.Timedelta(days=180)).strftime("%Y-%m-%d")
            )

    def get_code(self, code):
        """
        get standard code in status code column

        :param code:
        :return:
        """
        if code.startswith("F") or code.startswith("M"):
            return code[1:]
        else:
            return code

    def get_current_asset(self, date):
        """
        获取策略投入的资产在 date 日净值

        :param date:
        :return:
        """
        sys = self.get_current_mul()
        if sys is not None:
            sys = sys.summary(date.strftime("%Y-%m-%d"))
            row = sys[sys["基金名称"] == "总计"].iloc[0]
            current = row["基金现值"]
        else:
            current = 0
        return current

    def buy(self, code, value, date, is_value=True):
        """

        :param code: Fcode
        :param value:
        :param date: datetime obj
        :param is_value: bool, default True. whether the quantity in value is counted in value or in share,
                only value is supported for funds. 基金无法按份额申购。
        :return:
        """
        if self.verbose:
            print(f"buy {value} of {code} on {date.strftime('%Y-%m-%d')}")
        if code in self.trades:
            df = self.trades[code].status
            cftable = self.trades[code].cftable
            cftable = cftable[cftable["date"] <= self.lastdates[code]]
            remtable = self.trades[code].remtable
            remtable = remtable[remtable["date"] <= self.lastdates[code]]
            self.lastdates[code] = date
            df2 = pd.DataFrame([[date, value]], columns=["date", self.get_code(code)])
            df = df.append(df2)
            self.trades[code] = trade(
                self.infos[code],
                df,
                cftable=cftable,
                remtable=remtable,
            )
        else:
            self.lastdates[code] = date
            if code not in self.infos:
                self.infos[code] = self.get_info(code)
            df = pd.DataFrame({"date": [date], self.get_code(code): [value]})
            self.trades[code] = trade(self.infos[code], df)

    def sell(self, code, share, date, is_value=False):
        """

        :param code:
        :param share:
        :param date: datetime obj
        :param is_value: bool, default False. 货币基金可按照金额赎回
        :return:
        """

        share = abs(share)
        if self.verbose:
            print(f"sell {share} of {code} on {date.strftime('%Y-%m-%d')}")
        if code not in self.trades:
            raise TradeBehaviorError("You are selling something that you don't have")
        df = self.trades[code].status
        cftable = self.trades[code].cftable
        cftable = cftable[cftable["date"] <= self.lastdates[code]]
        remtable = self.trades[code].remtable
        remtable = remtable[remtable["date"] <= self.lastdates[code]]
        self.lastdates[code] = date
        self.lastdates[code] = date
        df2 = pd.DataFrame([[date, -share]], columns=["date", self.get_code(code)])
        df = df.append(df2)
        if is_value:
            self.set_fund(code, value_label=1)
        self.trades[code] = trade(
            self.infos[code],
            df,
            cftable=cftable,
            remtable=remtable,
        )
        if is_value:
            self.set_fund(code, value_label=0)


## the following are some example backtest policy classes for testing and educational purpose
## they are not stable in terms of API, and don't rely on them in production environment


class Scheduled(BTE):
    """
    无脑定投类
    """

    def prepare(self):
        self.code = self.kws["code"]
        self.value = self.kws["value"]  # 每次投入金额
        self.date_range = self.kws["date_range"]  # pd.data_range 买入日期列表

    def run(self, date):
        if date in self.date_range:
            self.buy(self.code, self.value, date)


class AverageScheduled(Scheduled):
    """
    最简单的价值平均定投类
    """

    def prepare(self):
        super().prepare()
        self.aim = 0  # 累积目标净值
        self.infos[self.code] = self.get_info(self.code)

    def run(self, date):
        if date in self.date_range:
            self.aim += self.value
            sys = self.get_current_mul()
            if sys is not None:
                sys = sys.summary(date.strftime("%Y-%m-%d"))
                row = sys[sys["基金名称"] == "总计"].iloc[0]
                current = row["基金现值"]
            else:
                current = 0

            if self.aim > current:
                self.buy(self.code, self.aim - current, date)
            else:
                df = self.infos[self.code].price
                unitvalue = df[df["date"] >= date].iloc[0].netvalue
                self.sell(self.code, (current - self.aim) / unitvalue, date)


class ScheduledSellonXIRR(Scheduled):
    """
    无脑定投+年化收益率达到阈值全部卖出
    """

    def prepare(self):
        super().prepare()
        self.sold = False
        self.threhold = self.kws.get("threhold", 0.2)
        self.holding_time = self.kws.get("holding_time", 180)
        self.check_weekday = self.kws.get("check_weekday", 4)
        # 定投开始一定时间后，才按照年化判断退出时机

    def run(self, date):
        if (
            date.weekday() == self.check_weekday
            and not self.sold
            and (date - self.start).days > self.holding_time
        ):  #  每周只检查一次退出条件
            sys = self.get_current_mul()
            if sys is not None:
                try:
                    xirr = sys.xirrrate(date=date.strftime("%Y-%m-%d"))
                except RuntimeError:
                    xirr = 0.0
                if self.verbose:
                    print(f"{date.strftime('%Y-%m-%d')} 内部年化收益率为 {round(xirr*100, 0)}%")
                if xirr > self.threhold:
                    self.sold = True
                    self.sell(self.code, -0.005, date)
        if not self.sold:
            super().run(date)


class Tendency28(BTE):
    """
    二八趋势轮动
    """

    def prepare(self):
        self.aim1 = self.kws.get("aim1", "SH000300")
        self.aim2 = self.kws.get("aim2", "SH000905")
        self.aim0 = self.kws.get("aim0", "M000198")
        self.freq = self.kws.get("freq", "W-THU")
        self.check_dates = avail_dates(
            pd.date_range(self.start, self.end, freq=self.freq)
        )
        self.upthrehold = self.kws.get("upthrehold", 1.0)
        self.diffthrehold = self.kws.get("diffthrehold", self.upthrehold)
        self.prev = self.kws.get("prev", 10)
        self.status = 0  # have aim0
        self.initial_money = self.kws.get("initial_money", self.totmoney / 2.0)
        self.buy(self.aim0, self.initial_money, self.start)

    def run(self, date):
        if date not in self.check_dates:
            return
        df1 = self.get_info(self.aim1).price
        df1 = df1[df1["date"] < date]
        up1 = (
            (df1.iloc[-1].netvalue - df1.iloc[-1 - self.prev].netvalue)
            / df1.iloc[-1 - self.prev].netvalue
            * 100
        )
        df2 = self.get_info(self.aim2).price
        df2 = df2[df2["date"] < date]
        up2 = (
            (df2.iloc[-1].netvalue - df2.iloc[-1 - self.prev].netvalue)
            / df2.iloc[-1 - self.prev].netvalue
            * 100
        )
        if up1 < self.upthrehold and up2 < self.upthrehold:
            if self.status == 1:
                value = self.get_current_asset(date)
                self.sell(self.aim1, -0.005, date)
                self.status = 0
                self.buy(self.aim0, value, date)
            elif self.status == 2:
                value = self.get_current_asset(date)
                self.sell(self.aim2, -0.005, date)
                self.status = 0
                self.buy(self.aim0, value, date)
        elif up1 > self.upthrehold and up1 > up2:
            if self.status == 0:
                value = self.get_current_asset(date)
                self.sell(self.aim0, -0.005, date, is_value=False)
                self.status = 1
                self.buy(self.aim1, value, date)
            elif self.status == 2 and up1 - up2 > self.diffthrehold:
                value = self.get_current_asset(date)
                self.sell(self.aim2, -0.005, date)
                self.status = 1
                self.buy(self.aim1, value, date)
        elif up2 > self.upthrehold and up2 > up1:
            if self.status == 0:
                value = self.get_current_asset(date)
                self.sell(self.aim0, -0.005, date, is_value=False)
                self.status = 2
                self.buy(self.aim2, value, date)
            elif self.status == 1 and up2 - up1 > self.diffthrehold:
                value = self.get_current_asset(date)
                self.sell(self.aim1, -0.005, date)
                self.status = 2
                self.buy(self.aim2, value, date)


class Balance(BTE):
    """
    动态平衡
    """

    def prepare(self):
        self.check_dates = avail_dates(self.kws.get("check_dates"))
        for i, s in enumerate(self.check_dates):
            if isinstance(s, str):
                self.check_dates[i] = pd.Timestamp(s)
        self.portfolio_dict = self.kws.get(
            "portfolio_dict"
        )  # value is float with the sum as 1 instead of 100.
        self.nill = True

    def run(self, date):
        if self.nill is True:  # 建仓买入
            for fund, ratio in self.portfolio_dict.items():
                self.set_fund(fund, dividend_label=1)
                self.buy(fund, ratio * self.totmoney, date)
            self.nill = False
        if date in self.check_dates:
            # 动态平衡
            sys = self.get_current_mul()
            df = sys.summary(date.strftime("%Y-%m-%d"))
            total_value = df[df["基金名称"] == "总计"]["基金现值"].iloc[0]
            for fund, ratio in self.portfolio_dict.items():
                delta = df[df["基金代码"] == fund[1:]]["基金现值"].iloc[0] - total_value * ratio
                if delta > 0:
                    share = round(
                        delta
                        / (1 - 0.005)
                        / df[df["基金代码"] == fund[1:]]["当日净值"].iloc[0],
                        2,
                    )
                    self.sell(fund, share, date)  # 赎回份额考虑赎回费估算为千五，会导致末态并非完全平衡
                elif delta < 0:
                    self.buy(fund, -delta, date)
