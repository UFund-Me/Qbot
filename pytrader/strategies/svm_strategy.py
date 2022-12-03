import os

import matplotlib.pyplot as plt
import pandas as pd
import talib as ta
from base import Strategy
from data.data_utils import load_data, load_from_file
from IPython.display import display
from model.svm import SVMModel


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
    return df


# Step 2: train model and prepare strategy
class MLStrategy(object):
    def __init__(self, df, topk=8):
        super(MLStrategy, self).__init__()
        svm = SVMModel()
        svm.fit(df, train_valid_date="20180101")
        results = svm.predict()
        df["pred_score"] = results
        self.K = topk

    def __call__(self, context):
        bar = context["bar"].copy()
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
    filename = os.path.dirname(path) + "/results/second_test.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df["date"] = df["date"].apply(lambda x: str(x))
        df.index = df["date"]
        se = (df["rate"] + 1).cumprod()
        se.name = "svm strategy"
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

    algo = MLStrategy(df, topk=3)
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
