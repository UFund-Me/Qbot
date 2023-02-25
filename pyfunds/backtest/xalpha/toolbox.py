# -*- coding: utf-8 -*-
"""
modules for Object oriented toolbox which wrappers get_daily and some more
"""

import re
import sys
import datetime as dt
import numpy as np
import pandas as pd
from collections import deque
from functools import wraps, lru_cache
import logging
from scipy import stats
from bs4 import BeautifulSoup

from xalpha.cons import (
    opendate,
    yesterday,
    next_onday,
    last_onday,
    scale_dict,
    tz_bj,
    holidays,
    xnpv,
    xirr,
    rget,
    rpost,
)
from xalpha.info import get_fund_holdings
from xalpha.universal import (
    get_rt,
    get_bar,
    ttjjcode,
    get_bond_rates,
    _convert_code,
    _inverse_convert_code,
    fetch_backend,
    save_backend,
)
import xalpha.universal as xu  ## 为了 set_backend 可以动态改变此模块的 get_daily
from xalpha.exceptions import ParserFailure, DateMismatch, NonAccurate

thismodule = sys.modules[__name__]

logger = logging.getLogger(__name__)


def _set_holdings(module):
    for name in [
        "no_trading_days",
        "holdings",
        "currency_info",
        "market_info",
        "futures_info",
        "alt_info",
        "gap_info",
    ]:
        setattr(thismodule, name, getattr(module, name, {}))


def set_holdings(module=None):
    """
    导入外部 holdings.py 数据文件用来预测基金净值

    :param module: mod. import holdings
    :return: None.
    """
    if not module:
        try:
            from xalpha import holdings

            _set_holdings(holdings)
            print("holdings.py is found and loaded within xalpha dir")
        except ImportError:
            # print("no holdings.py is found") # may cause confusing for general users
            from xalpha import cons

            _set_holdings(cons)
    else:
        _set_holdings(module)
        print("external holdings.py is loaded")


set_holdings()


def _set_display_notebook():
    """
    Initialize DataTable mode for pandas DataFrame represenation.
    """
    from IPython.core.display import display, Javascript

    display(
        Javascript(
            """
            require.config({
                paths: {
                    DT: '//cdn.datatables.net/1.10.20/js/jquery.dataTables.min',
                }
            });
            $('head').append('<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">');
            $('head').append('<style> td, th {{text-align: center;}}</style>')
        """
        )
    )

    def _repr_datatable_(self):
        # create table DOM
        script = f"$(element).html(`{self.to_html(index=False)}`);\n"

        # execute jQuery to turn table into DataTable
        script += """
                require(["DT"], function(DT) {$(document).ready( () => {
                    // Turn existing table into datatable
                    $(element).find("table.dataframe").DataTable({'scrollX': '100%'});
                    })
                });
        """

        return script

    pd.DataFrame._repr_javascript_ = _repr_datatable_


def set_display(env=""):
    """
    开关 DataFrame 的显示模式，仅 Jupyter Notebook 有效。

    :param env: str, default "". If env="notebook", pd.DataFrame will be shown in fantastic web language
    :return:
    """
    if not env:
        try:
            delattr(pd.DataFrame, "_repr_javascript_")
        except AttributeError:
            pass
    elif env in ["notebook", "jupyter", "ipython"]:
        _set_display_notebook()
    else:
        raise ParserFailure("unknown env %s" % env)


def PEBHistory(code, start=None, end=None, **kwargs):
    """
    历史估值分析工具箱

    :param code: str.
        1. SH000***, SZ399***, 指数历史估值情况，第一原理计算，需要聚宽数据源
        2. F******, 基金历史估值情况，根据股票持仓，第一原理计算
        3. 8*****, 申万行业估值数据，需要聚宽数据源
        4. 沪深港美股票代码，个股历史估值数据
    :param start: str, %Y%m%d, 默认起点随着标的类型不同而不同
    :param end: str, 仅限于 debug，强烈不建议设定，默认到昨天
    :return: some object of PEBHistory class
    """
    if code.startswith("SH000") or code.startswith("SZ399"):
        return IndexPEBHistory(code, start, end, **kwargs)
    elif code.startswith("F"):
        return FundPEBHistory(code, start, end, **kwargs)
    elif code.startswith("8"):
        return SWPEBHistory(code, start, end, **kwargs)
    else:
        return StockPEBHistory(code, start, end, **kwargs)


class IndexPEBHistory:
    """
    对于指数历史 PE PB 的封装类
    """

    indexs = {
        "000016.XSHG": ("上证50", "2012-01-01"),
        "000300.XSHG": ("沪深300", "2012-01-01"),
        "000905.XSHG": ("中证500", "2012-01-01"),
        "000922.XSHG": ("中证红利", "2012-01-01"),
        "000925.XSHG": ("基本面50", "2012-01-01"),
        "399006.XSHE": ("创业板指", "2012-01-01"),
        "000992.XSHG": ("全指金融", "2012-01-01"),
        "000991.XSHG": ("全指医药", "2012-01-01"),
        "399932.XSHE": ("中证消费", "2012-01-01"),
        "000831.XSHG": ("500低波", "2013-01-01"),
        "000827.XSHG": ("中证环保", "2013-01-01"),
        "000978.XSHG": ("医药100", "2012-01-01"),
        "399324.XSHE": ("深证红利", "2012-01-01"),
        "399971.XSHE": ("中证传媒", "2014-07-01"),
        "000807.XSHG": ("食品饮料", "2013-01-01"),
        "000931.XSHG": ("中证可选", "2012-01-01"),
        "399812.XSHE": ("养老产业", "2016-01-01"),
        "000852.XSHG": ("中证1000", "2015-01-01"),
    }

    # 聚宽数据源支持的指数列表： https://www.joinquant.com/indexData

    def __init__(self, code, start=None, end=None, **kwargs):
        """

        :param code: str. 形式可以是 399971.XSHE 或者 SH000931
        :param start: Optional[str]. %Y-%m-%d, 估值历史计算的起始日。
        :param end: Dont use, only for debug
        """
        yesterday_str = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        if len(code.split(".")) == 2:
            self.code = code
            self.scode = _convert_code(code)
        else:
            self.scode = code
            self.code = _inverse_convert_code(self.scode)
        if self.code in self.indexs:
            self.name = self.indexs[self.code][0]
            if not start:
                start = self.indexs[self.code][1]
        else:
            try:
                self.name = get_rt(self.scode)["name"]
            except:
                self.name = self.scode
            if not start:
                start = "2012-01-01"  # 可能会出问题，对应指数还未有数据
        self.start = start
        if not end:
            end = yesterday_str
        self.df = xu.get_daily("peb-" + self.scode, start=self.start, end=end, **kwargs)
        self.ratio = None
        self.title = "指数"
        self._gen_percentile()

    def _gen_percentile(self):
        self.pep = [
            round(i, 3) for i in np.nanpercentile(self.df.pe, np.arange(0, 110, 10))
        ]
        try:
            self.pbp = [
                round(i, 3) for i in np.nanpercentile(self.df.pb, np.arange(0, 110, 10))
            ]
        except TypeError:
            df = self.df.fillna(1)
            self.pbp = [
                round(i, 3) for i in np.nanpercentile(df.pb, np.arange(0, 110, 10))
            ]

    def percentile(self):
        """
        打印 PE PB 的历史十分位对应值

        :return:
        """
        print("PE 历史分位:\n")
        print(*zip(np.arange(0, 110, 10), self.pep), sep="\n")
        print("\nPB 历史分位:\n")
        print(*zip(np.arange(0, 110, 10), self.pbp), sep="\n")

    def v(self, y="pe"):
        """
        pe 或 pb 历史可视化

        :param y: Optional[str]. "pe" (defualt) or "pb"
        :return:
        """
        return self.df.plot(x="date", y=y)

    def fluctuation(self):
        if not self.ratio:
            d = self.df.iloc[-1]["date"]
            oprice = xu.get_daily(
                code=self.scode, end=d.strftime("%Y%m%d"), prev=20
            ).iloc[-1]["close"]
            nprice = get_rt(self.scode)["current"]
            self.ratio = nprice / oprice
        return self.ratio

    def current(self, y="pe"):
        """
        返回实时的 pe 或 pb 绝对值估计。

        :param y: Optional[str]. "pe" (defualt) or "pb"
        :return: float.
        """
        try:
            return round(self.df.iloc[-1][y] * self.fluctuation(), 3)
        except TypeError:
            return np.nan

    def current_percentile(self, y="pe"):
        """
        返回实时的 pe 或 pb 历史百分位估计

        :param y: Optional[str]. "pe" (defualt) or "pb"
        :return: float.
        """
        df = self.df
        d = len(df)
        u = len(df[df[y] < self.current(y)])
        return round(u / d * 100, 2)

    def summary(self, return_tuple=False):
        """
        打印现在估值的全部分析信息。

        :return:
        """
        result = (
            (
                self.current("pe"),
                self.current_percentile("pe"),
                max(
                    round(
                        (self.current("pe") - self.pep[0]) / self.current("pe") * 100, 1
                    ),
                    0,
                ),
            ),
            (
                self.current("pb"),
                self.current_percentile("pb"),
                max(
                    round(
                        (self.current("pb") - self.pbp[0]) / self.current("pb") * 100, 1
                    ),
                    0,
                ),
            ),
        )
        print("%s%s估值情况\n" % (self.title, self.name))
        # if dt.datetime.strptime(self.start, "%Y-%m-%d") > dt.datetime(2015, 1, 1):
        #     print("(历史数据较少，仅供参考)\n")
        print("现在 PE 绝对值 %s, 相对分位 %s%%，距离最低点 %s %%\n" % result[0])
        print("现在 PB 绝对值 %s, 相对分位 %s%%，距离最低点 %s %%\n" % result[1])
        if return_tuple:
            return result


class StockPEBHistory(IndexPEBHistory):
    """
    个股历史估值封装
    """

    def __init__(self, code, start=None, end=None, **kwargs):
        """

        :param code: 801180 申万行业指数
        :param start:
        :param end:
        """
        self.code = code
        self.scode = code
        if not end:
            end = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        if not start:
            start = "2012-01-01"
        self.start = start
        self.df = xu.get_daily("peb-" + code, start=start, end=end, **kwargs)
        self.name = get_rt(code)["name"]
        self.ratio = 1
        self.title = "个股"
        self._gen_percentile()


class FundPEBHistory(IndexPEBHistory):
    """
    基金历史估值封装
    """

    def __init__(self, code, start=None, end=None, **kwargs):
        self.code = code
        self.scode = code
        if not end:
            end = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        if not start:
            start = "2016-01-01"  # 基金历史通常比较短
        self.start = start
        self.df = xu.get_daily("peb-" + code, start=start, end=end, **kwargs)
        self.name = get_rt(code)["name"]
        self.title = "基金"
        self.ratio = None
        self._gen_percentile()


class SWPEBHistory(IndexPEBHistory):
    """
    申万行业历史估值封装。
    申万一级行业指数列表：
    https://www.hysec.com/hyzq/hy/detail/detail.jsp?menu=4&classid=00000003001200130002&firClassid=000300120013&twoClassid=0003001200130002&threeClassid=0003001200130002&infoId=3046547
    二三级行业指数也支持
    """

    index1 = [
        "801740",
        "801020",
        "801110",
        "801200",
        "801160",
        "801010",
        "801120",
        "801230",
        "801750",
        "801050",
        "801890",
        "801170",
        "801710",
        "801130",
        "801180",
        "801760",
        "801040",
        "801780",
        "801880",
        "801140",
        "801720",
        "801080",
        "801790",
        "801030",
        "801730",
        "801210",
        "801770",
        "801150",
    ]

    def __init__(self, code, start=None, end=None, **kwargs):
        """

        :param code: 801180 申万行业指数
        :param start:
        :param end:
        """
        self.code = code
        self.scode = code
        if not end:
            end = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        if not start:
            start = "2012-01-01"
        self.start = start
        self.df = xu.get_daily("sw-" + code, start=start, end=end, **kwargs)
        self.name = self.df.iloc[0]["name"]
        self.ratio = 1
        self.title = "申万行业指数"
        self._gen_percentile()


class TEBHistory:
    """
    指数总盈利和总净资产变化的分析工具箱
    """

    def __init__(self, code, start=None, end=None, **kwargs):
        """

        :param code: str. 指数代码，eg. SH000016
        :param start:
        :param end:
        """
        df = xu.get_daily("teb-" + code, start=start, end=end, **kwargs)
        df["e"] = pd.to_numeric(df["e"])
        df["b"] = pd.to_numeric(df["b"])
        df["lnb"] = df["b"].apply(lambda s: np.log(s))
        df["lne"] = df["e"].apply(lambda s: np.log(s))
        df["roe"] = df["e"] / df["b"] * 100
        df["date_count"] = (df["date"] - df["date"].iloc[0]).apply(
            lambda s: int(s.days)
        )
        self.df = df
        self.fit(verbose=False)

    def fit(self, verbose=True):
        """
        fit exponential trying find annualized increase

        :param verbose: if True (default), print debug info of linear regression
        :return:
        """
        df = self.df
        slope_b, intercept_b, r_b, p_b, std_err_b = stats.linregress(
            df["date_count"], df["lnb"]
        )
        slope_e, intercept_e, r_e, p_e, std_err_e = stats.linregress(
            df["date_count"], df["lne"]
        )
        if verbose:
            print("B fit", slope_b, intercept_b, r_b, p_b, std_err_b)
            print("E fit", slope_e, intercept_e, r_e, p_e, std_err_e)
        self.slope_b = slope_b
        self.intercept_b = intercept_b
        self.slope_e = slope_e
        self.intercept_e = intercept_e

    def result(self):
        """

        :return: Dict[str, float]. 返回指数总净资产和净利润的年均增速
        （拟合平滑意义，而非期末除以期初再开方，更好减少时间段两端极端情形的干扰）
        """
        return {
            "b_increase_percent": round((np.exp(365 * self.slope_b) - 1) * 100, 2),
            "e_increase_percent": round((np.exp(365 * self.slope_e) - 1) * 100, 2),
        }

    def v(self, y="lne"):
        """
        总资产或总利润与拟合曲线的可视化

        :param y: str. one of lne, lnb, e, b, roe
        :return:
        """
        df = self.df
        if y == "roe":
            return df.plot(x="date", y="roe")
        fitx = np.arange(0, df.iloc[-1]["date_count"], 10)
        if y == "lne":
            fity = self.intercept_e + self.slope_e * fitx
        elif y == "lnb":
            fity = self.intercept_b + self.slope_b * fitx
        elif y == "e":
            fity = np.exp(self.intercept_e + self.slope_e * fitx)
        elif y == "b":
            fity = np.exp(self.intercept_b + self.slope_b * fitx)
        else:
            raise ParserFailure("Unrecogized y %s" % y)
        ax = df.plot(x="date_count", y=y)
        ax.plot(fitx, fity)
        return ax


class Compare:
    """
    将不同金融产品同起点归一化比较
    """

    def __init__(
        self, *codes, start="20200101", end=yesterday(), col="close", normalize=True
    ):
        """

        :param codes: Union[str, tuple], 格式与 :func:`xalpha.universal.get_daily` 相同，若需要汇率转换，需要用 tuple，第二个元素形如 "USD"
        :param start: %Y%m%d
        :param end: %Y%m%d, default yesterday
        :param col: str, default close. The column to be compared.
        :param normalize: bool, default True. 是否将对比价格按起点时间归一。
        """
        totdf = pd.DataFrame()
        codelist = []
        for c in codes:
            if isinstance(c, tuple):
                code = c[0]
                currency = c[1]
            else:
                code = c
                currency = "CNY"  # 标的不做汇率调整
            codelist.append(code)
            df = xu.get_daily(code, start=start, end=end)
            df = df[df.date.isin(opendate)]
            currency_code = _get_currency_code(currency)
            if currency_code:
                cdf = xu.get_daily(currency_code, start=start, end=end)
                cdf = cdf[cdf["date"].isin(opendate)]
                df = df.merge(right=cdf, on="date", suffixes=("_x", "_y"))
                df[col] = df[col + "_x"] * df[col + "_y"]
            if normalize:
                df[code] = df[col] / df.iloc[0][col]
            else:
                df[code] = df[col]
            df = df.reset_index()
            df = df[["date", code]]
            if "date" not in totdf.columns:
                totdf = df
            else:
                totdf = totdf.merge(on="date", right=df)
        self.totdf = totdf
        self.codes = codelist

    def v(self):
        """
        显示日线可视化

        :return:
        """
        return self.totdf.plot(x="date", y=self.codes)

    def corr(self):
        """
        打印相关系数矩阵

        :return: pd.DataFrame
        """
        return self.totdf.iloc[:, 1:].pct_change().corr()


class OverPriced:
    """
    ETF 或 LOF 历史折溢价情况分析
    """

    def __init__(self, code, start=None, end=None, prev=None):
        """

        :param code: str. eg SH501018, SZ160416
        :param start: date range format is the same as xa.get_daily
        :param end:
        :param prev:
        """
        self.code = code
        df1 = xu.get_daily("F" + self.code[2:], start=start, end=end, prev=prev)
        df2 = xu.get_daily(self.code, start=start, end=end, prev=prev)
        df1 = df1.merge(df2, on="date", suffixes=("_F", "_" + code[:2]))
        df1["diff_rate"] = (
            (df1["close_" + code[:2]] - df1["close_F"]) / df1["close_F"] * 100
        )
        self.df = df1

    def v(self, hline=None):
        """

        :param hline: Union[float, List[float]], several horizental lines for assistance
        :return:
        """
        ax = self.df.plot(x="date", y="diff_rate")
        if hline:
            if isinstance(hline, float):
                ax.axhline(hline, c="red")
            else:
                for h in hline:
                    ax.axhline(h, c="red")
        return ax


#########################
# cb value estimation   #
#########################


def BlackScholes(S, K, t, v, r=0.02, CallPutFlag="C"):
    """
    BS option pricing calculator

    :param S: current stock price
    :param K: stricking price
    :param t: Time until option exercise (years to maturity)
    :param r: risk-free interest rate (by year)
    :param v: Variance(volitility) of annual increase
    :param CallPutFlag: "C" or "P", default call option
    :return:
    """
    # function modified from https://github.com/boyac/pyOptionPricing

    def CND(X):
        return stats.norm.cdf(X)

    d1 = (np.log(S / K) + (r + (v ** 2) / 2) * t) / (v * np.sqrt(t))
    d2 = d1 - v * np.sqrt(t)

    if CallPutFlag in ["c", "C"]:
        return S * CND(d1) - K * np.exp(-r * t) * CND(d2)  # call option
    elif CallPutFlag in ["p", "P"]:
        return K * np.exp(-r * t) * CND(-d2) - S * CND(-d1)  # put option
    else:
        raise ValueError("Unknown CallPutFlag %s" % CallPutFlag)


def cb_bond_value(issue_date, rlist, rate=0.03, date=None, tax=1.0):
    """
    可转债债券价值计算器

    :param issue_date: str. 发行日期
    :param rlist: List[float], 每年度的利息百分点，比如 0.4,0.6等，最后加上最后返回的值（不含最后一年利息），比如 104
    :param rate:  float，现金流折算利率，应取同久期同信用等级的企业债利率，参考 https://yield.chinabond.com.cn/
    :param date: 默认今天，计算债券价值基于的时间
    :param tax: float，税率，1.0 表示不算税后，0.8 为计算税后利息，一般不需要设置成0.8，因为区别不大
    :return:
    """

    if rlist[-1] < 100:
        logger.warning(
            "the format of rlist must contain the final return more than 100 without interest of that year"
        )
    issue_date = issue_date.replace("-", "").replace("/", "")
    issue_date_obj = dt.datetime.strptime(issue_date, "%Y%m%d")
    if date is None:
        date_obj = dt.datetime.today()
    else:
        date = date.replace("-", "").replace("/", "")
        date_obj = dt.datetime.strptime(date, "%Y%m%d")
    cf = [(date_obj, 0)]
    passed = (date_obj - issue_date_obj).days // 365
    for i, r in enumerate(rlist[:-1]):
        if i >= passed:
            cf.append((issue_date_obj + dt.timedelta(days=(i + 1) * 365), r * tax))
    cf.append((issue_date_obj + dt.timedelta(days=(len(rlist) - 1) * 365), rlist[-1]))
    return xnpv(rate, cf)


def cb_ytm(issue_date, rlist, cp, date=None, tax=1.0, guess=0.01):
    """
    可转债到期收益率计算器

    :param issue_date: 发行日期
    :param rlist: 计息及赎回列表
    :param cp: 可转债现价
    :param date: 参考日期
    :param tax: 计税 1 vs 0.8 税后 YTM
    :param guess: YTM 估计初始值
    :return:
    """

    if rlist[-1] < 100:
        logger.warning(
            "the format of rlist must contain the final return more than 100 without interest of that year"
        )
    issue_date = issue_date.replace("-", "").replace("/", "")
    issue_date_obj = dt.datetime.strptime(issue_date, "%Y%m%d")
    if date is None:
        date_obj = dt.datetime.today()
    else:
        date = date.replace("-", "").replace("/", "")
        date_obj = dt.datetime.strptime(date, "%Y%m%d")
    cf = [(date_obj, -cp)]
    passed = (date_obj - issue_date_obj).days // 365
    for i, r in enumerate(rlist[:-1]):
        if i >= passed:
            cf.append((issue_date_obj + dt.timedelta(days=(i + 1) * 365), r * tax))
    # 关于赎回利息计算： https://www.jisilu.cn/?/question/339
    # https://www.jisilu.cn/question/5807
    # 富投网的算法：将最后一年超出100的部分，全部按照20%计税，
    # 关于到期或回售部分的利息，最新进展： https://www.jisilu.cn/question/389264

    cf.append((issue_date_obj + dt.timedelta(days=(len(rlist) - 1) * 365), rlist[-1]))
    try:
        return xirr(cf, guess=guess)
    except RuntimeError:
        return


class CBCalculator:
    """
    可转债内在价值，简单计算器，期权价值与债券价值估算
    """

    def __init__(
        self,
        code,
        bondrate=None,
        riskfreerate=None,
        volatility=None,
        name=None,
        zgj=None,
    ):
        """

        :param code: str. 转债代码，包含 SH 或 SZ 字头
        :param bondrate: Optional[float]. 评估所用的债券折现率，默认使用中证企业债对应信用评级对应久期的利率
        :param riskfreerate: Optioal[float]. 评估期权价值所用的无风险利率，默认使用国债对应久期的年利率。
        :param volatility: Optional[float]. 正股波动性百分点，默认在一个范围浮动加上历史波动率的小幅修正。
        :param name: str. 对于历史回测，可以直接提供 str，免得多次 get_rt 获取 name
        :param zgj: float. 手动设置转股价，适用于想要考虑转股价调整因素进行历史估值的高阶用户
        """
        # 应该注意到该模型除了当天外，其他时间估计会利用现在的转股价，对于以前下修过转股价的转债历史价值估计有问题

        self.code = code
        self.refbondrate = bondrate
        self.bondrate = self.refbondrate
        self.refriskfreerate = riskfreerate
        self.riskfreerate = self.refriskfreerate
        self.refvolatility = volatility
        self.volatility = self.refvolatility
        self.name = name

        r = rget("https://www.jisilu.cn/data/convert_bond_detail/" + code[2:])
        r.encoding = "utf-8"
        b = BeautifulSoup(r.text, "lxml")
        self.rlist = [
            float(re.search(r"[\D]*([\d]*.?[\d]*)[\s]*[\%]", s).group(1))
            for s in re.split("、|，", b.select("td[id=cpn_desc]")[0].string)
        ]
        td_redeem_price = b.select("td[id=redeem_price]")[0]
        if td_redeem_price.span:
            redeem_price = float(
                re.match(
                    r"\S+，合计到期赎回价(\d\d\d\.\d\d)元", td_redeem_price.span["title"]
                ).group(1)
            )
            logger.info(
                "{}: redeem_price {} obtained from superscript".format(
                    code, redeem_price
                )
            )
        else:
            redeem_price = float(td_redeem_price.string)
        self.rlist.append(redeem_price)
        self.rlist[-1] -= self.rlist[-2]  # 最后一年不含息返多少
        self.scode = (
            b.select("td[class=jisilu_nav]")[0].contents[1].text.split("-")[1].strip()
        )
        self.scode = ttjjcode(self.scode)  # 标准化股票代码
        if not zgj:
            self.zgj = float(b.select("td[id=convert_price]")[0].string)  # 转股价
        else:
            self.zgj = zgj
        self.rating = b.select("td[id=rating_cd]")[0].string.strip()
        self.enddate = b.select("td[id=maturity_dt]")[0].string
        self.zhanbi = b.select("td[id=convert_amt_ratio2]")[0].string.strip()
        self.shares = float(b.select("td[id=curr_iss_amt]")[0].string.strip())

    def process_byday(self, date=None):
        if not date:
            self.date_obj = dt.datetime.today()
        else:
            self.date_obj = dt.datetime.strptime(
                date.replace("-", "").replace("/", ""), "%Y%m%d"
            )
        if not date:
            rt = get_rt(self.code)
            self.name = rt["name"]
            self.cbp = rt["current"]  # 转债价
            self.stockp = get_rt(self.scode)["current"]  # 股票价
        else:
            try:
                if not self.name:
                    rt = get_rt(self.code)
                    self.name = rt["name"]
            except:
                self.name = "unknown"
            df = xu.get_daily(self.code, prev=100, end=self.date_obj.strftime("%Y%m%d"))
            self.cbp = df.iloc[-1]["close"]
            df = xu.get_daily(
                self.scode, prev=100, end=self.date_obj.strftime("%Y%m%d")
            )
            self.stockp = df.iloc[-1]["close"]

        df = xu.get_daily(self.scode, prev=360, end=self.date_obj.strftime("%Y%m%d"))
        self.history_volatility = np.std(
            np.log(df["close"] / df.shift(1)["close"])
        ) * np.sqrt(244)
        if not self.refvolatility:
            self.volatility = 0.17
            if self.rating in ["A-", "A", "A+"] or self.rating.startswith("B"):
                self.volatility = 0.25
            elif self.rating in ["AA-"]:
                self.volatility = 0.2
            elif self.rating in ["AA"]:
                self.volatility = 0.19
            elif self.rating in ["AA+"]:
                self.volatility = 0.18
            if self.history_volatility < 0.2:
                self.volatility -= 0.01
            elif self.history_volatility > 0.7:
                self.volatility += 0.05
            elif self.history_volatility > 0.6:
                self.volatility += 0.035
            elif self.history_volatility > 0.5:
                self.volatility += 0.02
            elif self.history_volatility > 0.4:
                self.volatility += 0.01
        self.years = len(self.rlist) - 1
        syear = int(self.enddate.split("-")[0]) - self.years
        self.issuedate = str(syear) + self.enddate[4:]
        self.days = (
            dt.datetime.strptime(self.enddate, "%Y-%m-%d") - self.date_obj
        ).days
        if not self.refbondrate:
            ratestable = get_bond_rates(self.rating, self.date_obj.strftime("%Y-%m-%d"))
            if self.rating in ["A", "A+", "AA-"] or self.rating.startswith("B"):
                ## AA 到 AA- 似乎是利率跳高的一个坎
                cutoff = 3  # changed from 2 by considering more credit risk
            else:
                cutoff = 4
            if self.days / 365 > cutoff:
                # 过长久期的到期收益率，容易造成估值偏离，虽然理论上是对的
                # 考虑到国内可转债市场信用风险较低，不应过分低估低信用债的债券价值
                self.bondrate = (
                    ratestable[ratestable["year"] <= cutoff].iloc[-1]["rate"] / 100
                )
            else:
                self.bondrate = (
                    ratestable[ratestable["year"] >= self.days / 365].iloc[0]["rate"]
                    / 100
                )
        if not self.refriskfreerate:
            ratestable = get_bond_rates("N", self.date_obj.strftime("%Y-%m-%d"))
            if self.days / 365 > 5:
                self.riskfreerate = (
                    ratestable[ratestable["year"] <= 5].iloc[-1]["rate"] / 100
                )
            else:
                self.riskfreerate = (
                    ratestable[ratestable["year"] >= self.days / 365].iloc[0]["rate"]
                    / 100
                )

    def analyse(self, date=None):
        self.process_byday(date=date)
        d = {
            "stockcode": self.scode,
            "cbcode": self.code,
            "name": self.name,
            "enddate": self.enddate,
            "interest": self.rlist,
            "zgj": self.zgj,
            "stockprice": self.stockp,
            "cbprice": self.cbp,
            "rating": self.rating,
            "bondrate": self.bondrate,
            "predicted_volatility": self.volatility,
            "historical_volatility": self.history_volatility,
            "riskfreerate": self.riskfreerate,
            "years": self.days / 365,
            "issuedate": self.issuedate,
            "date": self.date_obj.strftime("%Y-%m-%d"),
            "zhanbi": self.zhanbi,
            "remaining": self.shares,
        }
        d["bond_value"] = cb_bond_value(self.issuedate, self.rlist, self.bondrate)
        d["ytm_wo_tax"] = cb_ytm(self.issuedate, self.rlist, self.cbp)
        d["ytm_wi_tax"] = cb_ytm(self.issuedate, self.rlist, self.cbp, tax=0.8)
        d["option_value"] = (
            BlackScholes(
                self.stockp,
                self.zgj,
                self.days / 365,
                self.volatility,
                self.riskfreerate,
                CallPutFlag="C",
            )
            * 100
            / self.zgj
        )
        # 经验上看，下修强赎回售及美式期权行为等其他带来的期权价值大约有1到4元的增益：
        # 以0.015 为无风险利率和 0.15-0.18 为波动率估计范围的情形下
        # 实在没有必要为了这几块钱上复杂工具估值，因为无风险利率几十个bp的改变，就足以导致更大的波动，看个热闹就行了
        # 可转债估值只能是模糊的正确
        d["tot_value"] = d["bond_value"] + d["option_value"]
        d["premium"] = (self.cbp / d["tot_value"] - 1) * 100
        return d


#########################
# netvalue prediction   #
#########################


@lru_cache(maxsize=512)
def get_currency(code):
    """
    通过代码获取计价货币的函数

    :param code:
    :return:
    """
    # 强制需要自带 cache，否则在回测 table 时，info 里没有的代码将很灾难。。。
    # only works for HKD JPY USD GBP CNY EUR, not very general when data source gets diverse more
    try:
        if code in currency_info:
            return currency_info[code]
        elif (code.startswith("F") or code.startswith("M")) and code[1:].isdigit():
            return "CNY"
        elif code.startswith("FT-") and len(code.split(":")) > 2:
            # be careful! FT-ABC:IOM has no currency information!
            return code.split(":")[-1]
        elif code.startswith("HK") and code[2:].isdigit():
            return "HKD"
        currency = get_rt(code)["currency"]
        if currency is None:
            currency = "CNY"
        elif currency == "JPY":
            currency = "100JPY"
    except (TypeError, AttributeError, ValueError):
        logger.warning("set currency of %s as default CNY" % code)
        currency = "CNY"
    return currency


def _get_currency_code(c):
    if c == "CNY":
        return  # None
    if c == "JPY":
        return "100JPY/CNY"
    zjjl = [
        "USD",
        "EUR",
        "100JPY",
        "HKD",
        "GBP",
        "AUD",
        "NZD",
        "SGD",
        "CHF",
        "CAD",
        "MYR",
        "RUB",
        "ZAR",
        "KRW",
        "AED",
        "SAR",
        "HUF",
        "PLN",
        "DKK",
        "SEK",
        "NOK",
        "TRY",
        "MXN",
        "THB",
    ]
    if c in zjjl:
        return c + "/CNY"
    return "currencies/" + c.lower() + "-cny"


@lru_cache(maxsize=512)
def get_currency_code(code):
    c = get_currency(code)
    return _get_currency_code(c)


@lru_cache(maxsize=512)
def get_market(code):
    """
    非常粗糙的通过代码获取交易市场的函数

    :param code:
    :return:
    """
    trans = {
        "USD": "US",
        "GBP": "UK",
        "HKD": "HK",
        "CNY": "CN",
        "CHF": "CH",
        "JPY": "JP",
        "EUR": "DE",
        "AUD": "AU",
        "INR": "IN",
        "SGD": "SG",
    }
    try:
        if code in market_info:
            return market_info[code]
        elif code.startswith("CNY/") or code.endswith("/CNY"):
            return "CM"  # china money 中间价市场标记
        elif code.startswith("HK") and code[2:].isdigit():
            return "HK"
        market = get_rt(code).get("market", None)
        if market is None:
            market = get_currency(code)
            market = trans.get(market, market)
    except (TypeError, AttributeError, ValueError, IndexError):
        market = "CN"
    return market


@lru_cache(maxsize=512)
def get_alt(code):
    """
    抓取失败后寻找替代对等标的

    :param code:
    :return:
    """
    if code in alt_info:
        return alt_info[code]
    elif len(code[1:].split("/")) == 2 and len(code.split("/")[-1]) > 6:
        return "INA-" + code  # 英为 app 源替代网页源
    elif code.startswith("SP") and code[2:].isdigit():
        return "SPC" + code[2:]  # 中国区标普源替代美国源
    else:
        return None


def _is_on(code, date):
    df = xu.get_daily(code, prev=20, end=date)
    if len(df[df["date"] == date]) == 0:
        return False
    return True


def is_on(date, market="CN", no_trading_days=None):
    """
    粗略鉴定 date 日是否是指定 market 的开市日，对于当日鉴定，仍有数据未及时更新的风险。也存在历史数据被 investing 补全的风险。

    :param date:
    :param market: str. CN, JP, HK, US, UK, CH, HK, DE
    :return: bool.
    """
    if not isinstance(date, dt.datetime):
        date_obj = dt.datetime.strptime(
            date.replace("-", "").replace("/", ""), "%Y%m%d"
        )
    else:
        date_obj = date
    if date_obj.weekday() in [5, 6]:  # 周末休市
        # 注意部分中东市场周日开市，暂时涉及不到
        return False
    date_dash = date_obj.strftime("%Y-%m-%d")
    if no_trading_days:
        if date_dash in no_trading_days.get(market, []):
            return False
    if date_dash in holidays.get(market, []):
        return False
    logger.warning(
        "determine whether %s is holiday in %s market, but may be wrong, be careful!"
        % (date_dash, market)
    )
    if market in ["CN", "CHN", "CNY", "RMB", "CHINA", "CM"]:  # 国内节假日不更新中间价
        return date_dash in opendate
    elif market in ["JP", "JAPAN", "JPY", "100JPY"]:
        code = "indices/japan-ni225"
    elif market in ["US", "NY", "USD", "NASDAQ"]:
        code = "indices/us-spx-500"
    elif market in ["GBP", "UK", "GB"]:
        code = "indices/uk-100"
    elif market in ["GER", "EUR", "DE"]:  # 是否可以代表欧洲待考量, 还要警惕欧洲市场的美元计价标的
        code = "indices/germany-30"
    elif market in ["CHF", "SWI", "CH"]:
        code = "indices/switzerland-20"
    elif market in ["HK"]:
        code = "indices/hang-sen-40"
    else:
        logger.warning(
            "unknown oversea market %s, assuming %s follows US holiday pattern"
            % (market, date_dash)
        )  # not sure which last resort is the best, but make no huge difference anyhow
        code = "indices/us-spx-500"
    return _is_on(code, date)


def daily_increment(code, date, lastday=None, _check=False, warning_threhold=None):
    """
    单一标的 date 日（若 date 日无数据则取之前的最晚有数据日，但该日必须大于 _check 对应的日期）较上一日或 lastday 的倍数，
    lastday 支持不完整，且不能离 date 太远

    :param code:
    :param date:
    :param lastday: 如果用默认 None，则表示和前一日的涨跌, 不是一个支持任意日期涨幅的通用类，只有最接近的几天才保证逻辑没有问题
    :param _check: 数据必须已更新到 date 日，除非之前每天都是节假日
    :return:
    """
    try:
        tds = xu.get_daily(code=code, end=date, prev=30)
    except Exception as e:  # 只能笼统 catch 了，因为抓取失败的异常是什么都能遇到。。。
        code = get_alt(code)
        if code:
            tds = xu.get_daily(code=code, end=date, prev=30)
        else:
            raise e
    tds = tds[tds["date"] <= date]
    if len(tds) > 1 and warning_threhold:
        rough_ratio = tds.iloc[-1]["close"] / tds.iloc[-2]["close"]
        if rough_ratio > warning_threhold[0] or rough_ratio < warning_threhold[1]:
            logger.warning(
                "daily_increment detects abnormal increase or decrease of %s"
                " trying to refresh price cache" % code
            )
            tds = xu.get_daily(code=code, end=date, prev=30, refresh=True)
            # 对于可能出现的拆合股情况，刷新该标的全局缓存
            tds = tds[tds["date"] <= date]
    if _check:
        date = date.replace("-", "").replace("/", "")
        date_obj = dt.datetime.strptime(date, "%Y%m%d")

        while tds.iloc[-1]["date"] < date_obj:
            # in case data is not up to date
            # 但是存在日本市场休市时间不一致的情况，估计美股也存在
            if (
                not is_on(
                    date_obj.strftime("%Y%m%d"),
                    get_market(code),
                    no_trading_days=no_trading_days,
                )
                or (date_obj.strftime("%Y-%m-%d") in gap_info.get(code, []))
            ):
                print("%s is closed on %s" % (code, date))
                if not lastday:
                    return 1  # 当日没有涨跌，这里暂时为考虑 _check 和 lastday 相同的的情形
                date_obj -= dt.timedelta(days=1)
            else:
                raise DateMismatch(
                    code,
                    reason="%s has no data newer than %s"
                    % (code, date_obj.strftime("%Y-%m-%d")),
                )
    if not lastday:
        ratio = tds.iloc[-1]["close"] / tds.iloc[-2]["close"]
    else:
        tds2 = tds[tds["date"] <= lastday]
        if tds2 is None or len(tds2) == 0:
            ratio = 1.0
        # 未考虑检查连 lastday 的数据数据源都没更新的情形，这种可能极小
        else:
            ratio = tds.iloc[-1]["close"] / tds2.iloc[-1]["close"]
    return ratio


def _smooth_pos(r, e, o):
    """
    单日仓位估计的平滑函数

    :param r: 实际涨幅
    :param e: 满仓估计涨幅
    :param o: 昨日仓位估计
    :return:
    """
    pos = r / e
    o = (0.92 + o) / 2  # 抑制季报异常的仓位基准
    if pos <= 0:
        return o
    if pos > 1:
        pos = 1
    elif pos < 0.5:
        pos = pos ** 0.6

    if abs(r) < 0.6:  # 实际波动小时参考意义有限，进行削弱
        pos = (pos + (3 - 5 * abs(r)) * o) / (4 - 5 * abs(r))

    return pos


def error_catcher(f):
    """
    装饰器，透明捕获 DateMismatch

    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kws):
        try:
            return f(*args, **kws)
        except DateMismatch as e:
            code = args[0]
            error_msg = e.reason
            error_msg += ", therefore %s cannot predict correctly" % code
            raise NonAccurate(code=code, reason=error_msg)

    return wrapper


def evaluate_fluctuation(hdict, date, lastday=None, _check=None, warning_threhold=None):
    """
    分析资产组合 hdict 的涨跌幅，全部兑换成人民币考虑

    :param hdict:
    :param date:
    :param lastday:
    :param _check: bool, ensure date source has been updated, otherwise throw DataMismatch error
    :param warning_threhold: float>1, 异常检查阈值，若为 2, 则代表单日涨到2或跌倒1/2以外被舍弃
    :return:
    """
    price = 0
    tot = 0
    if warning_threhold:
        if isinstance(warning_threhold, tuple):
            pass
        else:
            warning_threhold = (warning_threhold, 1 / warning_threhold)  # 上界， 下界
    for fundid, percent in hdict.items():
        ratio = daily_increment(fundid, date, lastday, _check, warning_threhold)
        if warning_threhold:

            # 额外检查，防止误算大幅分红和拆合股等为本身的价格变化，对于变化幅度小的拆合股与分红无法区别与价格变化
            if ratio > warning_threhold[0] or ratio < warning_threhold[1]:
                logger.warning(
                    "%s has abnormal daily increment beyond warning_threhold %s, auto reset..."
                    % (fundid, warning_threhold)
                )
                ratio = 1  # 直接重置
        exchange = 1
        currency = get_currency_code(fundid)
        if currency:
            exchange = daily_increment(currency, date, lastday, _check)
        price += ratio * percent / 100 * exchange
        tot += percent
    remain = 100 - tot
    price += remain / 100
    return (price - 1) * 100


def get_holdings_dict(code, aim=95):
    """
    通过天天基金的股票持仓数据来生成实时预测所需的持仓字典，不保证稳定性和可靠性以及 API 的连续性，慎用

    :param code:
    :param aim:
    :return:
    """
    df = get_fund_holdings(code)
    if df.ratio.sum() < 60:
        d = dt.datetime.now()
        if d.month > 3 and d.month < 8:
            year = d.year - 1
            season = 4
        elif d.month <= 3:
            year = d.year - 1
            season = 2
        else:
            year = d.year
            season = 2
        # season 只选 2，4, 具有更详细的持仓信息
        df = get_fund_holdings(code, year, season)
        if df is None:
            if season == 4:
                season = 2
            else:
                year -= 1
                season = 4
            df = get_fund_holdings(code, year, season)
    df["scode"] = df["code"].apply(ttjjcode)
    d = pd.Series(df.ratio.values, index=df.scode).to_dict()
    d = scale_dict(d, aim=aim)
    return d


class RTPredict:
    """
    场内 ETF LOF 实时溢价，非 QDII 类
    """

    def __init__(self, code, t0dict=None):
        """

        :param code:
        :param t0dict:
        """
        self.code = code
        self.fcode = "F" + code[2:]
        if not t0dict:
            t0dict = holdings.get(code[2:], None)
        if not t0dict:
            raise ValueError("Please provide t0dict for prediction")
        if isinstance(t0dict, str):
            t0dict = {t0dict: 100}
        self.t0dict = t0dict
        self.t1value_cache = None
        self.now = dt.datetime.now(tz=tz_bj).replace(tzinfo=None)
        self.today = self.now.replace(hour=0, minute=0, second=0, microsecond=0)

    def get_t1(self, return_date=True):
        """
        获取昨日基金净值

        :return:
        """
        if not self.t1value_cache:
            last_r = get_rt(self.fcode)
            last_value, last_date = last_r["current"], last_r["time"]
            self.t1value_cache = (last_value, last_date)
        if return_date:
            return self.t1value_cache
        else:
            return self.t1value_cache[0]

    @error_catcher
    def get_t0(self, return_date=True, percent=False):
        last_value, last_date = self.get_t1()
        last_date_obj = dt.datetime.strptime(last_date, "%Y-%m-%d")
        cday = last_onday(self.today)
        while last_date_obj < cday:  # 昨天净值数据还没更新
            # 是否存在部分部分基金可能有 gap？
            if cday.strftime("%Y-%m-%d") not in gap_info.get(self.fcode, []):
                self.t1_type = "昨日未出"
                raise DateMismatch(
                    self.code,
                    reason="%s netvalue has not been updated to yesterday" % self.code,
                )
            else:
                cday = last_onday(cday)
            # 经过这个没报错，就表示数据源是最新的
        if last_date_obj >= self.today:  # 今天数据已出，不需要再预测了
            print(
                "no need to predict net value since it has been out for %s" % self.code
            )
            self.t1_type = "今日已出"
            if not return_date:
                return last_value
            else:
                return last_value, last_date
        t = 0
        n = 0
        today_str = self.today.strftime("%Y%m%d")
        for k, v in self.t0dict.items():
            w = v
            t += w
            r = get_rt(k)
            # k should support get_rt, investing pid doesn't support this!
            if percent:
                c = w / 100 * (1 + r["percent"] / 100)  # 直接取标的当日涨跌幅
            else:
                df = xu.get_daily(k)
                basev = df[df["date"] <= last_date].iloc[-1]["close"]
                c = w / 100 * r["current"] / basev
            currency_code = get_currency_code(k)
            if currency_code:
                c = c * daily_increment(currency_code, today_str)
                # TODO: 这里似乎应该有 lastdate
            n += c
        n += (100 - t) / 100
        t0value = n * last_value
        self.t0_delta = n
        if not return_date:
            return t0value
        else:
            return t0value, self.today.strftime("%Y-%m-%d")

    def get_t0_rate(self, percent=False, return_date=True):
        iopv = self.get_t0(percent=False, return_date=False)
        rtv = get_rt(self.code)["current"]
        r = (rtv / iopv - 1) * 100
        if return_date:
            return r, self.today.strftime("%Y-%m-%d")
        else:
            return r


class QDIIPredict:
    """
    T+2 确认份额的 QDII 型基金净值预测类

    .. warning::

        由于该类与现实时间的强烈耦合和激进的缓存利用，该类的对象不能"过夜"使用，每天需声明新的对象

    """

    def __init__(
        self, code, t1dict=None, t0dict=None, positions=False, fetch=False, save=False
    ):
        """

        :param code: str, 场内基金代码，eg SH501018
        :param t1dict: Dict[str, float]. 用来预测 T-1 净值的基金组合持仓，若为空自动去 holdings 中寻找。
        :param t0ict: Dict[str, float]. 用来预测 T 实时净值的基金组合持仓，若为空自动去 holdings 中寻找。
        :param positions: bool. 仓位是否浮动，默认固定仓位。
        :param fetch: bool, default True. 优先从 backend fetch t1。
        :param save: bool, default True. 将 t1 缓存到 backend。
        """
        self.code = code
        self.fcode = "F" + code[2:]
        self.fetch = fetch
        self.save = save

        if not t1dict:
            self.t1dict = holdings.get(code[2:], None)
            if not self.t1dict:
                raise ValueError("Please provide t1dict for prediction")
        else:
            self.t1dict = t1dict
        if not t0dict:
            self.t0dict = holdings.get(code[2:] + "rt", None)
        else:
            self.t0dict = t0dict
        self.position_cache = {}
        self.t1value_cache = {}
        self.t2value_cache = None
        # t0 实时净值自然不 cache
        self.positions = positions
        self.position_zero = sum([v for _, v in self.t1dict.items()])
        self.now = dt.datetime.now(tz=tz_bj).replace(tzinfo=None)
        self.today = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.t1_type = "未计算"
        self.bar_cache = {}
        self.t0_delta = None
        self.t1_delta = None
        # 不建议直接使用以上两者看变化量，在手动 set 后，以上两者可能继续为 None
        if fetch:
            df = fetch_backend("t1-" + code)
            if df is not None:
                df["date"] = pd.to_datetime(df["date"])
                for i, r in df.iterrows():
                    self.set_t1(float(r["t1"]), r["date"].strftime("%Y-%m-%d"))
                    self.set_position(float(r["pos"]), r["date"].strftime("%Y-%m-%d"))
            else:  # nodf
                emptydf = pd.DataFrame({"date": [], "t1": [], "pos": []})
                save_backend("t1-" + code, emptydf, header=True)

    def set_t1(self, value, date=None):
        """
        设定 T-1 的基金净值，有时我们只想计算实时净值，这就不需要重复计算 t1，可以先行设定

        :param value:
        :param date:
        :return:
        """
        if date is None:
            yesterday = last_onday(self.today)
            datekey = yesterday.strftime("%Y%m%d")
        else:
            datekey = date.replace("/", "").replace("-", "")
        if datekey in self.t1value_cache:
            logger.debug("t-1 value already exists, rewriting...")
        self.t1value_cache[datekey] = value
        self.t1_type = "已计算"

    def set_t2(self, value, date=None):
        """
        手动设定 t2 净值

        :param value:
        :return:
        """
        if not date:
            date = last_onday(last_onday(self.today)).strftime("%Y-%m-%d")
        self.t2value_cache = (value, date)

    def get_t2(self, return_date=True):
        """
        返回最新的已公布基金净值，注意这里严格按照最新公布，不一定是前两个交易日，可以更新，但更老会报错 DateMismatch

        :param return_date:
        :return: if return_date is True, tuple (value, %Y-%m-%d)
        """
        if not self.t2value_cache:
            last_r = get_rt(self.fcode)
            last_value, last_date = last_r["current"], last_r["time"]
            self.t2value_cache = (last_value, last_date)
        if return_date:
            return self.t2value_cache
        else:
            return self.t2value_cache[0]

    @error_catcher
    def get_t1(self, date=None, return_date=True):
        """
        预测 date 日的净值，基于 date-1 日的净值和 date 日的外盘数据，数据自动缓存，不会重复计算

        :param date: str. %Y-%m-%d. 注意若是 date 日为昨天，即今日预测昨日的净值，date 取默认值 None。
        :param return_date: bool, default True. return tuple, the second one is date in the format %Y%m%d
        :return: float, (str).
        :raises NonAccurate: 由于外盘数据还未及时更新，而 raise，可在调用程序中用 except 捕获再处理。
        """
        if date is None:
            yesterday = last_onday(self.today)
            datekey = yesterday.strftime("%Y%m%d")
        else:
            datekey = date.replace("/", "").replace("-", "")
        if datekey not in self.t1value_cache:
            logger.debug("no cache for t1 value, computing from beginning")
            if self.positions:
                current_pos = self.get_position(datekey, return_date=False)
                hdict = scale_dict(self.t1dict.copy(), aim=current_pos * 100)
            else:
                current_pos = sum([v for _, v in self.t1dict.items()]) / 100
                hdict = self.t1dict.copy()
            if date is None:  # 此时预测上个交易日净值
                yesterday_str = datekey
                last_value, last_date = self.get_t2()
                last_date_obj = dt.datetime.strptime(last_date, "%Y-%m-%d")
                cday = last_onday(last_onday(self.today))
                while last_date_obj < cday:  # 前天净值数据还没更新
                    # 是否存在部分 QDII 在 A 股交易日，美股休市日不更新净值的情形？
                    if (
                        (cday.strftime("%Y-%m-%d") not in gap_info.get(self.fcode, []))
                        and is_on(cday.strftime("%Y-%m-%d"), "US", no_trading_days)
                        and is_on(cday.strftime("%Y-%m-%d"), "DE", no_trading_days)
                    ):
                        # 这里检查比较宽松，只要当天美股休市，就可以认为确实基金数据不存在而非未更新
                        # 这里宽松检查的根本原因是，天天基金如果第二天早晨还没数据，几乎不可能是数据更新迟缓
                        self.t1_type = "前日未出"
                        raise DateMismatch(
                            self.code,
                            reason="%s netvalue has not been updated to the day before yesterday"
                            % self.code,
                        )
                    else:
                        cday = last_onday(cday)
                    # 经过这个没报错，就表示数据源是最新的
                if last_date_obj >= last_onday(self.today):  # 昨天数据已出，不需要再预测了
                    print(
                        "no need to predict t-1 value since it has been out for %s"
                        % self.code
                    )
                    self.t1_type = "昨日已出"
                    self.t1value_cache = {last_date.replace("-", ""): last_value}
                    if not return_date:
                        return last_value
                    else:
                        return last_value, last_date
            else:
                yesterday_str = datekey
                fund_price = xu.get_daily(self.fcode)  # 获取国内基金净值
                fund_last = fund_price[fund_price["date"] < date].iloc[-1]
                # 注意实时更新应用 date=None 传入，否则此处无法保证此数据是前天的而不是大前天的，因为没做校验
                # 事实上这里计算的预测是针对 date 之前的最晚数据和之前一日的预测
                last_value = fund_last["close"]
                last_date = fund_last["date"].strftime("%Y-%m-%d")
            self.t1_delta = (
                1
                + evaluate_fluctuation(
                    hdict,
                    yesterday_str,
                    lastday=last_date,
                    _check=True,
                    warning_threhold=(1.8, 0.1),
                )
                / 100
            )
            net = last_value * self.t1_delta
            self.t1value_cache[datekey] = net
            self.t1_type = "已计算"
            if self.save:
                df = pd.DataFrame(
                    {
                        "date": [datekey[:4] + "-" + datekey[4:6] + "-" + datekey[6:8]],
                        "t1": [net],
                        "pos": [current_pos],
                    }
                )
                save_backend("t1-" + self.code, df)
        if not return_date:
            return self.t1value_cache[datekey]
        else:
            return (
                self.t1value_cache[datekey],
                datekey[:4] + "-" + datekey[4:6] + "-" + datekey[6:8],
            )

    def get_t1_rate(self, date=None, return_date=True):
        t1v, d = self.get_t1(date=date, return_date=True)
        cp = get_rt(self.code)["current"]
        r = (cp / t1v - 1) * 100
        if return_date:
            return r, d
        else:
            return r

    def get_t0_rate(self, percent=False, return_date=True):
        t0v, d = self.get_t0(percent=percent, return_date=True)
        cp = get_rt(self.code)["current"]
        r = (cp / t0v - 1) * 100
        if return_date:
            return r, d
        else:
            return r

    def _base_value(self, code, shift):
        if not shift:
            funddf = xu.get_daily(code)  ## 获取股指现货日线
            return funddf[funddf["date"] <= last_onday(self.today)].iloc[-1][
                "close"
            ]  # 日线日期是按当地时间
        # TODO: check it is indeed date of last_on(today)
        else:
            code = self.hot_replace(code)
            if code not in self.bar_cache:
                funddf = get_bar(code, prev=168, interval="3600")  ## 获取小时线
                ## 注意对于国内超长假期，prev 可能还不够
                if self.now.hour > 6:  # 昨日美国市场收盘才正常，才缓存参考小时线
                    self.bar_cache[code] = funddf
            else:
                funddf = self.bar_cache[code]
            refdate = last_onday(self.today) + dt.timedelta(days=1)  # 按北京时间校准
            return funddf[funddf["date"] <= refdate + dt.timedelta(hours=shift)].iloc[
                -1
            ][
                "close"
            ]  # 时间是按北京时间, 小时线只能手动缓存，日线不需要是因为自带透明缓存器

    def hot_replace(self, code):
        # 原油切换，避免展期误算实时
        if code in [
            "commodities/brent-oil",
            "commodities/crude-oil",
        ]:
            involvedays = [
                s.strftime("%Y/%m/%d")
                for s in pd.date_range(last_onday(self.today), self.today)
            ]
            st = get_rt(code)
            rl = st["rollover"]
            lrl = st["lastrollover"]
            if rl in involvedays or lrl in involvedays:
                # 可能实时牵涉到展期日，将该油的预测部分切换到另一只做近似
                # 其实对于升水不严重的时候，这一切换也不一定有正效果
                # 但对于升水严重的市场，可以防止实时预测的严重偏离
                # 对于展期交割时实时预测的逻辑正确性与稳定性，还需要进一步实盘验证
                logger.info(
                    "%s is rolling in this period, change to its alternative" % code
                )
                if code.endswith("brent-oil"):
                    code = "commodities/crude-oil"
                else:
                    code = "commodities/brent-oil"
        return code

    def get_t0(self, percent=False, return_date=True):
        """
        获取当日实时净值估计, 该接口每日凌晨到美股收盘（早晨），不保证自洽和可用

        :param percent: bool， default False。现在有两种实时的预测处理逻辑。若 percent 是 True，则将 t0dict 的
            每个持仓标的的今日涨跌幅进行估算，若为 False，则将标的现价和标的对应指数昨日收盘价的比例作为涨跌幅估算。不推荐使用 percent=True.
        :param return_date: bool, default True. return tuple, the second one is date in the format %Y%m%d
        :return: float
        """
        ###########
        # 这里还没有考虑海外标的的拆股合股以及分红的处理逻辑，这些商品基金如果说分红还不太多的话，拆合股可能比较频繁
        # 特别是对于杠杆油基。 英为的数据方面，基金拆合股之后，全部历史数据变化，相当于前复权。
        # 也就是说如果不缓存日线数据的话，预测没有任何问题。但是日线数据我们总是倾向于缓存，这样我们还有个刷新掉最后一天缓存的逻辑在，
        # 也就是说如果开缓存但预测是 positions=False, 不用浮动仓位的话，预测也没任何问题。
        # 但一旦开了浮动仓位预测，拆合股会贡献一个巨大的涨跌幅，这会导致对应日期的即时未平滑仓位变小（因为基金实际涨幅跟不上这个异常涨跌幅）
        # 最终导致 T-1 日仓位预测偏小，从而低估当日的涨跌幅，但应该不会出现方向性的问题。在这里没出现严重错误的原因是，
        # 刷新掉最后一日缓存的逻辑和英为历史数据自动变化前复权。
        # 至于分红，暂时没有样例观察英为如何处理价格，是否会前复权，如果会的话，也不会出现严重问题，只是仓位预估会偏。
        # 想要能估计准，还是建议了解这些变化信息，当天先 refresh=True 手动刷新相关标的的数据，前提是每次对应数据源都有正确复权。
        # 注意：英为似乎并不是总能及时正确的对历史数据前复权。所以需要双重保险，daily_increment 探测到异常增幅的标的进行 refresh 刷新
        # evaluate_fluctuation 可能继续探测到异常，这时直接涨幅置为0。
        #
        # 实际上对于仓位预测，之前几天的 daily increment 可能还有更多的坑，比如说节假日考虑不完善 real， pred 起止时间不对等。
        # 但原则就是仓位的滑动平均可以尽量抑制这种问题，而不至于使其暴露的过于明显。但是如果基准仓位比较偏，比如一季报披露的话，可能有些问题，
        # 会反复造成预估仓位过小。可能需要补一个修正。
        #
        # 此外关于利用基金净值而非市价预测的问题，可以参考：https://github.com/refraction-ray/xalpha/pull/15 的一些讨论。
        ###########

        if not self.t0dict:
            raise ValueError("Please provide t0dict for prediction")
        t1value = self.get_t1(date=None, return_date=False)
        t = 0
        n = 0
        today_str = self.today.strftime("%Y%m%d")
        for k, v in self.t0dict.items():
            if not isinstance(v, dict):
                v = {"weight": v}
            if len(k.split("~")) > 1 and k.split("~")[-1].isdigit():
                # 为了持仓中可以同标的多次出现的 workaround
                k = k.split("~")[0]
            w = v["weight"]
            shift = v.get("time", None)
            base = v.get("base", None)
            t += w
            k = self.hot_replace(k)  # 原油切换
            r = get_rt(
                k
            )  # k should support get_rt, investing pid doesn't support this!
            if percent:
                c = w / 100 * (1 + r["percent"] / 100)  # 直接取标的当日涨跌幅
            else:
                if k in futures_info and not base:
                    kf = futures_info[k]
                elif not base:
                    if k.endswith("-futures"):
                        kf = k[:-8]  # k + "-futures"
                    else:
                        kf = k
                else:
                    kf = base
                try:
                    basev = self._base_value(kf, shift)
                except Exception as e:
                    kf = get_alt(kf)
                    if not kf:
                        raise e
                    else:
                        basev = self._base_value(kf, shift)
                c = w / 100 * r["current"] / basev
            currency_code = get_currency_code(k)
            if currency_code:
                c = c * daily_increment(currency_code, today_str)
                # TODO: 中间价未更新，但实时数据不检查问题也不大
            n += c
        n += (100 - t) / 100
        t0value = n * t1value
        self.t0_delta = n
        if not return_date:
            return t0value
        else:
            return t0value, self.today.strftime("%Y-%m-%d")

    def set_position(self, value, date=None):
        if date is None:
            yesterday = last_onday(self.today)
            datekey = yesterday.strftime("%Y%m%d")
        else:
            datekey = date.replace("/", "").replace("-", "")
        self.position_cache[datekey] = value

    @error_catcher
    def get_position(self, date=None, refresh=False, return_date=True, **kws):
        """
        基于 date 日之前的净值数据，对 date 预估需要的仓位进行计算。

        :param date: str. %Y-%m-%d
        :param refresh: bool, default False. 若为 True，则刷新缓存，重新计算仓位。
        :param return_date: bool, default True. return tuple, the second one is date in the format %Y%m%d
        :param kws: 一些预估仓位可能的超参。包括 window，预估所需的时间窗口，decay 加权平均的权重衰减，smooth 每日仓位处理的平滑函数。以上参数均可保持默认即可获得较好效果。
        :return: float. 0-100. 100 代表满仓。
        """
        if not date:
            date = last_onday(self.today).strftime("%Y%m%d")
        else:
            date = date.replace("/", "").replace("-", "")
        if date not in self.position_cache or refresh:

            fdict = scale_dict(self.t1dict.copy(), aim=100)
            l = kws.get("window", 4)
            q = kws.get("decay", 0.8)
            s = kws.get("smooth", _smooth_pos)
            d = dt.datetime.strptime(date, "%Y%m%d")
            posl = [sum([v for _, v in self.t1dict.items()]) / 100]
            for _ in range(l):
                d = last_onday(d)
            for _ in range(l - 1):
                d = next_onday(d)
                pred = evaluate_fluctuation(
                    fdict,
                    d.strftime("%Y-%m-%d"),
                    lastday=last_onday(d).strftime("%Y-%m-%d"),
                    warning_threhold=(1.8, 0.1),
                )
                real = evaluate_fluctuation(
                    {self.fcode: 100},
                    d.strftime("%Y-%m-%d"),
                    lastday=last_onday(d).strftime("%Y-%m-%d"),
                )
                posl.append(s(real, pred, posl[-1]))
            current_pos = sum([q ** i * posl[l - i - 1] for i in range(l)]) / sum(
                [q ** i for i in range(l)]
            )
            self.position_cache[date] = current_pos
        if not return_date:
            return self.position_cache[date]
        else:
            return (
                self.position_cache[date],
                date[:4] + "-" + date[4:6] + "-" + date[6:8],
            )

    def benchmark_test(self, start, end, **kws):
        """
        对该净值预测模型回测

        :param start: str. 起始日期
        :param end: str. 终止日期
        :param kws: 可选仓位估计的超参。
        :return: pd.DataFrame. real 列为真实涨跌幅，est 列为估计涨跌幅，diff 列为两者之差。
        """
        compare_data = {
            "date": [],
        }
        l = kws.get("window", 4)
        q = kws.get("decay", 0.8)
        c = kws.get("pos", self.position_zero)
        s = kws.get("smooth", _smooth_pos)
        real_holdings = {self.fcode: 100}
        full_holdings = scale_dict(self.t1dict.copy(), aim=100)
        compare_data["est"] = []
        compare_data["real"] = []
        compare_data["estpos3"] = []
        compare_data["estpos1"] = []
        fq = deque([c / 100] * l, maxlen=l)
        current_pos = c / 100
        dl = pd.Series(pd.date_range(start=start, end=end))
        dl = dl[dl.isin(opendate)]
        for j, d in enumerate(dl):
            if j == 0:
                continue
            dstr = d.strftime("%Y%m%d")
            lstdstr = dl.iloc[j - 1].strftime("%Y%m%d")
            compare_data["date"].append(d)
            fullestf = evaluate_fluctuation(
                full_holdings, dstr, lstdstr, warning_threhold=(1.8, 0.1)
            )
            realf = evaluate_fluctuation(real_holdings, dstr, lstdstr)
            estf = fullestf * current_pos
            compare_data["est"].append(estf)
            compare_data["estpos3"].append(current_pos)
            compare_data["estpos1"].append(fq[-1])
            compare_data["real"].append(realf)
            pos = s(realf, fullestf, fq[-1])
            fq.append(pos)
            fq[0] = c / 100  ## 模拟实际的无状态仓位分析
            if self.positions:
                current_pos = sum([q ** i * fq[l - i - 1] for i in range(l)]) / sum(
                    [q ** i for i in range(l)]
                )
                if current_pos > 1:
                    current_pos = 1

        cpdf = pd.DataFrame(compare_data)
        cpdf["diff"] = cpdf["real"] - cpdf["est"]
        self.cpdf = cpdf
        return cpdf

    def analyse(self):
        """
        打印出回测结果的定量分析。

        :return: None
        """
        print("净值预测回测分析:\n")
        self.analyse_deviate(self.cpdf, "diff")
        self.analyse_percentile(self.cpdf, "diff")
        self.analyse_ud(self.cpdf, "real", "diff")

    @staticmethod
    def analyse_ud(cpdf, col1, col2):
        """


        :param cpdf: pd.DataFrame, with col1 as real netvalue and col2 as prediction difference
        :param col1: str.
        :param col2: str.
        :return:
        """
        uu, ud, dd, du, count = 0, 0, 0, 0, 0
        # uu 实际上涨，real-est>0 (预测涨的少)
        # ud 预测涨的多
        # du 预测跌的多
        # dd 预测跌的少
        for i, row in cpdf.iterrows():
            if row[col1] >= 0 and row[col2] > 0:
                uu += 1
            elif row[col1] >= 0 >= row[col2]:
                ud += 1
            elif row[col1] < 0 < row[col2]:
                du += 1
            else:
                dd += 1
            count += 1
        print(
            "\n涨跌偏差分析:",
            "\n预测涨的比实际少: ",
            round(uu / count, 2),
            "\n预测涨的比实际多: ",
            round(ud / count, 2),
            "\n预测跌的比实际多: ",
            round(du / count, 2),
            "\n预测跌的比实际少: ",
            round(dd / count, 2),
        )

    @staticmethod
    def analyse_percentile(cpdf, col):
        percentile = [1, 5, 25, 50, 75, 95, 99]
        r = [round(d, 3) for d in np.percentile(list(cpdf[col]), percentile)]
        print(
            "\n预测偏差分位:",
            "\n1% 分位: ",
            r[0],
            "\n5% 分位: ",
            r[1],
            "\n25% 分位: ",
            r[2],
            "\n50% 分位: ",
            r[3],
            "\n75% 分位: ",
            r[4],
            "\n95% 分位: ",
            r[5],
            "\n99% 分位: ",
            r[6],
        )

    @staticmethod
    def analyse_deviate(cpdf, col):
        l = np.array(cpdf[col])
        d1, d2 = np.mean(np.abs(l)), np.sqrt(np.mean(l ** 2))
        print("\n平均偏离: ", d1, "\n标准差偏离： ", d2)
