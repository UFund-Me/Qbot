import os
import sys

sys.path.append(os.getcwd())

# from data import data_utils

import matplotlib.pyplot as plt
import pandas as pd
import talib as ta
from base import Strategy
# from data.data_utils import load_data, load_from_file
from IPython.display import display
# from model.lgb import LGBModel

import os

import pandas as pd


def load_data(codes, start_time="20100101", end_time="20211231"):
    dfs = []
    for code in codes:
        df = load_from_file(code)
        # df.dropna(inplace=True)
        dfs.append(df)
    df_all = pd.concat(dfs, axis=0)
    df_all.sort_index(inplace=True)
    df_all = df_all.loc[start_time:end_time]
    return df_all


def load_from_file(code):
    path = os.path.dirname(__file__)
    filename = "{}/{}.csv".format(os.path.dirname(path) + "/data/indexes", code)
    # print("stack data:" + filename)
    if os.path.exists(filename):
        df = pd.read_csv(filename, index_col=[0])
        # print(df.head())
        df.rename(
            columns={"trade_date": "date", "ts_code": "code", "vol": "volume"},
            inplace=True,
        )
        df["date"] = df["date"].apply(lambda x: str(x))
        ## code,date,close,open,high,low,volume,amount
        # df = df[["code", "open", "high", "low", "close", "date", "volume"]]
        df = df[['open', 'high', 'low', 'close', 'date', 'volume']]
        df.index = df["date"]
        df.sort_index(ascending=True, inplace=True)
        df["rate"] = df["close"].pct_change()
    else:
        print("load_from_file error")
        return None
    return df


import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import r2_score, accuracy_score

class LGBModel:
    def __init__(self, regression = True):
        self.regression = regression
    def fit(self, dataset):
        X_train, X_valid, y_train, y_valid = dataset.split()

        dtrain = lgb.Dataset(X_train, label=y_train)
        dvalid = lgb.Dataset(X_valid, label=y_valid)

        #params = {"objective": 'mse', "verbosity": -1}
        # 参数
        params_regression = {
            'learning_rate': 0.1,
            'metrics':{'auc','mse'},
            'lambda_l1': 0.1,
            'lambda_l2': 0.2,
            'max_depth': 4,
            'objective': 'mse'#'mse',  # 目标函数
        }

        params = {'num_leaves': 90,
                  'min_data_in_leaf': 30,
                  'objective': 'multiclass',
                  'num_class': 10,
                  'max_depth': -1,
                  'learning_rate': 0.03,
                  "min_sum_hessian_in_leaf": 6,
                  "boosting": "gbdt",
                  "feature_fraction": 0.9,
                  "bagging_freq": 1,
                  "bagging_fraction": 0.8,
                  "bagging_seed": 11,
                  "lambda_l1": 0.1,
                  "verbosity": -1,
                  "nthread": 15,
                  'metric': {'multi_logloss'},
                  "random_state": 2022,
                  #'device': 'gpu'
                  }

        if self.regression:
            params = params_regression
        self.model = lgb.train(
            params,
            dtrain,
            num_boost_round=1000,
            valid_sets=[dtrain, dvalid],
            valid_names=["train", "valid"],
            early_stopping_rounds=50,
            verbose_eval=True,
            # evals_result=evals_result,
            #**kwargs
        )
        y_pred = self.model.predict(X_valid)
        if not self.regression:
            y_pred = np.argmax(y_pred, axis=1)
            print('accuracy:',accuracy_score(y_pred, y_valid))

            y_pred_train = np.argmax(self.model.predict(X_train), axis=1)
            print('accuracy_train:',accuracy_score(y_pred_train, y_train))
        else:
            print('R2系数：', r2_score(y_valid, y_pred))
            print('训练集——R2系数：', r2_score(y_train, self.model.predict(X_train)))

    def predict(self, dataset):
        if self.model is None:
            raise ValueError("model is not fitted yet!")
        x_test,_ = dataset.get_data(date_range=['20160101', '20211231'])
        pred = self.model.predict(x_test)
        print(pred)
        if not self.regression:
            return pd.Series(np.argmax(pred, axis=1), index=x_test.index)
        else:
            return pd.Series(pred, index=x_test.index)


# if __name__ == '__main__':
#     from bak.data.dataset import Dataset
#     from engine.data.datahandler import DataHandler

#     fields = ['Return($close,5)', 'Return($close,20)', 'Ref($close,126)/$close -1','$close','$open','$high','$low','$volume','$amount']
#     names = ['return_5', 'return_20', 'return_126','close','open','high','low','volume','amount']

#     #fields += ['Ref($close,-5)/$close -1']
#     #names += ['return_-5']

#     #ds = Dataset(codes=, fields=fields, feature_names=names,
#     #             label_expr='QCut(Ref($close,-20)/$close -1,10)')
#     #print(ds.df)
#     codes = ['512690.SH', '512170.SH', '512660.SH','159928.SZ','512010.SH']
#     codes = ['159915.SZ','510300.SH','512690.SH', '512170.SH', '512660.SH','159928.SZ','512010.SH']
#     codes = ['159928.SZ','510050.SH','512010.SH','513100.SH','518880.SH','511220.SH','511010.SH','161716.SZ']
#     codes = [
#         '000300.SH',
#         '000905.SH',
#         '399006.SZ', #创业板
#         '000852.SH', #中证1000
#         '399324.SZ', #深证红利
#         #'000922.SH', #中证红利
#         '399997.SZ', #中证白酒
#         '399396.SZ', #食品饮料

#         '000013.SH',#上证企债
#         '000016.SH' #上证50
#     ]
#     ds = Dataset(codes=codes, handler=DataHandler())
#     print(ds.df)

#     m = LGBModel()
#     m.fit(ds)
#     pred = m.predict(ds)
#     print(pred)


# Step 1: load dataset and generate features
def prepare_data(
    codes=["000300.SH", "399006.SZ"], start_time="20100101", end_time="20211231"
):
    df = load_data(codes, start_time, end_time)

    df["rsi"] = ta.RSI(df.close, timeperiod=14)

    types = ["SMA", "EMA", "WMA", "DEMA", "TEMA", "TRIMA", "KAMA", "MAMA", "T3"]
    for i in range(len(types)):
        df[types[i] + "5"] = ta.MA(df.close, timeperiod=5, matype=i)
        df[types[i] + "30"] = ta.MA(df.close, timeperiod=30, matype=i)
        df[types[i] + "120"] = ta.MA(df.close, timeperiod=120, matype=i)

    df["macd"], df["macdsignal"], df["macdhist"] = ta.MACD(
        df.close, fastperiod=12, slowperiod=26, signalperiod=9
    )

    df["obv"] = ta.OBV(df["close"], df["volume"])
    df["dcperiod"] = ta.HT_DCPERIOD(df.close)
    df["dcphase"] = ta.HT_DCPHASE(df.close)
    df["inhpase"], df["quadrature"] = ta.HT_PHASOR(df.close)
    df["sine"], df["leadsine"] = sine, leadsine = ta.HT_SINE(df.close)
    df["trendmode"] = ta.HT_TRENDMODE(df.close)

    df["atr"] = ta.ATR(df.high, df.low, df.close, timeperiod=14)
    df["natr"] = ta.NATR(df.high, df.low, df.close, timeperiod=14)
    df["trange"] = ta.TRANGE(df.high, df.low, df.close)

    df["label"] = df["close"].shift(5) / df["close"] - 1
    print(df[["close", "label"]])
    return df


# Step 2: train model and prepare strategy
class MLStrategy(object):
    def __init__(self, df, topk=8):
        super(MLStrategy, self).__init__()
        lgb = LGBModel()
        lgb.fit(df, train_valid_date="20160101")
        results = lgb.predict()
        df["pred_score"] = results
        self.K = topk

    def __call__(self, context):
        bar = context["bar"].copy()
        # 先看selected
        if "selected" in context.keys():
            if len(context["selected"]) == 0:
                return False

            to_select = []
            for s in context["selected"]:
                if s in bar.index:
                    to_select.append(s)

            bar = bar.loc[to_select]

        bar.sort_values(by="pred_score", ascending=False, inplace=True)  # 倒序
        symbols = bar.index[: self.K]
        context["selected"] = symbols

        n = len(context["selected"])
        if n > 0:
            context["weights"] = {code: 1 / n for code in symbols}
        else:
            context["weights"] = {}
        return False


# Step 3: backtest
class Backtest:
    def __init__(self, df):
        self.df = df
        self.dates = self.df.index.unique()
        self.observers = []

    def onbar(self, index, date):
        df_bar = self.df.loc[date]
        if type(df_bar) is pd.Series:
            df_bar = df_bar.to_frame().T

        df_bar.index = df_bar["code"]
        self.strategy.onbar(index, date, df_bar)

    def run(self, s):
        self.strategy = s
        for index, date in enumerate(self.dates):
            self.onbar(index, date)
        return self.get_results()

    def get_results(self):
        s = self.strategy
        df = s.acc.get_results_df()
        return df


# Step 4: analysis
def analysis(start, end, benchmarks=[]):
    equities = []
    for benchmark in benchmarks:
        bench_df = load_from_file(benchmark)[start:end]
        se = (bench_df["rate"] + 1).cumprod()
        se.name = benchmark
        equities.append(se)

    path = os.path.dirname(__file__)
    filename = os.path.dirname(path) + "/results/first_test.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df["date"] = df["date"].apply(lambda x: str(x))
        df.index = df["date"]
        se = (df["rate"] + 1).cumprod()
        se.name = "lgb strategy"
        equities.append(se)

    df_equities = pd.concat(equities, axis=1)
    df_equities.dropna(inplace=True)
    print(df_equities)

    from performance import PerformanceUtils

    df_ratios, df_corr, df_years = PerformanceUtils().calc_equity(df_equity=df_equities)
    return df_equities, df_ratios, df_corr, df_years


if __name__ == "__main__":
    date_start = "20100101"
    date_end = "20211231"
    df = prepare_data(
        codes=["000300.SH", "000905.SH", "399006.SZ", "399324.SZ"],
        start_time=date_start,
        end_time=date_end,
    )

    algo = MLStrategy(df, topk=2)
    s = Strategy(algo=algo)

    b = Backtest(df=df)
    df = b.run(s)

    path = os.path.dirname(__file__)
    df.to_csv(os.path.dirname(path) + "/results/second_test.csv")

    df_equities, df_ratios, df_corr, df_years = analysis(
        start=date_start, end=date_end, benchmarks=["000300.SH"]
    )
    display(df_ratios)

    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    df_equities.plot(ax=ax1)
    if df_years is not None:
        print(df_years)
        df_years.T.plot(kind="bar", ax=ax2, use_index=True)
    plt.show()
