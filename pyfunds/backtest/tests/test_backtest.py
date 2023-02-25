import sys

sys.path.insert(0, "../")
import xalpha as xa
import pandas as pd


def test_ScheduledSellonXIRR():
    bt = xa.backtest.ScheduledSellonXIRR(
        start="2018-01-01",
        value=1000,
        code="F110026",
        date_range=pd.date_range("2018-01-01", "2020-07-01", freq="W-FRI"),
    )
    bt.backtest()
    sys = bt.get_current_mul()
    assert sys.totcftable.iloc[-1]["date"].strftime("%Y-%m-%d") == "2020-01-17"


def test_tendency():
    t28 = xa.backtest.Tendency28(start="2018-01-01", verbose=True, initial_money=600000)
    t28.backtest()
    sys = t28.get_current_mul().summary()
    assert sys[sys["基金名称"] == "总计"].iloc[0]["历史最大占用"] == 600000


def test_balance():
    fundlist = ["002146", "001316", "001182"]
    portfolio_dict = {"F" + f: 1 / len(fundlist) for f in fundlist}
    check_dates = pd.date_range("2019-01-01", "2020-08-01", freq="Q")
    bt = xa.backtest.Balance(
        start=pd.Timestamp("2019-01-04"),
        totmoney=10000,
        check_dates=check_dates,
        portfolio_dict=portfolio_dict,
        verbose=True,
    )

    bt.backtest()
    sys = bt.get_current_mul()
    sys.summary("2020-08-15")
    assert round(sys.xirrrate("2020-08-14"), 2) == 0.18
