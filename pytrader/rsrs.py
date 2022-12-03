import numpy as np
import matplotlib.pyplot as plt

from easyquant.quotation import use_quotation

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import pandas as pd
import datetime
import jqdatasdk as jq
from easytrader.utils.misc import file2dict

config = file2dict('jqdata.json')
jq.auth(config["user"], config["password"])
quotation = use_quotation('jqdata')


class ETFQuant:
    # 初始化函数
    def __init__(self, stkList):
        self.edate = datetime.date.today()
        self.date = pd.to_datetime(self.edate)
        if self.date.dayofweek + 1 in [6, 7]:  # 剔除周末的日期，避免混淆
            self.date = self.date - datetime.timedelta(self.date.dayofweek - 4)
        #         print('today:',self.edate)
        self.stock_pool = stkList
        self.mom = 20
        self.ref = '000300.XSHG'
        self.N, self.M = 17, 400
        self.RSRS_threshold = 0.7

    # 20日收益率动量拟合取斜率最大的
    def get_rank(self):
        self.slope_series = self.initial_slope_series()[:-1]
        rank = []
        for stock in self.stock_pool:
            data = jq.get_price(stock, end_date=self.date, count=self.mom)
            score = np.polyfit(np.arange(len(data)), data.close / data.close[0], 1)[0]
            rank.append([stock, 100 * score])
        rank.sort(key=lambda x: x[-1], reverse=True)
        return rank[0]

    def get_ols(self, x, y):
        try:
            slope, intercept = np.polyfit(x, y, 1)
            r2 = 1 - (sum((y - (slope * x + intercept)) ** 2) / ((len(y) - 1) * np.var(y, ddof=1)))
            return (intercept, slope, r2)
        except Exception as e:
            print(e)

    def initial_slope_series(self):
        data = jq.get_price(self.ref, end_date=self.date, count=self.M + self.N, fields=['high', 'low'])
        return [self.get_ols(data.low[i:i + self.N], data.high[i:i + self.N])[1] for i in range(self.M)]

    # 因子标准化
    def get_zscore(self, slope_series):
        mean = np.mean(slope_series)
        std = np.std(slope_series)
        return (slope_series[-1] - mean) / std

    def get_rsrs_score(self, stock_code, days=60, slop_days=18, M=400, MA=10,buy_sail = 0.7, sail_score = -1.4):
        self.M = M
        # m + n + days
        data = quotation.get_bars(stock_code, self.M + slop_days + days,
                                  fields=['close', 'high', 'low'],
                                  end_dt=self.date)
        data['ma'] = data.close.rolling(MA).mean()
        # M+days
        ols_data = [self.get_ols(data.low[i:i + slop_days], data.high[i:i + slop_days]) for i in range(self.M + days)]
        slope_series = [ols_data[i][1] for i in range(self.M + days)]
        r2 = [ols_data[i][2] for i in range(self.M + days)]
        result = []
        signal = []
        position = 1  # 是否持仓，持仓：1，不持仓：0
        last_rsrs_score = 0
        last_ma = data.ma[self.M -1]
        # > -1.2 持仓
        # 最近的N天
        for i in range(days):
            current_ma = data.ma[self.M + i]
            close = data.close[self.M + i]
            rsrs_score = self.get_zscore(slope_series[i:self.M + i]) * r2[self.M + i]
            # M 天序列
            result.append(rsrs_score)
            signal.append(position)
            if rsrs_score < sail_score:
                position = 0
            # 10日线拐头
            elif (rsrs_score > buy_sail and current_ma > last_ma):
                position = 1
            last_rsrs_score = rsrs_score
            last_ma = current_ma

        return result, slope_series[-days:], signal, data.close[-days:].values

    def get_timing_signal(self, stock_code):
        high_low_data = jq.get_price(stock_code, end_date=self.date, count=self.N, fields=['high', 'low'])
        intercept, slope, r2 = self.get_ols(high_low_data.low, high_low_data.high)
        self.slope_series.append(slope)
        rsrs_score = self.get_zscore(self.slope_series[-self.M:]) * r2
        global RSRS
        RSRS.append(rsrs_score)
        #         print("rsrs factor:\t\t{:.3f}".format(rsrs_score))
        if rsrs_score > self.RSRS_threshold:
            return "BUY"
        elif rsrs_score < -self.RSRS_threshold:
            return "SELL"
        else:
            return "KEEP"

    def run(self, date=datetime.date.today()):
        self.date = pd.to_datetime(date)
        if self.date.dayofweek + 1 in [6, 7]:  # 剔除周末的日期，避免混淆
            self.date = date - datetime.timedelta(self.date.dayofweek - 4)
        check_out_list = self.get_rank()
        timing_signal = self.get_timing_signal()
        return [self.date.strftime('%Y-%m-%d'), check_out_list, timing_signal]


fig, axes = plt.subplots(3, 1, sharex=True, figsize=(18, 12))

# , '000300.XSHG'['159949.XSHE'
stkList = ['002230']
eq = ETFQuant(stkList)
days = 240
# trading_dates = get_trade_da0ys(end_date=eq.date, count=eq.N)
trading_dates = jq.get_trade_days(end_date=eq.date, count=days)
RSRS = pd.DataFrame([0 for i in range(days)], index=trading_dates, columns=['0'])
stock_price = pd.DataFrame([1 for i in range(days)], index=trading_dates, columns=['1'])
slope = pd.DataFrame([1 for i in range(days)], index=trading_dates, columns=['1'])

def get_payments(stock_code, days, slop_days=18, M=400, MA=10,buy_sail = 0.7, sail_score = -1.4):
    data = eq.get_rsrs_score(stock_code, days, slop_days, M, MA, buy_sail, sail_score)
    RSRS[stock_code + "ma18"] = data[0]
    slope[stock_code + "ma18"] = data[1]

    # data = eq.get_rsrs_score(stock_code, days, 5)
    # RSRS[stock_code+"ma5"] = data[0]
    # slope[stock_code+"ma5"] = data[1]

    # data = eq.get_rsrs_score(stock_code, days, 10)
    # RSRS[stock_code + "ma10"] = data[0]
    # slope[stock_code + "ma10"] = data[1]

    stock_price[stock_code] = data[3]
    stock_price[stock_code + "策略"] = (1 + stock_price[stock_code].pct_change(1).fillna(0) * data[2]).cumprod()
    # stock_price[stock_code] = stock_price[stock_code].pct_change(1)
    stock_price[stock_code] = stock_price[stock_code] / stock_price[stock_code][0]
    stock_price[stock_code+"signal"] = data[2]

    print("days=%s, slop_days=%s, M=%s, MA=%s,buy_sail = %s, sail_score = %s 基准收益率: %s 收益率: %s" % (days, slop_days, M,
                                                                                                  MA,
                                                                                         buy_sail,sail_score,
                                                                                         stock_price[stock_code][-1],
                                                                                            stock_price[stock_code + "策略"][
        -1]))

# get_payments('002230', days, slop_days=10, M=200, MA=1, buy_sail = 0.8, sail_score = -0.9 )
get_payments('002230', days, slop_days=18, M=600, MA=10,buy_sail = 0.8, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=600, MA=10,buy_sail = 0.6, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=600, MA=10,buy_sail = 0.5, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=600, MA=10,buy_sail = 0.4, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=600, MA=10,buy_sail = 0.8, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.7, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.6, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.5, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.4, sail_score = -1.4 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.8, sail_score = -1.5 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.7, sail_score = -1.5 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.6, sail_score = -1.5 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.5, sail_score = -1.5 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.4, sail_score = -1.5 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.8, sail_score = -1.3 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.7, sail_score = -1.3 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.6, sail_score = -1.3 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.5, sail_score = -1.3 )
# get_max_args('002230', days, slop_days=18, M=400, MA=10,buy_sail = 0.4, sail_score = -1.3 )
# # print("now:", datetime.datetime.now())
# for date in trading_dates: print('target and signal:\t', eq.run(date))

RSRS['买'] = 0.8
RSRS['卖'] = -0.9
RSRS.plot(ax=axes[1], title='score', grid=True)
slope.plot(ax=axes[2], title='斜率', grid=True)
stock_price.plot(ax=axes[0], title='价格', grid=True)
#
plt.show()
# get_price('159949.XSHE', end_date=datetime.date.today(), count=3)
