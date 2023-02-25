# -*- coding: utf-8 -*-
"""
module for implementation of indicator class, which is designed as MinIn for systems with netvalues
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid
from pyecharts.commons.utils import JsCode

from xalpha.cons import line_opts, opendate, yesterdayobj, sqrt_days_in_year


def _upcount(ls):
    """
    count the ratio of upmove days by given a list
    """
    count = 0
    for i in range(len(ls) - 1):
        # somehow after pandas 0.23(22?), the input is a series(dataframe?) and old list supporting syntax are illegal
        if ls.iloc[i + 1] > ls.iloc[i]:
            count += 1
    return count / (len(ls) - 1)


class indicator:
    """
    MixIn class provide quant indicator tool box which is desinged as interface for mulfix class as well
    as info class, who are both treated as a single fund with price table of net value.
    Most of the quant indexes, their name conventions, definitions and calculations are from
    `joinquant <https://www.joinquant.com/help/api/help?name=api#%E9%A3%8E%E9%99%A9%E6%8C%87%E6%A0%87>`_.
    Make sure first run obj.bcmkset() before you want to use functions in this class.
    """

    def bcmkset(self, infoobj, start=None, riskfree=0.0371724, name="基金组合"):
        """
        Once you want to utilize the indicator tool box for analysis, first run bcmkset function to set
        the benchmark, otherwise most of the functions would raise error.

        :param infoobj: info obj, whose netvalue are used as benchmark
        :param start: datetime obj, indicating the starting date of all analysis.
            Note if use default start, there may be problems for some fundinfo obj, as lots of
            funds lack netvalues of several days from our API, resulting unequal length between
            benchmarks and fund net values.
        :param riskfree: float, annual rate in the unit of 100%, strongly suggest make this value
            consistent with the interest parameter when instanciate cashinfo() class
        """
        self._pricegenerate(name)
        if start is None:
            self.start = self.price.iloc[0].date
        elif isinstance(start, str):
            self.start = pd.to_datetime(
                start, format="%Y-%m-%d"
            )  # pd.Timestamp.strptime(start, "%Y-%m-%d")
        self.benchmark = infoobj

        self.riskfree = riskfree
        self.bmprice = self.benchmark.price[self.benchmark.price["date"] >= self.start]
        self.price = self.price[self.price["date"] >= self.start]
        self.bmprice = self.bmprice[self.bmprice["date"].isin(self.price["date"])]
        self.price = self.price[self.price["date"].isin(self.bmprice["date"])]

    # the price data is removed from the infoobj before start date

    def _pricegenerate(self, name):
        """
        generate price table for mulfix class, the cinfo class has this attr by default
        """
        if getattr(self, "price", None) is None:  # 基金组合类，而非基金信息类
            times = pd.date_range(self.totcftable.iloc[0].date, yesterdayobj())
            netvalue = []
            for date in times:
                netvalue.append(self.unitvalue(date))  # may take a long time
            self.price = pd.DataFrame(data={"date": times, "netvalue": netvalue})
            self.price = self.price[self.price["date"].isin(opendate)]
            self.name = name

    def comparison(self, date=yesterdayobj()):
        """
        :returns: tuple of two pd.Dataframe, the first is for aim and the second if for the benchmark index
            all netvalues are normalized and set equal 1.00 on the self.start date
        """
        partp = self.price[self.price["date"] <= date]
        partm = self.bmprice[self.bmprice["date"] <= date]
        normp = partp.iloc[0].netvalue
        normm = partm.iloc[0].netvalue
        partp["netvalue"] = partp["netvalue"] / normp
        partm["netvalue"] = partm["netvalue"] / normm
        return (partp, partm)

    def total_return(self, date=yesterdayobj()):
        return round(
            (
                self.price[self.price["date"] <= date].iloc[-1].netvalue
                - self.price.iloc[0].netvalue
            )
            / self.price.iloc[0].netvalue,
            4,
        )

    @staticmethod
    def annualized_returns(price, start, date=yesterdayobj()):
        """
        :param price: price table of info().price
        :param start: datetime obj for starting date of calculation
        :param date: datetime obj for ending date of calculation
        :returns: float, annualized returns of the price table
        """
        datediff = (price[price["date"] <= date].iloc[-1].date - start).days
        totreturn = (
            price[price["date"] <= date].iloc[-1].netvalue - price.iloc[0].netvalue
        ) / price.iloc[0].netvalue
        return round((1 + totreturn) ** (365 / datediff) - 1, 4)

    def total_annualized_returns(self, date=yesterdayobj()):
        return indicator.annualized_returns(self.price, self.start, date)

    def benchmark_annualized_returns(self, date=yesterdayobj()):
        return indicator.annualized_returns(self.bmprice, self.start, date)

    def pct_chg(self, freq="Y", benchmark=True):
        """
        年度，月，周涨幅统计

        :param freq: str, default Y, could be M or W or anything pd.date_range accepts
        :return: pd.DataFrame with columns date and pct_chg
        """
        if getattr(self, "bmprice", None) is None:
            benchmark = False

        ydf = pd.merge_asof(
            pd.DataFrame(
                pd.date_range(
                    self.price["date"].iloc[0], self.price["date"].iloc[-1], freq=freq
                ),
                columns=["date"],
            ),
            self.price,
        )
        ydf["pct_chg"] = ydf["netvalue"].pct_change()
        if benchmark:
            ydf = pd.merge_asof(ydf, self.bmprice, on="date", suffixes=["", "_bc"])
            ydf["pct_chg_benchmark"] = ydf["netvalue_bc"].pct_change()
            ydf["pct_chg_difference"] = ydf["pct_chg"] - ydf["pct_chg_benchmark"]
            return ydf[["date", "pct_chg", "pct_chg_benchmark", "pct_chg_difference"]]

        return ydf[["date", "pct_chg"]]

    def beta(self, date=yesterdayobj()):
        bcmk = indicator.ratedaily(self.bmprice, date)
        bt = indicator.ratedaily(self.price, date)
        df = pd.DataFrame(data={"bcmk": bcmk, "bt": bt})
        res = df.cov()
        return res.loc["bcmk", "bt"] / res.loc["bcmk", "bcmk"]

    def alpha(self, date=yesterdayobj()):
        rp = self.total_annualized_returns(date)
        rm = self.benchmark_annualized_returns(date)
        beta = self.beta(date)
        return rp - (self.riskfree + beta * (rm - self.riskfree))

    def correlation_coefficient(self, date=yesterdayobj()):
        """
        correlation coefficient between aim and benchmark values,
            可以很好地衡量指数基金的追踪效果

        :returns: float between -1 and 1
        """
        bcmk = indicator.ratedaily(self.bmprice, date)
        bt = indicator.ratedaily(self.price, date)
        df = pd.DataFrame(data={"bcmk": bcmk, "bt": bt})
        res = df.cov()
        return res.loc["bcmk", "bt"] / (
            (res.loc["bcmk", "bcmk"] ** 0.5) * res.loc["bt", "bt"] ** 0.5
        )

    @staticmethod
    def ratedaily(price, date=yesterdayobj()):
        partp = price[price["date"] <= date]
        return list(partp["netvalue"].pct_change())[1:]
        # return [
        #     (partp.iloc[i + 1].netvalue - partp.iloc[i].netvalue)
        #     / partp.iloc[i].netvalue
        #     for i in range(len(partp) - 1)
        # ]

    @staticmethod
    def volatility(price, date=yesterdayobj()):
        df = pd.DataFrame(data={"rate": indicator.ratedaily(price, date)})
        return df.std().rate * sqrt_days_in_year

    def algorithm_volatility(self, date=yesterdayobj()):
        return indicator.volatility(self.price, date)

    def benchmark_volatility(self, date=yesterdayobj()):
        return indicator.volatility(self.bmprice, date)

    def sharpe(self, date=yesterdayobj()):
        rp = self.total_annualized_returns(date)
        return (rp - self.riskfree) / self.algorithm_volatility(date)

    def information_ratio(self, date=yesterdayobj()):
        rp = self.total_annualized_returns(date)
        rm = self.benchmark_annualized_returns(date)
        vp = indicator.ratedaily(self.price, date)
        vm = indicator.ratedaily(self.bmprice, date)
        diff = [vp[i] - vm[i] for i in range(len(vm))]
        df = pd.DataFrame(data={"rate": diff})
        var = df.std().rate
        var = var * sqrt_days_in_year
        return (rp - rm) / var

    def max_drawdown(self, date=yesterdayobj()):
        """
        回测时间段的最大回撤

        :param date: date obj or string
        :returns: three elements tuple, the first two are the date obj of
            start and end of the time window, the third one is the drawdown amplitude in unit 1.
        """
        li = [
            (row["date"], row["netvalue"])
            for i, row in self.price[self.price["date"] <= date].iterrows()
        ]
        res = []
        for i, _ in enumerate(li):
            for j in range(i + 1, len(li)):
                res.append((li[i][0], li[j][0], (li[j][1] - li[i][1]) / li[i][1]))
        return min(res, key=lambda x: x[2])

    ## 以上基本为聚宽提供的整体量化指标，以下是其他短线技术面指标

    def ma(self, window=5, col="netvalue"):
        """
        移动平均线指标
        give the moving average as a new column 'MA' in the price table, return None

        :param window: the date window of the MA calculation
        :param col: string, column name in dataframe you want to calculate
        """
        self.price["MA" + str(window)] = self.price[col].rolling(window=window).mean()

    def md(self, window=5, col="netvalue"):
        """
        移动标准差指标
        give the moving standard deviation as a new column 'MD' in the price table, return None

        :param window: the date window of the MD calculation
        :param col: string, column name in dataframe you want to calculate
        """
        self.price["MD" + str(window)] = self.price[col].rolling(window=window).std()

    def ema(self, window=5, col="netvalue"):
        """
        指数平均数指标
        give the exponential moving average as a new column 'EMA' in the price table, return None

        :param window: the span of date, where the decay factor alpha=2/(1+window)
        :param col: string, column name in dataframe you want to calculate
        """
        self.price["EMA" + str(window)] = self.price[col].ewm(span=window).mean()

    def macd(self, fast_window=12, slow_window=26, signal_window=9, col="netvalue"):
        """
        指数平滑异同移动平均线
        give the MACD index as three new columns 'MACD_DIFF/DEM/OSC' in the price table, return None

        :param fast_window: int,
        :param slow_window: int,
        :param signal_window: int, the ema window of the signal line
        :param col: string, column name in dataframe you want to calculate
        """
        EMAfast = pd.Series(self.price[col].ewm(span=fast_window).mean())
        EMAslow = pd.Series(self.price[col].ewm(span=slow_window).mean())
        # 短期ema和长期ema的差
        MACDDiff = pd.Series(EMAfast - EMAslow)
        # 该差的再次 ema 平均
        MACDDem = pd.Series(MACDDiff.ewm(span=signal_window).mean())
        # ema平均过的差和原来差的差
        MACDOsc = pd.Series(MACDDiff - MACDDem)
        self.price["MACD_DIFF_" + str(fast_window) + "_" + str(slow_window)] = MACDDiff
        self.price["MACD_DEM_" + str(fast_window) + "_" + str(slow_window)] = MACDDem
        self.price["MACD_OSC_" + str(fast_window) + "_" + str(slow_window)] = MACDOsc

    def mtm(self, window=10, col="netvalue"):
        """
        动量指标，并未附加动量的平均线指标，如需计算动量平均线指标，使用ma或emca函数，col参数选择MTM列即可
        give the MTM as a new column 'MTM' in the price table, return None

        :param window: int, the difference between price now and window days ago
        :param col: string, column name in dataframe you want to calculate
        """
        self.price["MTM" + str(window)] = self.price[col].diff(window)

    def roc(self, window=10, col="netvalue"):
        """
        变动率指标
        give the ROC as a new column 'ROC' in the price table, return None, the ROC is in the unit of 1 instead of 1%

        :param window: int, the change rate between price now and window days ago
        :param col: string, column name in dataframe you want to calculate
        """
        abdiff = self.price[col].diff(window)
        deno = self.price[col].shift(window)
        reladiff = pd.Series(abdiff / deno)
        self.price["ROC" + str(window)] = reladiff

    def boll(self, window=10, deviation=2, col="netvalue"):
        """
        布林线上下轨计算
        give the bolling upper and lower band in the price table, the middle line is just ma line

        :param window: int, the date window for ma and md
        :param deviation: int or float, how many times deviation of sigma
        :param col: string, column name in dataframe you want to calculate
        """
        self.ma(window=window, col=col)
        self.md(window=window, col=col)
        self.price["BOLL_UPPER"] = (
            self.price["MA" + str(window)] + deviation * self.price["MD" + str(window)]
        )
        self.price["BOLL_LOWER"] = (
            self.price["MA" + str(window)] - deviation * self.price["MD" + str(window)]
        )

    def bias(self, window=10, col="netvalue"):
        """
        乖离率
        give the bias as BIAS column in price table

        :param window: int, MA_window
        :param col: string, column name in dataframe you want to calculate
        """
        self.ma(window=window, col=col)
        self.price["BIAS" + str(window)] = (
            self.price[col] - self.price["MA" + str(window)]
        ) / self.price["MA" + str(window)]

    def rsi(self, window=14, col="netvalue"):
        """
        相对强弱指标
        give the rsi as RSI column in price table

        :param window: int, MA_window
        :param col: string, column name in dataframe you want to calculate
        """
        i = 0
        UpI = [0]
        DoI = [0]
        while i + 1 <= len(self.price) - 1:
            Move = self.price.loc[i + 1, col] - self.price.loc[i, col]
            if Move > 0:
                UpD = Move
                DoD = 0
            else:
                UpD = 0
                DoD = -Move
            UpI.append(UpD)
            DoI.append(DoD)
            i = i + 1

        UpI = pd.Series(UpI)
        DoI = pd.Series(DoI)
        PosDI = pd.Series(UpI.ewm(span=window).mean())
        NegDI = pd.Series(DoI.ewm(span=window).mean())
        self.price["RSI" + str(window)] = pd.Series(PosDI / (PosDI + NegDI))

    def kdj(self, rsv_window=9, k_window=3, d_window=3, col="netvalue"):
        """
        KDJ 随机指标
        由于该模块不涉及日内高低价的信息，因此区间最高价最低价都由极值收盘价代替，因此和其他软件计算的 kdj 指标可能存在出入。
        give k,d,j indexes as three columns KDJ_K/D/J in price table

        :param rsv_window: int
        :param k_window: int
        :param d_window: int
        :param col: string, column name in dataframe you want to calculate
        """
        roll = self.price[col].rolling(window=rsv_window)
        rsv = (self.price[col] - roll.min()) / (roll.max() - roll.min())
        k = rsv.rolling(window=k_window).mean()
        d = k.rolling(window=d_window).mean()
        j = 3 * k - 2 * d
        self.price["KDJ_K"] = k
        self.price["KDJ_D"] = d
        self.price["KDJ_J"] = j

    def wnr(self, window=14, col="netvalue"):
        """
        威廉指标，这里取超卖结果接近0的约定(wnr*-1)，事实上就是 rsv, 同样的区间极值价用极值收盘价替代
        give williams %R in WNR column in price table

        :param window: int
        :param col: string, column name in dataframe you want to calculate
        """
        roll = self.price[col].rolling(window=window)
        wnr = (self.price[col] - roll.min()) / (roll.max() - roll.min())
        self.price["WNR" + str(window)] = wnr

    def dma(self, fast_window=10, slow_window=50, ama_window=10, col="netvalue"):
        """
        平行线差指标
        give different of moving average as columns DMA and AMA in price table

        :param fast_window: int
        :param slow_window: int
        :param ama_window:  int
        :param col: string, column name in dataframe you want to calculate
        """
        dma = (
            self.price[col].rolling(window=fast_window).mean()
            - self.price[col].rolling(window=slow_window).mean()
        )
        ama = dma.rolling(window=ama_window).mean()
        self.price["DMA"] = dma
        self.price["AMA"] = ama

    def bbi(self, col="netvalue"):
        """
        多空指标
        give bull and bear line in column BBI in price table

        :param col: string, column name in dataframe you want to calculate
        """
        bbi = self.price[col].rolling(3).mean()
        bbi = bbi + self.price[col].rolling(6).mean()
        bbi = bbi + self.price[col].rolling(12).mean()
        bbi = bbi + self.price[col].rolling(24).mean()
        bbi = bbi / 4
        self.price["BBI"] = bbi

    def trix(self, window=10, ma_window=10, col="netvalue"):
        """
        三重指数平滑平均线
        give the trix index in column TRIX, TRMA

        :param window: int
        :param col: string, column name in dataframe you want to calculate
        """
        tr = self.price[col].ewm(span=window).mean()
        tr = tr.ewm(span=window).mean()
        tr = tr.ewm(span=window).mean()
        trix = tr.diff(1) / tr.shift(1)
        trma = trix.rolling(ma_window).mean()
        self.price["TRIX" + str(window)] = trix
        self.price["TRMA" + str(window)] = trma

    def psy(self, count_window=12, ma_window=6, col="netvalue"):
        """
        心理线指标（衡量过去 count_window 天涨幅天数）
        give psy and psyma as column PSY and PSYMA in price table

        :param count_window: int
        :param ma_window: int
        :param col: string, column name in dataframe you want to calculate
        """
        psy = self.price[col].rolling(count_window + 1).aggregate(_upcount)
        psyma = psy.rolling(ma_window).mean()
        self.price["PSY" + str(count_window)] = psy
        self.price["PSYMA" + str(count_window)] = psyma

    ## 以下是可视化部分

    def v_netvalue(self, end=yesterdayobj(), benchmark=True, rendered=True, vopts=None):
        """
        visulaization on  netvalue curve

        :param end: dateobject for indicating the end date in the figure, default to yesterday
        :param benchmark: bool, whether include benchmark's netvalue curve, default true
        :param vopts: dict, options for pyecharts instead of builtin settings
        """
        if getattr(self, "bmprice", None) is None:
            benchmark = False
        if benchmark:
            a, b = self.comparison(end)
        else:
            a = self.price
        if vopts is None:
            vopts = line_opts
        line = Line()
        line.add_xaxis([d.date() for d in list(a.date)])
        line.add_yaxis(
            y_axis=list(a.netvalue), series_name=self.name, is_symbol_show=False
        )
        line.set_global_opts(**vopts)
        if benchmark:
            line.add_yaxis(
                series_name=self.benchmark.name,
                y_axis=list(b.netvalue),
                is_symbol_show=False,
            )
        if rendered:
            return line.render_notebook()
        else:
            return line

    def v_techindex(self, end=yesterdayobj(), col=None, rendered=True, vopts=None):
        """
        visualization on netvalue curve and specified indicators

        :param end: date string or obj, the end date of the figure
        :param col: list, list of strings for price col name, eg.['MA5','BBI']
            remember generate these indicators before the visualization,
            these cols don't automatically generate for visualization
        :param vopts: dict, options for pyecharts instead of builtin settings
        """
        partprice = self.price[self.price["date"] <= end]
        xdata = [d.date() for d in list(partprice.date)]
        netvaldata = list(partprice.netvalue)
        if vopts is None:
            vopts = line_opts
        line = Line()
        line.add_xaxis(xdata)
        line.add_yaxis(series_name="netvalue", y_axis=netvaldata, is_symbol_show=False)
        line.set_global_opts(**vopts)
        if col is not None:
            for ind in col:
                inddata = list(partprice[ind])
                line.add_yaxis(series_name=ind, y_axis=inddata, is_symbol_show=False)
        if rendered:
            return line.render_notebook()
        else:
            return line


def plot_kline(
    df,
    rendered=True,
    ucolor="#ef232a",
    dcolor="#14b143",
    ucolorborder=None,
    dcolorborder=None,
    ucolorvolume=None,
    dcolorvolume=None,
    col="",
):
    """
    针对 dataframe 直接画出标准看盘软件的上k线图下成交量图的形式

    :param df:
    :param rendered:
    :param ucolor: str for color when going up, default red in A stock as "#ef232a"
    :param dcolor: str for color when going down, default green in A stock as "#14b143"
    :param col:
    :return:
    """
    # TODO: color changing seems to make no effect, possible issue with pyecharts
    if ucolorborder is None:
        ucolorborder = ucolor
    if dcolorborder is None:
        dcolorborder = dcolor
    if ucolorvolume is None:
        if ucolor != "#ffffff":
            ucolorvolume = ucolor
        else:
            ucolorvolume = ucolorborder
    if dcolorvolume is None:
        if dcolor != "#ffffff":
            dcolorvolume = dcolor
        else:
            dcolorvolume = dcolorborder

    kline = (
        Kline()
        .add_xaxis(xaxis_data=list(df["date"]))
        .add_yaxis(
            series_name="",
            itemstyle_opts=opts.ItemStyleOpts(
                color=ucolor,
                color0=dcolor,
                border_color=ucolorborder,  # ucolor,
                border_color0=dcolorborder,  # dcolor,
            ),
            y_axis=list(zip(df["open"], df["close"], df["low"], df["high"])),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ],
                symbol="pin",
                symbol_size=[56, 40],
                # label_opts=opts.LabelOpts(color="#CCFFFF",position=["top", "bottom"])
            ),
        )
        .set_global_opts(
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    type_="slider",
                    range_start=50,
                    range_end=100,
                    xaxis_index=[0, 1],
                ),
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    range_start=50,
                    range_end=100,
                    xaxis_index=1,
                ),
            ],
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis",
                trigger_on="mousemove",
                axis_pointer_type="cross",
            ),
        )
    )
    if col is not None:
        for c in col:
            line = (
                Line()
                .add_xaxis(xaxis_data=list(df["date"]))
                .add_yaxis(
                    series_name=c,
                    y_axis=list(df[c]),
                    is_smooth=True,
                    linestyle_opts=opts.LineStyleOpts(opacity=0.5),
                    label_opts=opts.LabelOpts(is_show=False),
                )
            )
            kline = kline.overlap(line)

    if "volume" in df.columns:
        vl = list(df["volume"])
    elif "amount" in df.columns:
        vl = list(df["amount"])
    else:
        vl = [0 for _ in range(len(df))]
    bar = (
        Bar()
        .add_js_funcs("var barData = {}".format(list(df["close"] - df["open"])))
        .add_xaxis(xaxis_data=list(df["date"]))
        .add_yaxis(
            series_name="",
            yaxis_data=vl,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    """
                function(params) {{
                    var colorList;
                    if (barData[params.dataIndex]>0) {{
                        colorList = '{ucolor}';
                    }} else {{
                        colorList = '{dcolor}';
                    }}
                    return colorList;
                }}
                """.format(
                        ucolor=ucolorvolume, dcolor=dcolorvolume
                    )
                )  # escape {} when using format
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis",
                trigger_on="mousemove",
                axis_pointer_type="cross",
            ),
        )
    )
    grid_chart = Grid()
    grid_chart.add_js_funcs("var barData = {}".format(list(df["close"] - df["open"])))
    grid_chart.add(
        kline,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="1%", pos_top="2%", height="65%"
        ),
    )

    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="1%", pos_top="71%", height="22%"
        ),
    )
    if rendered:
        return grid_chart.render_notebook()
    else:
        return grid_chart


pd.DataFrame.v_kline = plot_kline
