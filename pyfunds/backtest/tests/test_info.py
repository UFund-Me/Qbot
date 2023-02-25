import sys

sys.path.insert(0, "../")
import xalpha as xa
from xalpha.exceptions import FundTypeError
import pandas as pd
import pytest

ioconf = {"save": True, "fetch": True, "path": "pytest", "form": "csv"}
ca = xa.cashinfo(interest=0.0002, start="2015-01-01")
zzhb = xa.indexinfo("0000827", **ioconf)
hs300 = xa.fundinfo("000311")
zogqb = xa.mfundinfo("001211", **ioconf)


# @pytest.mark.skip(reason="fund report utility to be repaired due to web refactort")
def test_fundreport():
    # somehow fragile, to be checked
    r = xa.FundReport("000827")
    assert r.get_report()[0][:2] == "广发"
    assert r.analyse_report(1)["bank"][:2] == "兴业"
    assert r.show_report_list(type_=0)[0]["FUNDCODE"] == "000827"
    assert r.get_report(id_="AN202003171376532533")[0][:2] == "广发"


def test_cash():
    assert (
        round(ca.price[ca.price["date"] == "2018-01-02"].iloc[0].netvalue, 4) == 1.2453
    )
    assert ca.code == "mf"
    date, value, share = ca.shuhui(
        300, "2018-01-01", [[pd.Timestamp("2017-01-03"), 200]]
    )
    assert date == pd.Timestamp("2018-01-02")
    assert value == 249.06
    assert share == -200
    ca.bcmkset(ca)
    assert ca.alpha() == 0
    assert round(ca.total_annualized_returns("2018-01-01"), 4) == 0.0757


def test_index():
    assert (
        round(zzhb.price[zzhb.price["date"] == "2012-02-01"].iloc[0].totvalue, 3)
        == 961.406
    )
    assert (
        round(zzhb.price[zzhb.price["date"] == "2015-02-02"].iloc[0].netvalue, 2)
        == 1.62
    )
    assert zzhb.name == "中证环保"
    assert zzhb.shengou(100, "2018-01-02")[2] == 55.24
    assert zzhb.shuhui(100, "2016-01-01", [[pd.Timestamp("2017-01-03"), 200]])[2] == 0
    zzhb.info()
    zzhb.ma(window=10)
    zzhb.md()
    zzhb.ema(col="totvalue")
    zzhb.macd()
    zzhb.mtm()
    zzhb.roc()
    zzhb.boll()
    zzhb.bias()
    zzhb.rsi()
    zzhb.kdj()
    zzhb.wnr()
    zzhb.dma(col="totvalue")
    zzhb.bbi()
    zzhb.trix(col="totvalue")
    zzhb.psy()
    row = zzhb.price[zzhb.price["date"] == "2018-08-01"].iloc[0]
    assert round(row["MD5"], 3) == 0.012
    assert round(row["MA10"], 3) == 1.361
    assert round(row["MACD_OSC_12_26"], 4) == 0.0076
    assert round(row["EMA5"], 1) == 1318.8
    assert round(row["MTM10"], 4) == 0.0078
    assert round(row["ROC10"], 4) == 0.0058
    assert round(row["BOLL_UPPER"], 3) == 1.398
    assert round(row["BIAS10"], 3) == -0.012
    assert round(row["RSI14"], 3) == 0.411
    assert round(row["KDJ_J"], 4) == 0.0456
    assert round(row["WNR14"], 2) == 0.27
    assert round(row["AMA"], 2) == -87.71
    assert round(row["BBI"], 3) == 1.356
    assert round(row["TRIX10"], 4) == 0.0005
    assert round(row["PSYMA12"], 2) == 0.47
    zzhb.v_techindex(col=["TRIX10"])


def test_fund():
    assert hs300.round_label == 1
    assert hs300.name == "景顺长城沪深300指数增强A"  ## "景顺长城沪深300增强", 蜜汁改名。。。
    assert hs300.fenhongdate[1] == pd.Timestamp("2017-08-15")
    assert hs300.get_holdings(2019, 4).iloc[0]["name"] == "中国平安"
    assert (
        float(hs300.special[hs300.special["date"] == "2017-08-04"]["comment"]) == 0.19
    )
    hs300.rate = 0.12
    hs300.segment = [[0, 7], [7, 365], [365, 730], [730]]
    with pytest.raises(Exception) as excinfo:
        hs300.shuhui(
            100,
            "2014-01-04",
            [[pd.Timestamp("2014-01-03"), 200], [pd.Timestamp("2017-01-03"), 200]],
        )
    assert str(excinfo.value) == "One cannot move share before the lastest operation"
    assert (
        hs300.shuhui(
            320,
            "2018-01-01",
            [[pd.Timestamp("2011-01-03"), 200], [pd.Timestamp("2017-12-29"), 200]],
        )[1]
        == 685.72
    )
    assert hs300.shengou(200, "2018-07-20")[2] == 105.24
    with pytest.raises(FundTypeError) as excinfo:
        xa.mfundinfo("000311")
    assert str(excinfo.value) == "This code seems to be a fund, use fundinfo instead"
    hs300.info()
    dax = xa.fundinfo("510030")  # test empty shuhuifei and shengoufei case
    assert dax.feeinfo == ["小于7天", "1.50%", "大于等于7天", "0.00%"]


def test_mfundinfo():
    zogqb.bcmkset(xa.cashinfo())
    assert round(zogqb.total_annualized_returns("2018-08-01"), 3) == 0.036
    with pytest.raises(FundTypeError) as excinfo:
        xa.fundinfo("001211")
    assert str(excinfo.value) == "This code seems to be a mfund, use mfundinfo instead"


def test_fund_holdings():
    f = xa.fundinfo("F519732")
    df = f.get_stock_holdings(2020, 2)
    assert df.iloc[0]["code"] == "300413"
    d = f.get_industry_holdings(2020, 2)
    assert d["交通运输"] == 5.48
    d = f.get_portfolio_holdings("20180101")
    assert d["stock_ratio"] == 68.62
    df = f.get_bond_holdings(2020, 2)
    assert df.iloc[0]["code"] == "190307"
    assert f.which_industry() == "宽基基金"


def test_evaluate():
    comp = xa.evaluate(ca, zzhb, hs300)
    comp.v_netvalue(end="2018-08-01")
    comp.v_correlation()
    comp2 = xa.evaluate(ca, zzhb, start="2018-01-01")
    assert round(comp2.correlation_table("2018-08-01").iloc[0, 1], 3) == 0.064


def delete_csvlines(path, lines=5):
    df = pd.read_csv(path)
    for _ in range(lines):  ## delete one weeks data
        df = df.drop(df.index[len(df) - 1])
    df.to_csv(path, index=False)


def test_csvio():
    hs300 = xa.fundinfo("000311", **ioconf)
    len1 = len(hs300.price)
    hs300 = xa.fundinfo("000311", **ioconf)
    len2 = len(hs300.price)
    delete_csvlines(path=ioconf["path"] + "000311.csv")
    hs300 = xa.fundinfo("000311", **ioconf)
    len3 = len(hs300.price)
    assert (len1 == len2) or (len1 - len2 == -1)  # temp fixup
    # there may be time lag for update of .js API, i.e. 天天基金的该 API 不一定能保证更新昨天的净值，即使不是 QDII
    assert (len1 == len3) or (len1 - len3 == -1)
    delete_csvlines(path=ioconf["path"] + "001211.csv")
    zogqb2 = xa.mfundinfo("001211", **ioconf)
    assert round(zogqb.price.iloc[-1].netvalue, 5) in [
        round(zogqb2.price.iloc[-1].netvalue, 5),
        round(zogqb2.price.iloc[-2].netvalue, 5),
    ]
    delete_csvlines(path=ioconf["path"] + "0000827.csv")
    zzhb2 = xa.indexinfo("0000827", **ioconf)
    assert (len(zzhb2.price) == len(zzhb.price)) or (
        (len(zzhb2.price) - len(zzhb.price)) == 1
    )


def test_fund_update():
    zghl = xa.fundinfo(
        "501029", **ioconf
    )  # 164906 maybe possible remainning issue for qdii?
    len1 = len(zghl.price)
    delete_csvlines(path=ioconf["path"] + "501029.csv", lines=83)
    zghl = xa.fundinfo("501029", **ioconf)
    len2 = len(zghl.price)
    assert (len1 == len2) or (len1 - len2 == -1)  # similar fix up
    jxzl = xa.mfundinfo("002758", **ioconf)
    netvalue = jxzl.price.iloc[-1]["netvalue"]
    len3 = len(jxzl.price)
    delete_csvlines(path=ioconf["path"] + "002758.csv", lines=9)
    jxzl = xa.mfundinfo("002758", **ioconf)
    netvaluel = [
        round(jxzl.price.iloc[-1]["netvalue"], 4),
        round(jxzl.price.iloc[-2]["netvalue"], 4),
    ]
    len4 = len(jxzl.price)
    assert (len3 == len4) or (len3 - len4 == -1)
    assert round(netvalue, 4) in netvaluel  ##天天基金的总量 API 更新越来越慢了。。。


def test_vinfo():
    hs300 = xa.vinfo("SH000300", start="20190901")
    hs300.info()
    st = pd.DataFrame({"date": ["20200101", "20200203"], "SH000300": [200, -100]})
    st["date"] = pd.to_datetime(st["date"])
    t = xa.trade(hs300, st)
    t.dailyreport()
    assert len(t.cftable) == 2
    # yy = xa.vinfo("ZZ931152") # fail on oversea server
    hs300.pct_chg()
