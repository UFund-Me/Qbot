# ======================================================================================================================
# 导入必要的库
# ======================================================================================================================

import io
from datetime import datetime

import backtrader as bt
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta

# ======================================================================================================================
# 配置数据
# ======================================================================================================================

# 设置Amberdata的API_KEY，以便从Amberdata下载行情数据
Amberdata_API_KEY = "YOUR_API_KEY"

# 初始资金
icap = 100000

# 每次交易投入的仓位百分比
PercSize = 100

# 追踪停损百分比
PercTrail = 0.40

# 回测时段
start_date = "2015-01-20"
end_date = "2020-05-09"


# ======================================================================================================================
# 帮助类和函数 - 数据源
# ======================================================================================================================
# 定义一个新的pandas data feed，加入线 stf
class CustomPandas(bt.feeds.PandasData):
    # Add a 'stf' line to the inherited ones from the base class
    lines = ("stf",)
    # sft默认在dataframe的第8列
    params = (("stf", 8),)


# 调用 Amberdata 的 在线API
def amberdata(url, queryString, apiKey):
    try:
        headers = {"x-api-key": apiKey}
        response = requests.request("GET", url, headers=headers, params=queryString)
        return response.text
    except Exception as e:
        raise e


# 从 Amberdata获取日线行情数据
def amberdata_ohlcv(exchange, symbol, startDate, endDate):
    format = "%Y-%m-%dT%H:%M:%S"
    startTimestamp = datetime.strptime(startDate, "%Y-%m-%d")
    endTimestamp = datetime.strptime(endDate, "%Y-%m-%d")

    current = startTimestamp
    next = current
    fields = "timestamp,open,high,low,close,volume"
    payload = fields
    while current < endTimestamp:
        next += relativedelta(years=1)
        if next > endTimestamp:
            next = endTimestamp
        print("Retrieving OHLCV between", current, " and ", next)
        result = amberdata(
            "https://web3api.io/api/v2/market/ohlcv/" + symbol + "/historical",
            {
                "exchange": exchange,
                "timeInterval": "days",
                "timeFormat": "iso",
                "format": "raw_csv",
                "fields": fields,
                "startDate": current.strftime(format),
                "endDate": next.strftime(format),
            },
            Amberdata_API_KEY,
        )
        payload += "\n" + result
        current = next

    return payload


# 获取stf指标数据
def amberdata_stf(symbol, startDate, endDate):
    print("Retrieving STF between", startDate, " and ", endDate)
    return amberdata(
        "https://web3api.io/api/v2/market/metrics/"
        + symbol
        + "/historical/stock-to-flow",
        {
            "format": "csv",
            "timeFrame": "day",
            "startDate": startDate,
            "endDate": endDate,
        },
        Amberdata_API_KEY,
    )


def to_pandas(csv):
    return pd.read_csv(io.StringIO(csv), index_col="timestamp", parse_dates=True)


# ======================================================================================================================
# 策略
# ======================================================================================================================


class Strategy(bt.Strategy):
    params = (
        ("macd1", 12),
        ("macd2", 26),
        ("macdsig", 9),
        ("trailpercent", PercTrail),
        ("smaperiod", 30),
        ("dirperiod", 10),
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # No pending orders

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data,
            period_me1=self.p.macd1,
            period_me2=self.p.macd2,
            period_signal=self.p.macdsig,
        )

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # 移动均线。
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        # 当日移动均线与dirperiod期前移动均线的差值，若小于0，说明市场处于跌势
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def start(self):
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:  # 无仓位
            # 如果macd金叉，并且当日移动均值比dirperiod前的低，并且收盘价低于stf，则买入
            # 基本思想是当市场处于跌势、且价格低估时，若出现macd金叉，则买入
            if (
                self.mcross[0] > 0.0
                and self.smadir < 0.0
                and self.data.close < self.data.stf
            ):
                self.order = self.buy()

        # 若有仓位
        elif self.order is None:
            # 发出停损跟踪单，保护自己
            self.order = self.sell(
                exectype=bt.Order.StopTrail, trailpercent=self.p.trailpercent
            )


# ======================================================================================================================
# 主程序开始
# ======================================================================================================================


cerebro = bt.Cerebro(stdstats=False)
cerebro.broker.setcash(icap)

# addsizer设置下单量管理者
cerebro.addsizer(bt.sizers.PercentSizer, percents=PercSize)

# Add our strategy
cerebro.addstrategy(Strategy)

# 通过amberdata api获取gdax交易所的比特币行情数据，放到dataframe
btc = to_pandas(amberdata_ohlcv("gdax", "btc_usd", start_date, end_date))
btc.to_csv("btc_new.csv")
# 获取stf指标
btc_stf = to_pandas(amberdata_stf("btc", start_date, end_date))
# 将stf指标合并到行情数据帧
btc["stf"] = btc_stf["price"]

# 注入数据
cerebro.adddata(CustomPandas(dataname=btc, openinterest=None, stf="stf"))

# 运行回测
backtest = cerebro.run()
