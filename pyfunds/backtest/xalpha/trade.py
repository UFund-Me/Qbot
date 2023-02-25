# -*- coding: utf-8 -*-
"""
module for trade class
"""
import math
import datetime as dt
import logging

import pandas as pd
from pyecharts.charts import Bar, Line
from pyecharts import options as opts

import xalpha.remain as rm
from xalpha.cons import convert_date, line_opts, myround, xirr, yesterdayobj
from xalpha.exceptions import ParserFailure, TradeBehaviorError
from xalpha.record import irecord
import xalpha.universal as xu
from xalpha.universal import get_rt

logger = logging.getLogger(__name__)


def xirrcal(cftable, trades, date, startdate=None, guess=0.01):
    """
    calculate the xirr rate

    :param cftable: cftable (pd.Dateframe) with date and cash column
    :param trades: list [trade1, ...], every item is an trade object,
        whose shares would be sold out virtually
    :param date: string of date or datetime object,
        the date when virtually all holding positions being sold
    :param guess: floating number, a guess at the xirr rate solution to be used
        as a starting point for the numerical solution
    :returns: the IRR as a single floating number
    """
    date = convert_date(date)
    partcftb = cftable[cftable["date"] <= date]
    if len(partcftb) == 0:
        return 0
    if not startdate:
        cashflow = [(row["date"], row["cash"]) for i, row in partcftb.iterrows()]
    else:
        if not isinstance(startdate, dt.datetime):
            startdate = dt.datetime.strptime(
                startdate.replace("-", "").replace("/", ""), "%Y%m%d"
            )
        start_cash = 0
        for fund in trades:
            start_cash += fund.briefdailyreport(startdate).get("currentvalue", 0)
        cashflow = [(startdate, -start_cash)]
        partcftb = partcftb[partcftb["date"] > startdate]
        cashflow.extend([(row["date"], row["cash"]) for i, row in partcftb.iterrows()])
    rede = 0
    for fund in trades:
        if not isinstance(fund, itrade):
            partremtb = fund.remtable[fund.remtable["date"] <= date]
            if len(partremtb) > 0:
                rem = partremtb.iloc[-1]["rem"]
            else:
                rem = []
            rede += fund.aim.shuhui(
                fund.briefdailyreport(date).get("currentshare", 0), date, rem
            )[1]
        else:  # 场内交易
            rede += fund.briefdailyreport(date).get("currentvalue", 0)
    cashflow.append((date, rede))
    return xirr(cashflow, guess)


def bottleneck(cftable):
    """
    find the max total input in the history given cftable with cash column

    :param cftable: pd.DataFrame of cftable
    """
    if len(cftable) == 0:
        return 0
    # cftable = cftable.reset_index(drop=True) # unnecessary as iloc use natural rows instead of default index
    inputl = [-sum(cftable.iloc[:i].cash) for i in range(1, len(cftable) + 1)]
    return myround(max(inputl))


def turnoverrate(cftable, end=yesterdayobj()):
    """
    calculate the annualized turnoverrate

    :param cftable: pd.DataFrame of cftable
    :param end: str or obj of datetime for the end date of the estimation
    """
    if len(cftable) == 0:
        return 0
    end = convert_date(end)
    start = cftable.iloc[0].date
    tradeamount = sum(abs(cftable.loc[:, "cash"]))
    turnover = tradeamount / bottleneck(cftable) / 2.0
    if (end - start).days <= 0:
        return 0
    return turnover * 365 / (end - start).days


def vtradevolume(cftable, freq="D", rendered=True):
    """
    aid function on visualization of trade summary

    :param cftable: cftable (pandas.DataFrame) with at least date and cash columns
    :param freq: one character string, frequency label, now supporting D for date,
        W for week and M for month, namely the trade volume is shown based on the time unit
    :returns: the Bar object
    """
    ### WARN: datazoom and time conflict, sliding till 1970..., need further look into pyeacharts
    startdate = cftable.iloc[0]["date"]
    if freq == "D":
        # datedata = [d.to_pydatetime() for d in cftable["date"]]
        datedata = pd.date_range(startdate, yesterdayobj(), freq="D")
        selldata = [
            [row["date"].to_pydatetime(), row["cash"]]
            for _, row in cftable.iterrows()
            if row["cash"] > 0
        ]
        buydata = [
            [row["date"].to_pydatetime(), row["cash"]]
            for _, row in cftable.iterrows()
            if row["cash"] < 0
        ]
    elif freq == "W":
        cfmerge = cftable.groupby([cftable["date"].dt.year, cftable["date"].dt.week])[
            "cash"
        ].sum()
        # datedata = [
        #     dt.datetime.strptime(str(a) + "4", "(%Y, %W)%w")
        #     for a, _ in cfmerge.iteritems()
        # ]
        datedata = pd.date_range(
            startdate, yesterdayobj() + pd.Timedelta(days=7), freq="W-THU"
        )
        selldata = [
            [dt.datetime.strptime(str(a) + "4", "(%G, %V)%w"), b]
            for a, b in cfmerge.iteritems()
            if b > 0
        ]
        buydata = [
            [dt.datetime.strptime(str(a) + "4", "(%G, %V)%w"), b]
            for a, b in cfmerge.iteritems()
            if b < 0
        ]
        # %V pandas gives iso weeknumber which is different from python original %W or %U,
        # see https://stackoverflow.com/questions/5882405/get-date-from-iso-week-number-in-python for more details
        # python3.6+ required for %G and %V
        # but now seems no equal distance between sell and buy data, no idea why
    elif freq == "M":
        cfmerge = cftable.groupby([cftable["date"].dt.year, cftable["date"].dt.month])[
            "cash"
        ].sum()
        # datedata = [
        #     dt.datetime.strptime(str(a) + "15", "(%Y, %m)%d")
        #     for a, _ in cfmerge.iteritems()
        # ]
        datedata = pd.date_range(
            startdate, yesterdayobj() + pd.Timedelta(days=31), freq="MS"
        )
        selldata = [
            [dt.datetime.strptime(str(a) + "1", "(%Y, %m)%d"), b]
            for a, b in cfmerge.iteritems()
            if b > 0
        ]
        buydata = [
            [dt.datetime.strptime(str(a) + "1", "(%Y, %m)%d"), b]
            for a, b in cfmerge.iteritems()
            if b < 0
        ]
    else:
        raise ParserFailure("no such freq tag supporting")

    buydata = [[d, round(x, 1)] for d, x in buydata]
    selldata = [[d, round(x, 1)] for d, x in selldata]
    bar = Bar()
    datedata = list(datedata)
    bar.add_xaxis(xaxis_data=datedata)
    # buydata should before selldata, since emptylist in the first line would make the output fig empty: may be bug in pyecharts
    bar.add_yaxis(series_name="买入", yaxis_data=buydata)
    bar.add_yaxis(series_name="卖出", yaxis_data=selldata)
    bar.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            trigger="axis",
            trigger_on="mousemove",
            axis_pointer_type="cross",
        ),
        datazoom_opts=[opts.DataZoomOpts(range_start=90, range_end=100)],
    )
    if rendered:
        return bar.render_notebook()
    else:
        return bar


def vtradecost(
    self, cftable, unitcost=False, start=None, end=yesterdayobj(), rendered=True
):
    """
    visualization giving the average cost line together with netvalue line as well as buy and sell points

    :returns: pyecharts.line
    """
    funddata = []
    costdata = []
    pprice = self.price[self.price["date"] <= end]
    pcftable = cftable
    if start is not None:
        pprice = pprice[pprice["date"] >= start]
        pcftable = pcftable[pcftable["date"] >= start]
    for _, row in pprice.iterrows():
        date = row["date"]
        funddata.append(row["netvalue"])
        if unitcost:
            cost = 0
            if (date - self.cftable.iloc[0].date).days >= 0:
                cost = self.unitcost(date)
            costdata.append(cost)

    coords = []
    # pcftable = pcftable[abs(pcftable["cash"]) > threhold]
    for i, r in pcftable.iterrows():
        if r.cash != 0:
            coords.append(
                [r.date, pprice[pprice["date"] <= r.date].iloc[-1]["netvalue"]]
            )

    upper = pcftable.cash.abs().max()
    lower = pcftable.cash.abs().min()
    if upper == lower:
        upper = 2 * lower + 1  # avoid zero in denominator

    def marker_factory(x, y):
        buy = pcftable[pcftable["date"] <= x].iloc[-1]["cash"]
        if buy < 0:
            color = "#ff7733"
        else:

            color = "#3366ff"
        size = (abs(buy) - lower) / (upper - lower) * 5 + 5
        return opts.MarkPointItem(
            coord=[x.date(), y],
            itemstyle_opts=opts.ItemStyleOpts(color=color),
            # this nested itemstyle_opts within MarkPointItem is only supported for pyechart>1.7.1
            symbol="circle",
            symbol_size=size,
        )

    line = Line()

    line.add_xaxis([d.date() for d in pprice.date])

    if unitcost:
        line.add_yaxis(
            series_name="持仓成本",
            y_axis=costdata,
            is_symbol_show=False,
        )
    line.add_yaxis(
        series_name="基金净值",
        y_axis=funddata,
        is_symbol_show=False,
        markpoint_opts=opts.MarkPointOpts(
            data=[marker_factory(*c) for c in coords],
        ),
    )
    line.set_global_opts(
        datazoom_opts=[
            opts.DataZoomOpts(
                is_show=True, type_="slider", range_start=50, range_end=100
            ),
            opts.DataZoomOpts(
                is_show=True,
                type_="slider",
                orient="vertical",
                range_start=50,
                range_end=100,
            ),
        ],
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            trigger="axis",
            trigger_on="mousemove",
            axis_pointer_type="cross",
        ),
    )
    if rendered:
        return line.render_notebook()
    else:
        return line


class trade:
    """
    Trade class with fundinfo obj as input and its main attrs are cftable and remtable:

        1. cftable: pd.Dataframe, 现金流量表，每行为不同变更日期，三列分别为 date，cash， share，标记对于某个投资标的
        现金的进出和份额的变化情况，所有的份额数据为交易当时的不复权数据。基金份额折算通过流量表中一次性的份额增减体现。

        2. remtable：pd.Dataframe, 持仓情况表，每行为不同变更日期，两列分别为 date 和 rem， rem 数据结构是一个嵌套的列表，
        包含了不同时间买入仓位的剩余情况，详情参见 remain 模块。这一表格如非必需，避免任何直接调用。

    :param infoobj: info object as the trading aim
    :param status: status table, obtained from record class
    """

    def __init__(self, infoobj, status, cftable=None, remtable=None):
        self.aim = infoobj
        code = self.aim.code
        self.code = code
        self.name = self.aim.name
        self.price = self.aim.price
        if (cftable is not None and remtable is None) or (
            cftable is None and remtable is not None
        ):
            raise ValueError(
                "You must provide both `cftable` and `remtable` for incremental trade engine"
            )
        # 请确保提供的 cftable 和 remtable 在日期，份额等数据上是匹配的
        if cftable is None:
            self.cftable = pd.DataFrame([], columns=["date", "cash", "share"])
        else:
            self.cftable = cftable
        if remtable is None:
            self.remtable = pd.DataFrame([], columns=["date", "rem"])
        else:
            self.remtable = remtable
        self.status = status.loc[:, ["date", code]]
        self.status = self.status[self.status[code] != 0]
        self._arrange()

    def _arrange(self):
        self.recorddate_set = set(self.status.date)
        while 1:
            try:
                self._addrow()
            except Exception as e:
                if e.args[0] == "no other info to be add into cashflow table":
                    break
                else:
                    raise e

    def _addrow(self):
        """
        Return cashflow table with one more line or raise an exception if there is no more line to add
        The same logic also applies to rem table
        关于对于一个基金多个操作存在于同一交易日的说明：无法处理历史买入第一笔同时是分红日的情形, 事实上也不存在这种情形。无法处理一日多笔买卖的情形。
        同一日既有卖也有买不现实，多笔买入只能在 csv 上合并记录，由此可能引起份额计算 0.01 的误差。可以处理分红日买入卖出的情形。
        分级份额折算日封闭无法买入，所以程序直接忽略当天的买卖。因此不会出现多个操作共存的情形。
        """
        # the design on data remtable is disaster, it is very dangerous though works now
        # possibly failing cases include:
        # 买卖日记录是节假日，而顺延的日期恰好是折算日（理论上无法申赎）或分红日（可能由于 date 和 rdate 的错位而没有考虑到），
        # 又比如周日申购记录，周一申购记录，那么周日记录会现金流记在周一，继续现金流标更新将从周二开始，周一数据被丢弃
        code = self.aim.code
        if len(self.cftable) == 0:
            if len(self.status[self.status[code] != 0]) == 0:
                raise Exception("no other info to be add into cashflow table")
            i = 0
            while self.status.iloc[i].loc[code] == 0:
                i += 1
            value = self.status.iloc[i].loc[code]
            date = self.status.iloc[i].date
            self.lastdate = date
            if len(self.price[self.price["date"] >= date]) > 0:
                date = self.price[self.price["date"] >= date].iloc[0]["date"]
            else:
                date = self.price[self.price["date"] <= date].iloc[-1]["date"]

            # 这里没有像下边部分一样仔细处理单独的 lastdate，hopefully 不会出现其他奇怪的问题，有 case 再说
            # https://github.com/refraction-ray/xalpha/issues/47
            # 凭直觉这个地方的处理很可能还有其他 issue

            if value > 0:
                feelabel = 100 * value - int(100 * value + 1e-6)
                if round(feelabel, 1) == 0.5:
                    # binary encoding, 10000.005 is actually 10000.0050...1, see issue #59
                    feelabel = feelabel - 0.5
                    if abs(feelabel) < 1e-4:
                        feelabel = 0
                    else:
                        feelabel *= 100
                else:
                    feelabel = None
                value = int(value * 100 + 1e-6) / 100
                assert feelabel is None or feelabel >= 0.0, "自定义申购费必须为正值"
                rdate, cash, share = self.aim.shengou(value, date, fee=feelabel)
                rem = rm.buy([], share, rdate)
            else:
                raise TradeBehaviorError("You cannot sell first when you never buy")
        elif len(self.cftable) > 0:
            # recorddate = list(self.status.date)
            if not getattr(self, "lastdate", None):
                lastdate = self.cftable.iloc[-1].date + pd.Timedelta(1, unit="d")
            else:
                lastdate = self.lastdate + pd.Timedelta(1, unit="d")
            while (lastdate not in self.aim.specialdate) and (
                (lastdate not in self.recorddate_set)
                or (
                    (lastdate in self.recorddate_set)
                    and (
                        self.status[self.status["date"] == lastdate].loc[:, code].any()
                        == 0
                    )
                )
            ):
                lastdate += pd.Timedelta(1, unit="d")
                if (lastdate - yesterdayobj()).days >= 1:
                    raise Exception("no other info to be add into cashflow table")
            if (lastdate - yesterdayobj()).days >= 1:
                raise Exception("no other info to be add into cashflow table")
            date = lastdate
            # 无净值日优先后移，无法后移则前移
            # 还是建议日期记录准确，不然可能有无法完美兼容的错误出现
            if len(self.price[self.price["date"] >= date]) > 0:
                date = self.price[self.price["date"] >= date].iloc[0]["date"]
            else:
                date = self.price[self.price["date"] <= date].iloc[-1]["date"]
            if date != lastdate and date in list(self.status.date):
                # 日期平移到了其他记录日，很可能出现问题!
                logger.warning(
                    "账单日期 %s 非 %s 的净值记录日期，日期智能平移后 %s 与账单其他日期重合！交易处理极可能出现问题！！ "
                    "靠后日期的记录被覆盖" % (lastdate, self.code, date)
                )
            self.lastdate = lastdate
            if date > lastdate:
                self.lastdate = date
            # see https://github.com/refraction-ray/xalpha/issues/27, begin new date from last one in df is not reliable
            label = self.aim.dividend_label  # 现金分红 0, 红利再投 1
            cash = 0
            share = 0
            rem = self.remtable.iloc[-1].rem
            rdate = date
            if (lastdate in self.recorddate_set) and (date not in self.aim.zhesuandate):
                # deal with buy and sell and label the fenhongzaitouru, namely one label a 0.05 in the original table to label fenhongzaitouru
                value = self.status[self.status["date"] <= lastdate].iloc[-1].loc[code]
                if date in self.aim.fenhongdate:  # 0.05 的分红行为标记，只有分红日才有效
                    fenhongmark = round(10 * value - int(10 * value), 1)
                    # TODO: any rounding issue here for th int
                    if fenhongmark == 0.5 and label == 0:
                        label = 1  # fenhong reinvest
                        value = value - math.copysign(0.05, value)
                    elif fenhongmark == 0.5 and label == 1:
                        label = 0
                        value = value - math.copysign(0.05, value)

                if value > 0:  # value stands for purchase money
                    feelabel = 100 * value - int(100 * value + 1e-6)

                    if int(10 * feelabel + 1e-6) == 5:
                        feelabel = (feelabel - 0.5) * 100
                    else:
                        feelabel = None
                    value = int(value * 100 + 1e-6) / 100
                    rdate, dcash, dshare = self.aim.shengou(
                        value, date, fee=feelabel
                    )  # shengou fee is in the unit of percent, different than shuhui case
                    rem = rm.buy(rem, dshare, rdate)

                elif value < -0.005:  # value stands for redemp share
                    feelabel = int(100 * value - 1e-6) - 100 * value
                    if int(10 * feelabel + 1e-6) == 5:
                        feelabel = feelabel - 0.5
                    else:
                        feelabel = None
                    value = int(value * 100 - 1e-6) / 100
                    rdate, dcash, dshare = self.aim.shuhui(
                        -value, date, self.remtable.iloc[-1].rem, fee=feelabel
                    )
                    _, rem = rm.sell(rem, -dshare, rdate)
                elif value >= -0.005 and value < 0:
                    # value now stands for the ratio to be sold in terms of remain positions, -0.005 stand for sell 100%
                    remainshare = sum(
                        self.cftable[self.cftable["date"] <= date].loc[:, "share"]
                    )
                    ratio = -value / 0.005
                    rdate, dcash, dshare = self.aim.shuhui(
                        remainshare * ratio, date, self.remtable.iloc[-1].rem, 0
                    )
                    _, rem = rm.sell(rem, -dshare, rdate)
                else:  # in case value=0, when specialday is in record day
                    rdate, dcash, dshare = date, 0, 0

                cash += dcash
                share += dshare
            if date in self.aim.specialdate:  # deal with fenhong and xiazhe
                comment = self.price[self.price["date"] == date].iloc[0].loc["comment"]
                if isinstance(comment, float):
                    if comment < 0:
                        dcash2, dshare2 = (
                            0,
                            sum([myround(sh * (-comment - 1)) for _, sh in rem]),
                        )  # xiazhe are seperately carried out based on different purchase date
                        rem = rm.trans(rem, -comment, date)
                        # myround(sum(cftable.loc[:,'share'])*(-comment-1))
                    elif comment > 0 and label == 0:
                        dcash2, dshare2 = (
                            myround(sum(self.cftable.loc[:, "share"]) * comment),
                            0,
                        )
                        rem = rm.copy(rem)

                    elif comment > 0 and label == 1:
                        dcash2, dshare2 = (
                            0,
                            myround(
                                sum(self.cftable.loc[:, "share"])
                                * (
                                    comment
                                    / self.price[self.price["date"] == date]
                                    .iloc[0]
                                    .netvalue
                                )
                            ),
                        )
                        rem = rm.buy(rem, dshare2, date)

                    cash += dcash2
                    share += dshare2
                else:
                    raise ParserFailure("comments not recognized")

        self.cftable = self.cftable.append(
            pd.DataFrame([[rdate, cash, share]], columns=["date", "cash", "share"]),
            ignore_index=True,
        )
        self.remtable = self.remtable.append(
            pd.DataFrame([[rdate, rem]], columns=["date", "rem"]), ignore_index=True
        )

    def xirrrate(self, date=yesterdayobj(), startdate=None, guess=0.01):
        """
        give the xirr rate for all the trade of the aim before date (virtually sold out on date)

        :param date: string or obj of datetime, the virtually sell-all date
        :param startdate: string or obj of datetime, the beginning date of calculation, default from first buy
        """
        return xirrcal(self.cftable, [self], date, startdate, guess)

    def dailyreport(self, date=yesterdayobj()):
        date = convert_date(date)
        partcftb = self.cftable[self.cftable["date"] <= date]
        value = self.get_netvalue(date)

        if len(partcftb) == 0:
            reportdict = {
                "基金名称": [self.name],
                "基金代码": [self.code],
                "当日净值": [value],
                "持有份额": [0],
                "基金现值": [0],
                "基金总申购": [0],
                "历史最大占用": [0],
                "基金分红与赎回": [0],
                "基金收益总额": [0],
            }
            df = pd.DataFrame(reportdict, columns=reportdict.keys())
            return df
        # totinput = myround(-sum(partcftb.loc[:,'cash']))
        totinput = myround(
            -sum([row["cash"] for _, row in partcftb.iterrows() if row["cash"] < 0])
        )
        totoutput = myround(
            sum([row["cash"] for _, row in partcftb.iterrows() if row["cash"] > 0])
        )

        currentshare = myround(sum(partcftb.loc[:, "share"]))
        currentcash = myround(currentshare * value)
        btnk = bottleneck(partcftb)
        turnover = turnoverrate(partcftb, date)
        ereturn = myround(currentcash + totoutput - totinput)
        if currentshare == 0:
            unitcost = 0
        else:
            unitcost = round((totinput - totoutput) / currentshare, 4)
        if btnk == 0:
            returnrate = 0
        else:
            returnrate = round((ereturn / btnk) * 100, 4)

        reportdict = {
            "基金名称": [self.name],
            "基金代码": [self.code],
            "当日净值": [value],
            "单位成本": [unitcost],
            "持有份额": [currentshare],
            "基金现值": [currentcash],
            "基金总申购": [totinput],
            "历史最大占用": [btnk],
            "基金持有成本": [totinput - totoutput],
            "基金分红与赎回": [totoutput],
            "换手率": [turnover],
            "基金收益总额": [ereturn],
            "投资收益率": [returnrate],
        }
        df = pd.DataFrame(reportdict, columns=reportdict.keys())
        return df

    def get_netvalue(self, date=yesterdayobj()):
        df = self.price[self.price["date"] <= date]
        if df is None or len(df) == 0:
            return 0
        return df.iloc[-1].netvalue

    def briefdailyreport(self, date=yesterdayobj()):
        """
        quick summary of highly used attrs for trade

        :param date: string or object of datetime
        :returns: dict with several attrs: date, unitvalue, currentshare, currentvalue
        """
        date = convert_date(date)
        partcftb = self.cftable[self.cftable["date"] <= date]
        if len(partcftb) == 0:
            return {}

        unitvalue = self.get_netvalue(date)
        currentshare = myround(sum(partcftb.loc[:, "share"]))
        currentvalue = myround(currentshare * unitvalue)

        return {
            "date": date,
            "unitvalue": unitvalue,
            "currentshare": currentshare,
            "currentvalue": currentvalue,
        }

    def unitcost(self, date=yesterdayobj()):
        """
        give the unitcost of fund positions

        :param date: string or object of datetime
        :returns: float number of unitcost
        """
        partcftb = self.cftable[self.cftable["date"] <= date]
        if len(partcftb) == 0:
            return 0
        totnetinput = myround(-sum(partcftb.loc[:, "cash"]))
        currentshare = self.briefdailyreport(date).get("currentshare", 0)
        # totnetinput
        if currentshare > 0:
            unitcost = totnetinput / currentshare
        else:
            unitcost = 0
        return unitcost

    def v_tradevolume(self, freq="D", rendered=True):
        """
        visualization on trade summary

        :param freq: string, "D", "W" and "M" are supported
        :returns: pyecharts.charts.bar.render_notebook()
        """
        return vtradevolume(self.cftable, freq=freq, rendered=rendered)

    def v_tradecost(self, start=None, end=yesterdayobj(), rendered=True):
        """
        visualization giving the average cost line together with netvalue line

        :returns: pyecharts.line
        """
        return vtradecost(
            self, self.cftable, unitcost=True, start=start, end=end, rendered=rendered
        )

    def v_totvalue(self, end=yesterdayobj(), rendered=True, vopts=None):
        """
        visualization on the total values daily change of the aim
        """
        partp = self.price[self.price["date"] >= self.cftable.iloc[0].date]
        # 多基金账单时起点可能非该基金持有起点
        partp = partp[partp["date"] <= end]

        date = [d.date() for d in partp.date]
        valuedata = [
            self.briefdailyreport(d).get("currentvalue", 0) for d in partp.date
        ]

        line = Line()
        if vopts is None:
            vopts = line_opts

        line.add_xaxis(date)
        line.add_yaxis(series_name="持仓总值", y_axis=valuedata, is_symbol_show=False)
        line.set_global_opts(**vopts)
        if rendered:
            return line.render_notebook()
        else:
            return line

    def __repr__(self):
        return self.name + " 交易情况"


"""
可视化图的合并可参考以下代码 v0.5.5
from pyecharts import Overlap
overlap = Overlap()
overlap.add(self.v_tradecost())
overlap.add(self.v_tradevolume(bar_category_gap='95%'), yaxis_index=1,is_add_yaxis=True)
overlap
"""


class itrade(trade):
    """
    场内交易，只包含 cftable 现金流表
    """

    def __init__(self, code, status, name=None):
        """

        :param code: str. 代码格式与 :func:`xalpha.universal.get_daily` 要求相同
        :param status: 记账单或 irecord 类。
        :param name: Optional[str]. 可提供标的名称。
        """
        self.code = code
        if isinstance(status, irecord):
            self.status = status.filter(code)
        else:
            self.status = status[status.code == code]
        # self.cftable = pd.DataFrame([], columns=["date", "cash", "share"])
        try:
            self.price = xu.get_daily(
                self.code, start=self.status.iloc[0]["date"].strftime("%Y-%m-%d")
            )
            self.price["netvalue"] = self.price["close"]
        except Exception as e:
            logger.warning(
                "%s when trade trying to get daily price of %s" % (e, self.code)
            )
            self.price = None
        self._arrange()
        if not name:
            try:
                self.name = get_rt(code)["name"]
            except:
                self.name = code
        self.type_ = None

    def get_type(self):
        if not self.type_:
            code = self.code
            if (
                code.startswith("SZ15900")
                or code.startswith("SH5116")
                or code.startswith("SH5117")
                or code.startswith("SH5118")
                or code.startswith("SH5119")
                or code.startswith("SH5198")
            ):
                self.type_ = "货币基金"
            elif (
                code.startswith("SH5")
                or code.startswith("SZ16")
                or code.startswith("SZ159")
            ):
                self.type_ = "场内基金"
            elif code.startswith("SH11") or code.startswith("SZ12"):
                if self.name.endswith("转债") or self.name.endswith("转2"):
                    self.type_ = "可转债"
                else:
                    self.type_ = "债券"
            elif code.startswith("SZ399") or code.startswith("SH000"):
                self.type_ = "指数"

            elif (
                code.startswith("SH60")
                or code.startswith("SZ00")
                or code.startswith("SZ20")
                or code.startswith("SZ30")
            ):
                self.type_ = "股票"
            else:
                self.type_ = "其他"

        return self.type_

    def _arrange(self):
        d = {"date": [], "cash": [], "share": []}
        for _, r in self.status.iterrows():
            d["date"].append(r.date)

            if r.share == 0:
                d["cash"].append(-r.value)
                d["share"].append(0)
            else:
                if r.value < 0:
                    r.value = xu.get_daily(
                        self.code, end=r.date.strftime("%Y-%m-%d"), prev=15
                    ).iloc[-1]["close"]
                if r.value == 0:
                    d["cash"].append(0)
                    d["share"].append(r.share)  # 直接记录总的应增加+或减少的份额数
                else:
                    d["cash"].append(-r.value * r.share - abs(r.fee))  # 手续费总是正的，和买入同号
                    d["share"].append(r.share)
        self.cftable = pd.DataFrame(d)

    def get_netvalue(self, date=yesterdayobj()):
        if self.price is None:
            return 0
        df = self.price[self.price["date"] <= date]
        if len(df) > 0:
            return df.iloc[-1].close
        else:
            return 0


Trade = trade
ITrade = itrade
