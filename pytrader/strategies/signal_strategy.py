import sys

sys.path.append(r"/Users/charmve/Qbot/pytrader/data")

# print(sys.path)

import os

import matplotlib.pyplot as plt
import pandas as pd
import talib as ta
from base import Strategy
from data_utils import load_data, load_from_file
from IPython.display import display


# Step 1: load dataset and generate features
def prepare_data(
    codes=["000300.SH", "399006.SZ"], start_time="20100101", end_time="20211231"
):
    df = load_data(codes, start_time, end_time)

    df["rsi"] = ta.RSI(df.close, timeperiod=14)
    df["to_buy"] = ""
    df.loc[df["rsi"] <= 30, "to_buy"] = True
    df["to_buy"] = df["to_buy"].astype("bool")

    df["to_sell"] = ""
    df.loc[df["rsi"] >= 70, "to_sell"] = True
    df["to_sell"] = df["to_sell"].astype("bool")
    print("> step 1 is Successfully.")
    return df


# Step 2: prepare strategy
class SelectBySignal(object):
    def __init__(self, signal_buy="to_buy", signal_sell="to_sell"):
        super(SelectBySignal, self).__init__()
        self.signal_buy = signal_buy
        self.signal_sell = signal_sell

    def __call__(self, context):
        bar = context["bar"].copy()

        acc = context["acc"]
        holding = acc.get_holding_instruments()

        to_buy = list(bar[bar[self.signal_buy]].index)
        to_sell = list(bar[bar[self.signal_sell]].index)

        instruments = to_buy + holding
        to_selected = []
        for s in instruments:
            if s not in to_sell:
                to_selected.append(s)
        context["selected"] = to_selected

        n = len(to_selected)
        if n > 0:
            context["weights"] = {code: 1 / n for code in to_selected}
        else:
            context["weights"] = {}
        print("> step 2 is Successfully.")
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
        se.name = "strategy"
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
        codes=["000300.SH", "399006.SZ"], start_time=date_start, end_time=date_end
    )

    algo = SelectBySignal(signal_buy="to_buy", signal_sell="to_sell")
    s = Strategy(algo=algo)

    b = Backtest(df=df)
    df = b.run(s)

    path = os.path.dirname(__file__)
    # print(path)
    df.to_csv(os.path.dirname(path) + "/results/first_test.csv")

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
