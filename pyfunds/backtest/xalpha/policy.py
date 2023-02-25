# -*- coding: utf-8 -*-
"""
modules for policy making: generate status table for simple backtesting
"""
import pandas as pd

from xalpha.cons import myround, opendate, yesterdaydash, convert_date
from xalpha.record import record


class policy(record):
    """
    base class for policy making, self.status to get the generating status table

    :param infoobj: info object as evidence for policy making
    :param start: string or object of date, the starting date for policy running
    :param end: string or object of date, the ending date for policy running
    :param totmoney: float or int, characteristic money value,
        not necessary to be the total amount of money
    """

    def __init__(self, infoobj, start, end=yesterdaydash(), totmoney=100000):
        self.aim = infoobj
        self.totmoney = totmoney
        self.price = infoobj.price[
            (infoobj.price["date"] >= start) & (infoobj.price["date"] <= end)
        ]
        if len(self.price) == 0:
            self.start = convert_date(start)
            self.end = convert_date(end)
            self.status = pd.DataFrame(data={"date": [], self.aim.code: []})
        else:
            self.start = self.price.iloc[0].date
            self.end = self.price.iloc[-1].date
            datel = []
            actionl = []
            times = pd.date_range(self.start, self.end)
            for date in times:
                action = self.status_gen(date)
                if action > 0:
                    datel.append(date)
                    actionl.append(action)
                elif action < 0:
                    datel.append(date)
                    actionl.append(action * 0.005)
            df = pd.DataFrame(data={"date": datel, self.aim.code: actionl})
            self.status = df

    def status_gen(self, date):
        """
        give policy decision based on given date

        :param date: date object
        :returns: float, positive for buying money, negative for selling shares
        """
        raise NotImplementedError


class buyandhold(policy):
    """
    simple policy class where buy at the start day and hold forever,
    始终选择分红再投入
    """

    def status_gen(self, date):
        if date == self.start:
            return self.totmoney
        elif date in self.aim.specialdate:
            if self.price[self.price["date"] == date].iloc[0].comment > 0:
                return 0.05
            else:
                return 0
        else:
            return 0


class scheduled(policy):
    """
    fixed schduled purchase for given date list

    :param infoobj: info obj
    :param totmoney: float, money value for purchase every time
    :param times: datelist of datetime object for purchase date, eg ['2017-01-01','2017-07-07',...]
        we recommend you use pd.date_range() to generate the schduled list
    """

    def __init__(self, infoobj, totmoney, times):
        start = times[0]
        end = times[-1]
        self.times = times
        super().__init__(infoobj, start, end, totmoney)

    def status_gen(self, date):
        if date in self.times:
            return self.totmoney
        else:
            return 0


class scheduled_tune(scheduled):
    """
    定期不定额的方式进行投资，基于净值点数分段进行投资
    """

    def __init__(self, infoobj, totmoney, times, piece):
        """
        :param piece: list of tuples, eg.[(1000,2),(2000,1.5)]. It means when the fund netvalue
            is small than some value, we choose to buy multiple times the totmoney. In this example,
            if the netvalue is larger than 2000, then no purchase happen at all.
        """
        self.piece = piece
        super().__init__(infoobj, totmoney, times)

    def status_gen(self, date):
        if date in self.times:
            value = self.price[self.price["date"] >= date].iloc[0].netvalue
            for term in self.piece:
                if value <= term[0]:
                    return term[1] * self.totmoney
            return 0
        else:
            return 0


class scheduled_window(scheduled):
    """
    在定投点前面设置一个滑动窗口，根据滑动窗口中的净值与当前净值进行比较，满足一定条件则进行定投。
    通常用于跌了多投，跌越多投越多；涨了少投，涨越多投越少。
    """

    def __init__(
        self, infoobj, totmoney, times, piece, window=7, window_dist=1, method="AVG"
    ):
        """
        :param window: window width, means the total trading days in the window.
        :param window_dist: the total trading days after window's end date and up to current date.
            Sometimes we only use the data some days before, so we need window_dist to control the
            distance between window and current date. eg. the window is [2021-01-04, 2021-01-05, 2021-01-06],
            current date is 2021-01-07. In this example, the window width is 3, because there are three
            trading days in this window, the window dist for current date is 1, because there is only
            one trading date after 2021-01-06 and up to 2021-01-07.
        :param piece: list of tuples, eg.[(-3,2),(0,1),(3,0.5)]. In this example, it means if the
            fund netvalue rise in the range of (-100%, -3%], we will buy 2*totmoney,
            if the fund netvalue rise in the range of (-3%, 0%], we will buy 1*totmoney,
            if the fund netvalue rise in the range of (0%, 3%], we will buy 0.5*totmoney,
            if the fund netvalue rise in the range of (3%, +infinity), then no purchase happen at all.
        :param method: MAX, MIN, AVG, default value is AVG. It means how we process the data in the window.
        """
        self.window = window
        self.window_dist = window_dist
        self.piece = piece
        self.method = method
        assert self.method in ["MAX", "MIN", "AVG"]
        assert self.window >= 1
        assert self.window_dist >= 1
        super().__init__(infoobj, totmoney, times)

    def status_gen(self, date):
        # skip the date in the first window
        if date in self.times[0 : self.window + self.window_dist - 1]:
            return 0
        if date in self.times:
            price_range = self.price[self.price["date"] < date]
            if len(price_range) < self.window + self.window_dist - 1:
                return 0
            value = self.price[self.price["date"] >= date].iloc[0].netvalue
            window_values = [
                price_range.iloc[-1 * i].netvalue
                for i in range(self.window_dist, self.window + self.window_dist)
            ]
            if self.method == "MAX":
                base_value = max(window_values)
            elif self.method == "MIN":
                base_value = min(window_values)
            else:
                base_value = sum(window_values) / len(window_values)
            for term in self.piece:
                if (value - base_value) / base_value * 100 <= term[0]:
                    return term[1] * self.totmoney
            return 0
        return 0


class grid(policy):
    """
    网格投资类，用于指导网格投资策略的生成和模拟。这一简单的网格，买入仓位基于均分总金额，每次的卖出仓位基于均分总份额。
    因此实际上每次卖出的份额都不到对应原来档位买入的份额，从而可能实现更多的收益。

    :param infoobj: info object, trading aim of the grid policy
    :param buypercent: list of positive int or float, the grid of points when purchasing, in the unit of percent
        比如 [5,5,5,5] 表示以 start 这天的价格为基准，每跌5%，就加一次仓，总共加四次仓
    :param sellpercent: list of positive int or float, the grid of points for selling
        比如 [8,8,8,8] 分别对应上面各买入仓位应该涨到的百分比从而决定卖出的点位，两个列表都是靠前的是高价位仓，两列表长度需一致
    :param start: date str of policy starting
    :param end: date str of policy ending
    :param totmoney: 总钱数，平均分给各个网格买入仓位
    """

    def __init__(
        self,
        infoobj,
        buypercent,
        sellpercent,
        start,
        end=yesterdaydash(),
        totmoney=100000,
    ):
        assert len(buypercent) == len(sellpercent)
        self.division = len(buypercent)
        self.pos = 0
        self.zero = (
            infoobj.price[infoobj.price["date"] >= start].iloc[0].loc["netvalue"]
        )
        buypts = [self.zero]
        sellpts = []
        for term in buypercent:
            buypts.append(buypts[-1] * (1 - term / 100.0))
        for i, term in enumerate(sellpercent):
            sellpts.append(buypts[i + 1] * (1 + term / 100.0))
        self.buypts = buypts[1:]
        self.sellpts = sellpts
        self.buypercent = buypercent
        self.sellpercent = sellpercent
        super().__init__(infoobj, start, end, totmoney)

    def status_gen(self, date):
        # 过滤交易日这一需求，交给各个类自由裁量，这里网格类就需要过掉非交易日干扰，
        # 而定投类中则不过掉，遇到非交易日顺延定投更合理些
        if date.strftime("%Y-%m-%d") not in opendate:
            return 0

        if date == self.start:
            if self.buypercent[0] == 0:
                self.pos += 1
                return myround(self.totmoney / self.division)
            else:
                return 0
        value = self.price[self.price["date"] <= date].iloc[-1].loc["netvalue"]
        valueb = self.price[self.price["date"] <= date].iloc[-2].loc["netvalue"]
        action = 0
        for i, buypt in enumerate(self.buypts):
            if (value - buypt) <= 0 and (valueb - buypt) > 0 and self.pos <= i:
                self.pos += 1
                action += myround(self.totmoney / self.division)
        for j, sellpt in enumerate(self.sellpts):
            if (value - sellpt) >= 0 and (valueb - sellpt) < 0 and self.pos > j:
                action += -1 / self.pos
                self.pos += -1
        return action


class indicator_cross(policy):
    """
    制定两个任意技术指标之间（或和净值之间）交叉时买入卖出的策略。若收盘时恰好交叉，不操作，等第二日趋势确认。

    :param info: info object, trading aim of the policy
    :param col: a tuple with two strings, eg ('netvalue','MA10'), when the left one is over the
        right one, we buy and otherwise we sell, that is the core of cross policy, you can choose
        any two columns as you like, as long as you generate them on the info object before input
        也即左栏数据从下向上穿过右栏数据时，买入；反之亦然
    :param start: date str of policy starting
    :param end: date str of policy ending
    :param totmoney: float or int, total money, in the cross policy, we dont have position division,
        instead we buy all or sell all on the given cross
    """

    def __init__(self, infoobj, col, start, end=yesterdaydash(), totmoney=100000):
        self.col = col
        self.pos = 0
        super().__init__(infoobj, start, end, totmoney)

    def status_gen(self, date):
        if date.strftime("%Y-%m-%d") not in opendate:
            return 0
        rows = self.price[self.price["date"] <= date]
        if len(rows) == 1:
            return 0
        valuel = rows.iloc[-1].loc[self.col[0]]
        valuelb = rows.iloc[-2].loc[self.col[0]]
        valuer = rows.iloc[-1].loc[self.col[1]]
        valuerb = rows.iloc[-2].loc[self.col[1]]
        cond = (valuerb - valuelb) * (valuer - valuel)

        if cond > 0:
            return 0
        if cond == 0 and (valuer - valuel == 0):
            return 0
        if (cond == 0 and (valuer - valuel) != 0) or cond < 0:
            if valuer > valuel:
                if self.pos == 1:
                    self.pos = 0
                    return -1
                else:
                    return 0
            else:
                if self.pos == 0:
                    self.pos = 1
                    return self.totmoney
                else:
                    return 0


class indicator_points(policy):
    """
    基于技术指标的策略生成类之一，给出技术指标的多个阈值，基于这些点数值进行交易

    :param infoobj: info object, trading aim of the policy
    :param col: str, stands for the tracking column of price table, eg. 'netvalue' or 'PSY'
    :param buy: list of tuple, eg [(0.1,1),(0.2,2),(0.3,5)]. buy 1/(1+2+5) of totmoney, when the col
        value approach 0.1 and so on.
    :param sell: similar list of tuple as buy input. the difference is you can omit setting of sell list,
        this implies you don't want to sell. 初始化不设置sell参数，在col设为netvalue时，用于进行金字塔底仓购买特别有效.
        注意不论是 sell 还是 buy 列表，都要将更难实现（离中间值更远）的点位列在后边。比如如果现在是低买模式，
        那么 buy 列表越考后的点数就越小。此外，不建议设置的买点卖点有重叠区域，可能会出现策略逻辑错误。
    :param buylow: Bool, Ture 代表，对应点位是跌破买，涨破卖，如果是 False 则反之，默认是 True
    :param start: date str of policy starting
    :param end: date str of policy ending
    :param totmoney: float or int, total money, in the points policy, we share them as different positions, based on
        the instruction of sell and buy list
    """

    def __init__(
        self,
        infoobj,
        start,
        col,
        buy,
        sell=None,
        buylow=True,
        end=yesterdaydash(),
        totmoney=100000,
    ):
        self.pos = 0
        self.col = col
        self.buylow = buylow
        self.selllevel = 0
        bdivision = sum([it[1] for it in buy])
        self.buy = []
        for item in buy:
            self.buy.append((item[0], item[1] / bdivision))

        if sell is not None:
            self.sell = []
            sdivision = sum([it[1] for it in sell])
            for item in sell:
                self.sell.append((item[0], item[1] / sdivision))
        else:
            self.sell = sell

        super().__init__(infoobj, start, end, totmoney)

    def status_gen(self, date):
        if date.strftime("%Y-%m-%d") not in opendate:
            return 0
        rows = self.price[self.price["date"] <= date]
        if len(rows) == 1:
            return 0
        value = rows.iloc[-1].loc[self.col]
        valueb = rows.iloc[-2].loc[self.col]
        action = 0
        if self.buylow is True:
            judge = 1
        else:
            judge = -1
        for i, term in enumerate(self.buy):
            if (
                judge * (value - term[0]) <= 0 < judge * (valueb - term[0])
                and self.pos + sum([it[1] for it in self.buy[i:]]) <= 1
            ):
                self.pos += term[1]
                action += myround(self.totmoney * term[1])
                self.selllevel = 0
        if self.sell is not None:
            for i, term in enumerate(self.sell):
                if (
                    judge * (value - term[0]) >= 0 > judge * (valueb - term[0])
                    and self.pos > 0
                    and self.selllevel <= i
                ):
                    deltaaction = myround(
                        term[1] / sum([it[1] for it in self.sell[i:]])
                    )
                    action -= (1 + action) * deltaaction  # 需考虑一日卖出多仓的情形
                    self.pos = (1 - deltaaction) * self.pos
                    self.selllevel = i + 1

        return action
