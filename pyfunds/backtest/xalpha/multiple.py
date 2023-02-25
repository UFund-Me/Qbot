# -*- coding: utf-8 -*-
"""
module for mul and mulfix class: fund combination management
"""

import logging
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, ThemeRiver

from xalpha.cons import convert_date, myround, yesterdaydash, yesterdayobj
from xalpha.evaluate import evaluate
from xalpha.exceptions import FundTypeError, TradeBehaviorError
from xalpha.record import record, irecord
from xalpha.indicator import indicator
from xalpha.info import cashinfo, fundinfo, mfundinfo, get_fund_holdings
from xalpha.trade import (
    bottleneck,
    trade,
    turnoverrate,
    vtradevolume,
    xirrcal,
    itrade,
    vtradecost,
)
from xalpha.universal import get_fund_type, ttjjcode, get_rt, get_industry_fromxq
import xalpha.universal as xu


logger = logging.getLogger(__name__)


class mul:
    """
    multiple fund positions manage class

    :param fundtradeobj: list of trade obj which you want to analyse together
    :param status: the status table of trade, all code in this table would be considered.
            one must provide one of the two paramters, if both are offered, status will be overlooked
            可以是场内记账单 DataFrame，也可以是 record 对象。
    :param istatus: 场内交易账单，也可以是 irecord 对象。
            若提供，则场内外交易联合统计展示。该选项只保证 ``combsummary`` 方法可正常使用，不保证 ``mul`` 类的其他方法可用。
    :param property: Dict[fundcode, property_number]. property number 的解释：
            int. 1: 基金申购采取分位以后全舍而非四舍五入（这种基金是真实存在的==）。2：基金默认分红再投入（0 则是默认现金分红）。4：基金赎回按净值处理（暂时只支持货币基金，事实上无法精确支持按份额赎回的净值型基金）。将想要的性质数值相加即可，类似 *nix 上的 xwr 系统。
    :param fetch: boolean, when open the fetch option, info class will try fetching from local files first in the init
    :param save: boolean, when open the save option, info classes automatically save the class to files
    :param path: string, the file path prefix of IO, or object or engine from sqlalchemy to connect sql database
    :param form: string, the format of IO, options including: 'csv','sql'
    """

    def __init__(
        self,
        *fundtradeobj,
        status=None,
        istatus=None,
        property=None,
        fetch=False,
        save=False,
        path="",
        form="csv"
    ):
        if isinstance(status, record):
            if not property:
                property = getattr(status, "property", {})
            status = status.status
        elif not property:
            property = {}
        self.is_in = False
        if fundtradeobj:
            fundtradeobj = list(fundtradeobj)
            for t in fundtradeobj:
                if isinstance(t, itrade):
                    self.is_in = True
                break
        else:
            fundtradeobj = []
            # warning: not a very good way to automatic generate these fund obj
            # because there might be some funds use round_down for share calculation, ie, label=2 must be given
            # unless you are sure corresponding funds are added to the droplist
        fundcodelist = [f.code for f in fundtradeobj]
        if status is not None:
            for code in status.columns:
                if code == "date" or code.startswith("#"):
                    continue
                # r1, d2, v4 p = r+d+v
                if code in fundcodelist:
                    continue
                p = property.get(code, 0)
                round_label = p % 2
                dividend_label = ((p - round_label) / 2) % 2
                value_label = ((p - round_label - dividend_label) / 4) % 2
                try:
                    fundtradeobj.append(
                        trade(
                            fundinfo(
                                code,
                                round_label=round_label,
                                dividend_label=dividend_label,
                                fetch=fetch,
                                save=save,
                                path=path,
                                form=form,
                            ),
                            status,
                        )
                    )
                except FundTypeError:
                    fundtradeobj.append(
                        trade(
                            mfundinfo(
                                code,
                                round_label=round_label,
                                value_label=value_label,
                                fetch=fetch,
                                save=save,
                                path=path,
                                form=form,
                            ),
                            status,
                        )
                    )
        if istatus is not None:
            self.is_in = True
            if isinstance(istatus, irecord):
                istatus = istatus.status
            for code in istatus.code.unique():
                if code not in fundcodelist and not code.startswith("#"):
                    fundtradeobj.append(itrade(code, istatus))
        self.fundtradeobj = tuple(fundtradeobj)
        self.totcftable = self._mergecftb()

    def tot(self, prop="基金现值", date=yesterdayobj()):
        """
        sum of all the values from one prop of fund daily report,
        of coures many of the props make no sense to sum

        :param prop: string defined in the daily report dict,
            typical one is 'currentvalue' or 'originalpurchase'
        """
        res = 0
        for fund in self.fundtradeobj:
            res += fund.dailyreport(date).iloc[0][prop]
        return res

    def combsummary(self, date=yesterdayobj()):
        """
        brief report table of every funds and the combination investment

        :param date: string or obj of date, show info of the date given
        :returns: empty dict if nothing is remaining that date
            dict of various data on the trade positions
        """
        date = convert_date(date)
        columns = [
            "基金名称",
            "基金代码",
            "当日净值",
            "单位成本",
            "持有份额",
            "基金现值",
            "基金总申购",
            "历史最大占用",
            "基金持有成本",
            "基金分红与赎回",
            "换手率",
            "基金收益总额",
            "投资收益率",
        ]
        summarydf = pd.DataFrame([], columns=columns)
        for fund in self.fundtradeobj:
            summarydf = summarydf.append(
                fund.dailyreport(date), ignore_index=True, sort=True
            )
        tname = "总计"
        tcode = "total"
        tunitvalue = float("NaN")
        tunitcost = float("NaN")
        tholdshare = float("NaN")
        tcurrentvalue = summarydf["基金现值"].sum()
        tpurchase = summarydf["基金总申购"].sum()
        tbtnk = bottleneck(self.totcftable[self.totcftable["date"] <= date])
        tcost = summarydf["基金持有成本"].sum()
        toutput = summarydf["基金分红与赎回"].sum()
        tturnover = turnoverrate(self.totcftable[self.totcftable["date"] <= date], date)
        # 计算的是总系统作为整体和外界的换手率，而非系统各成分之间的换手率
        tearn = summarydf["基金收益总额"].sum()
        trate = round(tearn / tbtnk * 100, 4)
        trow = pd.DataFrame(
            [
                [
                    tname,
                    tcode,
                    tunitvalue,
                    tunitcost,
                    tholdshare,
                    tcurrentvalue,
                    tpurchase,
                    tbtnk,
                    tcost,
                    toutput,
                    tturnover,
                    tearn,
                    trate,
                ]
            ],
            columns=columns,
        )
        summarydf = summarydf.append(trow, ignore_index=True, sort=True)

        return summarydf[columns].sort_values(by="基金现值", ascending=False)

    summary = combsummary

    def _mergecftb(self):
        """
        merge the different cftable for different funds into one table
        """
        dtlist = []
        for fund in self.fundtradeobj:
            dtlist2 = []
            for _, row in fund.cftable.iterrows():
                dtlist2.append((row["date"], row["cash"]))
            dtlist.extend(dtlist2)

        nndtlist = set([item[0] for item in dtlist])
        nndtlist = sorted(list(nndtlist), key=lambda x: x)
        reslist = []
        for date in nndtlist:
            reslist.append(sum([item[1] for item in dtlist if item[0] == date]))
        df = pd.DataFrame(data={"date": nndtlist, "cash": reslist})
        df = df[df["cash"] != 0]
        df = df.reset_index(drop=True)
        return df

    def xirrrate(self, date=yesterdayobj(), startdate=None, guess=0.01):
        """
        xirr rate evauation of the whole invest combination

        :param date: string or obj of datetime, the virtually sell-all date
        :param startdate: string or obj of datetime, the beginning date of calculation, default from first buy
        """
        return xirrcal(self.totcftable, self.fundtradeobj, date, startdate, guess)

    def evaluation(self, start=None):
        """
        give the evaluation object to analysis funds properties themselves instead of trades

        :returns: :class:`xalpha.evaluate.evaluate` object, with referenced funds the same as funds
            we invested
        """
        if self.is_in:
            raise NotImplementedError()
        case = evaluate(
            *[fundtrade.aim for fundtrade in self.fundtradeobj], start=start
        )
        return case

    def get_stock_holdings(
        self, year=None, season=None, date=yesterdayobj(), threhold=100
    ):
        """
        获取整个基金组合的底层股票持仓总和和细节，组合穿透

        :param year: 基于的基金季报年份
        :param season: 基于的基金季报季度
        :param date: 默认昨天
        :param threhold: 默认100。小于100元的底层股票将不在最后的结果中展示
        :return: pd.DataFrame column: name, code, value, ratio
        """
        d = {}
        if year is None or season is None:
            rd = convert_date(date) - pd.Timedelta(days=120)
            if not year:
                year = rd.year
            if not season:
                season = int((rd.month - 0.1) / 3) + 1
            logger.debug("use %s, %s for fund report" % (year, season))
        for f in self.fundtradeobj:
            if isinstance(f, itrade):
                if f.get_type() == "股票":
                    code = f.code
                elif f.get_type() == "场内基金":
                    code = f.code[2:]
                else:
                    continue
            else:
                code = f.code
            value = f.briefdailyreport(date).get("currentvalue", 0)
            if value > 0:
                if code.startswith("SH") or code.startswith("SZ"):
                    stock = code
                    d[stock] = d.get(stock, 0) + value
                elif code == "mf":
                    continue
                else:
                    df = get_fund_holdings(code, year, season)
                    if df is None:
                        continue

                    for _, row in df.iterrows():
                        stock = row["code"]
                        stock = ttjjcode(stock)
                        d[stock] = d.get(stock, 0) + row["ratio"] / 100 * value
                        # print("%s has %s contribution from %s" %(stock, row["ratio"] / 100 * value, f.name))

        l = []
        for code, value in sorted(d.items(), key=lambda item: -item[1]):
            if value >= threhold:
                try:
                    name = get_rt(code)["name"]
                except:
                    name = code
                l.append([name, code, value])
        fdf = pd.DataFrame(l, columns=["name", "code", "value"])
        fdf["ratio"] = fdf["value"] / fdf["value"].sum()
        return fdf

    def get_portfolio(self, date=yesterdayobj()):
        """
        获取基金组合底层资产大类配置的具体值

        :param date:
        :return: Dict[str, float]. stock，bond，cash 对应总值的字典
        """

        d = {"stock": 0, "bond": 0, "cash": 0}
        date = convert_date(date)
        for f in self.fundtradeobj:
            value = f.briefdailyreport(date).get("currentvalue", 0)
            if value > 0:
                if isinstance(f, itrade):
                    if f.get_type() == "股票":
                        d["stock"] += value
                        continue
                    elif f.get_type() in ["可转债", "债券"]:
                        d["bond"] += value
                        continue
                    elif f.get_type() == "货币基金":
                        d["cash"] += value
                        continue
                    elif f.get_type() == "场内基金":
                        code = f.code[2:]
                    else:
                        continue
                else:
                    code = f.code
                if code == "mf":
                    d["cash"] += value
                    continue
                if get_fund_type(code) == "货币基金":
                    d["cash"] += value
                    continue
                df = xu.get_daily("pt-F" + code, end=date.strftime("%Y%m%d"))
                if df is None or len(df) == 0:
                    logger.warning("empty portfolio info for %s" % code)
                row = df.iloc[-1]
                if row["bond_ratio"] + row["stock_ratio"] < 10:  # 联接基金
                    d["stock"] += (
                        (100 - row["bond_ratio"] - row["cash_ratio"]) * value / 100
                    )
                    d["bond"] += row["bond_ratio"] * value / 100
                    d["cash"] += row["cash_ratio"] * value / 100
                else:
                    d["stock"] += row["stock_ratio"] * value / 100
                    d["bond"] += row["bond_ratio"] * value / 100
                    d["cash"] += row["cash_ratio"] * value / 100
        return d

    get_portfolio_holdings = get_portfolio

    def get_industry(self, date=yesterdayobj()):
        """
        获取基金组合持仓的行业占比信息，底层为非 A 股持仓的暂不支持

        :param date:
        :return: Dict
        """
        # TODO: hard coded 一个字典来合并一些二级行业
        d = {}
        date = convert_date(date)
        rd = date - pd.Timedelta(days=120)
        year = rd.year
        season = int((rd.month - 0.1) / 3) + 1
        for f in self.fundtradeobj:
            value = f.briefdailyreport(date).get("currentvalue", 0)
            if value > 0:
                if isinstance(f, itrade):
                    if f.get_type() == "股票":
                        industry = get_industry_fromxq(f.code).get("industryname", "")
                        if industry.strip():
                            d[industry] = d.get(industry, 0) + value
                        continue
                    elif f.get_type() in ["可转债", "债券", "货币基金"]:
                        # 现在简化实现可转债暂时不按正股记行业
                        continue
                    elif f.get_type() == "场内基金":
                        code = f.code[2:]
                    else:
                        continue
                else:
                    code = f.code
                if code == "mf":
                    continue
                if get_fund_type(code) == "货币基金":
                    continue
                ## 以下为持有股票的基金处理
                ## fundinfo 有点浪费，不过简化实现暂时如此
                fobj = fundinfo(code)
                industry_dict = fobj.get_industry_holdings(year=year, season=season)
                if industry_dict is None:
                    continue
                ## 这里行业占比需要做个 scaling
                sv = sum([v for _, v in industry_dict.items()])
                if sv < 1.0:
                    # 只有极少数持仓存在行业信息
                    continue
                stock_ratio = fobj.get_portfolio_holdings(date.strftime("%Y%m%d"))[
                    "stock_ratio"
                ]
                scale = stock_ratio / sv
                for k, v in industry_dict.items():
                    if k.strip():
                        d[k] = d.get(k, 0) + value * v / 100 * scale
        return d

    get_industry_holdings = get_industry

    def v_positions(self, date=yesterdayobj(), rendered=True):
        """
        pie chart visualization of positions ratio in combination
        """
        sdata = sorted(
            [
                (fob.name, fob.briefdailyreport(date).get("currentvalue", 0))
                for fob in self.fundtradeobj
            ],
            key=lambda x: x[1],
            reverse=True,
        )
        pie = Pie()
        pie.add(
            series_name="总值占比",
            data_pair=sdata,
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        ).set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_left="left", type_="scroll", orient="vertical"
            )
        ).set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
        )

        if rendered:
            return pie.render_notebook()
        else:
            return pie

    def v_category_positions(self, date=yesterdayobj(), rendered=True):
        """
        资产分类扇形图，按大类资产求和绘制

        :param date:
        :param rendered: bool. default true for notebook, for plain pyechart obj to return, set rendered=False
        :return:
        """
        d = {}
        for f in self.fundtradeobj:
            if isinstance(f, itrade):
                t = f.get_type()
                if t == "场内基金":
                    t = get_fund_type(f.code[2:])
            elif f.code == "mf":
                t = "货币基金"
            else:
                t = get_fund_type(f.code)
            if t == "其他":
                logger.warning(
                    "%s has category others which should be double checked" % f.code
                )
            d[t] = d.get(t, 0) + f.briefdailyreport(date).get("currentvalue", 0)

        sdata = sorted([(k, round(v, 2)) for k, v in d.items()])
        pie = Pie()
        pie.add(
            series_name="总值占比",
            data_pair=sdata,
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        ).set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_left="left", type_="scroll", orient="vertical"
            )
        ).set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
        )

        if rendered:
            return pie.render_notebook()
        else:
            return pie

    def v_positions_history(self, end=yesterdaydash(), rendered=True):
        """
        river chart visulization of positions ratio history
        use text size to avoid legend overlap in some sense, eg. legend_text_size=8
        """
        start = self.totcftable.iloc[0].date
        times = pd.date_range(start, end)
        tdata = []
        for date in times:
            sdata = sorted(
                [
                    (
                        date,
                        fob.briefdailyreport(date).get("currentvalue", 0),
                        fob.name,
                    )
                    for fob in self.fundtradeobj
                ],
                key=lambda x: x[1],
                reverse=True,
            )
            tdata.extend(sdata)

        tr = ThemeRiver()
        tr.add(
            series_name=[foj.name for foj in self.fundtradeobj],
            data=tdata,
            label_opts=opts.LabelOpts(is_show=False),
            singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="10%"),
        )
        if rendered:
            return tr.render_notebook()
        else:
            return tr

    def v_tradevolume(self, freq="D", rendered=True):
        """
        visualization on trade summary of the funds combination

        :param freq: one character string, frequency label, now supporting D for date,
            W for week and M for month, namely the trade volume is shown based on the time unit
        :returns: ``pyecharts.Bar()``
        """
        return vtradevolume(self.totcftable, freq=freq, rendered=rendered)


class mulfix(mul, indicator):
    """
    introduce cash to make a closed investment system, where netvalue analysis can be applied
    namely the totcftable only has one row at the very beginning

    :param fundtradeobj: trade obj to be include
    :param status: status table,  if no trade obj is provided, it will include all fund
            based on code in status table
    :param property: Dict[fundcode, property_number]. property number 的解释：
            int. 1: 基金申购采取分位以后全舍而非四舍五入（这种基金是真实存在的==）。2：基金默认分红再投入（0 则是默认现金分红）。4：基金赎回按净值
    :param fetch: boolean, when open the fetch option, info class will try fetching from local files first in the init
    :param save: boolean, when open the save option, info classes automatically save the class to files
    :param path: string, the file path prefix of IO, or object or engine from sqlalchemy to connect sql database
    :param form: string, the format of IO, options including: 'csv','sql'
    :param totmoney: positive float, the total money as the input at the beginning
    :param cashobj: cashinfo object, which is designed to balance the cash in and out
    """

    def __init__(
        self,
        *fundtradeobj,
        status=None,
        istatus=None,
        property=None,
        fetch=False,
        save=False,
        path="",
        form="csv",
        totmoney=100000,
        cashobj=None
    ):
        super().__init__(
            *fundtradeobj,
            status=status,
            istatus=istatus,
            property=property,
            fetch=fetch,
            save=save,
            path=path,
            form=form
        )
        if cashobj is None:
            cashobj = cashinfo()
        self.totmoney = totmoney
        nst = mulfix._vcash(totmoney, self.totcftable, cashobj)
        cashtrade = trade(cashobj, nst)
        # 		 super().__init__(*self.fundtradeobj, cashtrade)
        self.cashobj = cashobj
        self.fundtradeobj = list(self.fundtradeobj)
        self.fundtradeobj.append(cashtrade)
        self.fundtradeobj = tuple(self.fundtradeobj)
        btnk = bottleneck(self.totcftable)
        if btnk > totmoney:
            raise TradeBehaviorError("the initial total cash is too low")
        self.totcftable = pd.DataFrame(
            data={"date": [nst.iloc[0].date], "cash": [-totmoney]}
        )

    @staticmethod
    def _vcash(totmoney, totcftable, cashobj):
        """
        return a virtue status table with a mf(cash) column based on the given tot money and cftable
        """
        cashl = []
        cashl.append(totmoney + totcftable.iloc[0].cash)
        for i in range(len(totcftable) - 1):
            date = totcftable.iloc[i + 1].date
            delta = totcftable.iloc[i + 1].cash
            if delta < 0:
                cashl.append(
                    myround(
                        delta
                        / cashobj.price[cashobj.price["date"] <= date].iloc[-1].netvalue
                    )
                )
            else:
                cashl.append(delta)
        datadict = {"date": totcftable.loc[:, "date"], "mf": cashl}
        return pd.DataFrame(data=datadict)

    def unitvalue(self, date=yesterdayobj()):
        """
        :returns: float at unitvalue of the whole investment combination
        """
        date = convert_date(date)
        res = 0
        for fund in self.fundtradeobj:
            res += fund.briefdailyreport(date).get("currentvalue", 0)
        return res / self.totmoney

    def v_tradecost(self, threhold=0, date=yesterdayobj(), rendered=True):
        if getattr(self, "price", None) is None:
            raise ValueError("Please generate price table by ``bcmkset()`` first")
        cftable = self.fundtradeobj[-1].cftable[1:]
        cftable = cftable[abs(cftable["cash"]) > threhold]
        cftable["cash"] = -cftable["cash"]
        return vtradecost(self, cftable, end=date, rendered=rendered)


class imul(mul):
    def __init__(self, *fundtradeobj, status=None, istatus=None):
        """
        对场内投资组合进行分析的类

        :param fundtradeobj: itrade objects.
        :param status: 场内格式记账单，或 irecord 对象。
        """

        if not fundtradeobj:
            fundtradeobj = []
        if status is None:
            status = istatus
        if isinstance(status, irecord):
            status = status.status
        fundcodelist = [f.code for f in fundtradeobj]
        if status is not None:
            for code in status.code.unique():
                if code not in fundcodelist and not code.startswith("#"):
                    fundtradeobj.append(itrade(code, status))
        self.fundtradeobj = tuple(fundtradeobj)
        self.totcftable = self._mergecftb()
        self.is_in = True


Mul = mul
MulFix = mulfix
IMul = imul
