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

date = pd.to_datetime(datetime.date.today())
if date.dayofweek + 1 in [6, 7]:  # 剔除周末的日期，避免混淆
    date = date - datetime.timedelta(date.dayofweek - 4)

max_score = 0


def get_ols(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    r2 = 1 - (sum((y - (slope * x + intercept)) ** 2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return intercept, slope, r2


def get_zscore(slope_series):
    mean = np.mean(slope_series)
    std = np.std(slope_series)
    return (slope_series[-1] - mean) / std


def get_rsrs_score(stock_code, days=60, slop_days=18, M=400, MA=10, buy_score=0.7, sail_score=-1.4, use_ma=1):
    # m + n + days
    data = quotation.get_bars(stock_code, M + slop_days + days,
                              fields=['close', 'high', 'low'],
                              end_dt=date)
    data['ma'] = data.close.rolling(MA).mean()
    # M+days
    ols_data = [get_ols(data.low[i:i + slop_days], data.high[i:i + slop_days]) for i in range(M + days)]
    slope_series = [ols_data[i][1] for i in range(M + days)]
    r2 = [ols_data[i][2] for i in range(M + days)]
    result = []
    signal = []
    position = 0  # 是否持仓，持仓：1，不持仓：0
    last_rsrs_score = 0
    last_ma = data.ma[M - 1]
    # > -1.2 持仓
    # 最近的N天
    for i in range(days):
        current_ma = data.ma[M + i]
        close = data.close[M + i]
        rsrs_score = get_zscore(slope_series[i:M + i]) * r2[M + i]
        # M 天序列
        result.append(rsrs_score)
        signal.append(position)
        if rsrs_score < sail_score:
            position = 0
        # 10日线拐头
        elif rsrs_score > buy_score:
            if use_ma == 0 or (use_ma == 1 and current_ma > last_ma):
                position = 1
        last_rsrs_score = rsrs_score
        last_ma = current_ma

    return result, slope_series[-days:], signal, data.close[-days:].values


def get_max_args(stock_code, days, slop_days=18, M=400, MA=10, buy_score=0.7, sail_score=-1.4, use_ma=0):
    (rsrs_score, slopes, signal, close) = get_rsrs_score(stock_code, days, slop_days, M,
                                                         MA, buy_score, sail_score, use_ma)
    df = pd.DataFrame(rsrs_score, columns=['rsrs_score'])
    df['slopes'] = slopes
    df['signal'] = signal
    df['close'] = close

    df["策略"] = (1 + df.close.pct_change(1).fillna(0) * signal).cumprod()
    df["基准"] = df['close'] / df['close'][0]

    print("slop_days=%s, M=%s, MA=%s,buy_score = %s, sail_score = %s use_ma:%s 基准收益率: %s 收益率: %s" % (slop_days, M,
                                                                                           MA,
                                                                                           buy_score,
                                                                                           sail_score,
                                                                                            use_ma,
                                                                                           df["基准"].values[-1],
                                                                                           df["策略"].values[
                                                                                               -1]))

    if df["策略"].values[-1] > df["基准"].values[-1]:
        fig, axes = plt.subplots(2, 1, sharex=True, figsize=(18, 12))
        df[['策略', '基准', 'signal']].plot(ax=axes[0], grid=True, title='收益', figsize=(20, 10))
        df.rsrs_score.plot(ax=axes[1], title='rsrs_score', grid=True)
        plt.savefig('slop_days%s_M%s_MA%s_buy_score%s_sail_score%s_usema%s.png' % (slop_days, M, MA, buy_score,
                                                                                   sail_score, use_ma))

    return df["策略"].values[-1]


M = 600
slop_days = 18
days = 600

data = quotation.get_bars('002230', M + slop_days + days,
                          fields=['close', 'high', 'low'],
                          end_dt=date)
# data['ma'] = data.close.rolling(20).mean()

#     for i in range(M):
#         HS300.loc[i, 'beta_norm'] = (HS300.loc[i, 'beta'] - HS300.loc[:i - 1, 'beta'].mean()) / HS300.loc[:i - 1,
#                                                                                                 'beta'].std()

# M+days
ols_data = [get_ols(data.low[i:i + slop_days], data.high[i:i + slop_days]) for i in range(len(data))]
slope_series = [ols_data[i][1] for i in range(M + days)]
r2 = [ols_data[i][2] for i in range(M + days)]

# 斜率直方图
plt.figure(figsize=(15,5))
plt.hist(slope_series, bins= 100, range= None, weights= None, cumulative= False,
         bottom= None, histtype= 'bar', align= 'mid', orientation= 'vertical', rwidth= None, log= False, color= 'r',
         label='直方图', stacked= False)
plt.show()



# slop_days=17, M=200, MA=0,buy_score = 0.9, sail_score = -1.3 use_ma:0 收益率: 2.2461242244347384
# slop_days=10, M=200, MA=10,buy_score = 1.0, sail_score = -1.2 基准收益率: 1.6168427594779367 收益率: 2.257659818289085
#slop_days=10, M=200, MA=10,buy_score = 0.9, sail_score = -1.2
# slop_days=10, M=250, MA=1,buy_score = 0.6, sail_score = -1.5 use_ma:0 基准收益率: 1.3719224724986905 收益率: 1.3719224724986916

# get_max_args('002230', 600, 10, 250, 1, 0.9, -1.5, 0)

# slop_days=17, M=200, MA=1,buy_score = 1.0, sail_score = -1.4 use_ma:0 基准收益率: 1.652887346165983 收益率: 2.3299197792940176
# slop_days=17, M=200, MA=1,buy_score = 1.0, sail_score = -1.3 use_ma:0 基准收益率: 1.652887346165983 收益率: 2.4466786338581996
# get_max_args('002230', 600, 10, 200, 1, 1.0, -1.3, 0)

# slop_days=17, M=200, MA=1,buy_score = 0.9, sail_score = -1.3 use_ma:0 基准收益率: 1.652887346165983 收益率: 2.2461242244347384


# get_max_args('002230', 600, 10, 200, 10, 1.0, -1.2, 1)
# # get_max_args('002230', 600, 10, 200, 10, 0.9, -1.2, 1)
# get_max_args('002230', 240, 17, 200, 1, 0.9, -1.0, 0)
# get_max_args('002230', 240, 17, 200, 1, 1.0, -1.3, 0)
# get_max_args('002230', 240, 17, 200, 1, 0.9, -1.4, 0)
# get_max_args('002230', 240, 17, 200, 5, 1.0, -1.3, 1)
# get_max_args('002230', 240, 17, 200, 10, 1.0, -1.3, 1)
# get_max_args('002230', 240, 17, 200, 12, 1.0, -1.3, 1)
# get_max_args('002230', 240, 17, 200, 14, 1.0, -1.3, 1)
# get_max_args('002230', 240, 17, 200, 20, 1.0, -1.3, 1)
# get_max_args('002230', 240, 17, 200, 17, 1.0, -1.3, 1)

#
# 4*4*3*7*8 = 2688
# for slop_days in [10, 15, 17]:
#     for M in [200, 250, 300, 400]:
#         for buy_score in [0.6, 0.7, 0.9, 1.0]:
#             for sail_score in [-1.0, -1.2, -1.2, -1.3, -1.4, -1.5]:
#                 for use_ma in [0, 1]:
#                     if use_ma:
#                         for MA in [10, 15, 20]:
#                             score = get_max_args('002230', 600, slop_days, M, MA, buy_score, sail_score, use_ma)
#                             if score > max_score:
#                                 max_score = score
#                                 print("当前最大值slop_days=%s, M=%s, MA=%s,buy_score = %s, sail_score = %s,use_ma:%s 收益率: "
#                                       "%s" % (
#                                     slop_days, M, MA, buy_score, sail_score, use_ma, max_score))
#                     else:
#                         score = get_max_args('002230', 600, slop_days, M, 1, buy_score, sail_score, use_ma)
#                         if score > max_score:
#                             max_score = score
#                             print("当前最大值slop_days=%s, M=%s, MA=%s,buy_score = %s, sail_score = %s use_ma:0 收益率: %s" % (
#                                 slop_days, M, 0, buy_score, sail_score, max_score))
#
# print(max_score)
