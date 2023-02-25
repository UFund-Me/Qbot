import sys
import time
import pytest

sys.path.insert(0, "../")
import xalpha as xa

xa.set_backend(backend="memory", prefix="pytest-")


@pytest.fixture
def proxy():
    xa.provider.set_proxy("socks5://127.0.0.1:1080")
    yield
    xa.provider.set_proxy()


def test_get_xueqiu():
    df = xa.get_daily(start="20200302", end="2020-03-07", code="HK01810")
    assert round(df.iloc[-1]["close"], 2) == 12.98
    df = xa.get_daily(start="2020/03/02", end="20200307", code="PDD")
    assert round(df.iloc[0]["close"], 2) == 37.51
    df = xa.get_daily(start="20200301", end="20200307", code="SZ112517")
    # note how this test would fail when the bond is matured
    assert round(df.iloc[0]["close"], 2) == 98
    df = xa.get_daily(start="20200222", end="20200301", code="SH501018")
    assert round(df.iloc[-1]["close"], 3) == 0.965
    df = xa.get_daily("SH600000.A", end="20200428")
    assert round(df.iloc[-1]["close"], 2) == 131.34


def test_get_rmb():
    df = xa.get_daily(start="20180101", end="2020-03-07", code="USD/CNY")
    assert len(df) == 528
    df = xa.get_daily(code="EUR/CNY", end="20200306")
    assert round(df.iloc[-1]["close"], 4) == 7.7747
    df = xa.get_daily("CNY/EUR", end="20200306", prev=5)
    assert round(df.iloc[-1]["close"], 3) == round(1 / 7.7747, 3)


def test_get_fund():
    df = xa.get_daily(code="F100032", start="2020-02-01")
    assert round(df[df["date"] == "2020-03-06"].iloc[0]["close"], 3) == 1.036
    df = xa.get_daily(code="M002758", start="20200201")
    assert round(df.iloc[1]["close"], 3) == 1.134


def test_get_fund_pt():
    df = xa.get_daily("pt-F100032", start="20191201")
    assert round(df[df["date"] < "2020-01-01"].iloc[-1]["bond_ratio"], 2) == 0.08


@pytest.mark.skip(reason="cninvesting explorer check")
def test_get_investing():
    df1 = xa.get_daily(code="indices/germany-30")
    df2 = xa.get_daily(code="172")
    assert (
        df1.iloc[-2]["close"] == df2.iloc[-2]["close"]
    )  ## never try -1, today's data is unpredictable
    df = xa.get_daily(code="/currencies/usd-cny", end="20200307", prev=20)
    assert round(df.iloc[-1]["close"], 4) == 6.9321
    df.v_kline(ucolor="#ffffff", ucolorborder="#ef232a")


# @pytest.mark.local
@pytest.mark.skip(reason="cninvesting explorer check")
def test_get_investng_app():
    df = xa.get_daily(
        code="INA-currencies/usd-cny", end="20200307", prev=30
    )  # 似乎外网链接有问题？
    assert round(df.iloc[-1]["close"], 4) == 6.9321
    assert xa.get_rt("INA-indices/germany-30")["name"] == "德国DAX30指数 (GDAXI)"


def test_get_xueqiu_rt():
    assert xa.get_rt("PDD")["currency"] == "USD"
    assert xa.get_rt("03333")["name"] == xa.get_rt("HK03333")["name"]
    assert isinstance(xa.get_rt("SH501018")["percent"], float)


def test_get_sina_rt():
    assert xa.get_rt("PDD", _from="sina")["currency"] == "USD"
    xa.get_rt("HK00700", double_check=True)  # 港股 sina 实时数据延迟, 代码前需加 rt_ 方可获取实时
    xa.get_rt("SH600000", double_check=True)


@pytest.mark.skip(reason="cninvesting explorer check")
def test_get_investing_rt():
    assert xa.get_rt("currencies/usd-cny")["currency"] == None
    assert xa.get_rt("/indices/germany-30")["name"] == "德国DAX30指数 (GDAXI)"
    ext = xa.get_rt("equities/pinduoduo")["current_ext"]
    assert isinstance(ext, float) or (ext is None)


@pytest.mark.local
def test_get_ft_rt():
    assert xa.get_rt("FT-INX:IOM")["currency"] == "USD"
    assert xa.get_rt("FTC-WTI+Crude+Oil")["name"] == "NYMEX Crude Oil Front Month"


# @pytest.mark.skip(
#     reason="sp fetcher is currently to be fixed for new version of websites"
# )
def test_get_sp_daily():
    df = xa.get_daily("SP5475707.2", start="20200202", end="20200303")
    assert round(df.iloc[-1]["close"], 3) == 1349.31
    df = xa.get_daily("SP5475707.2", prev=100, end="20200303")
    assert round(df.iloc[-1]["close"], 3) == 1349.31


# @pytest.mark.local
@pytest.mark.skip(reason="blommberg network connection issue")
def test_get_bb_daily(proxy):
    df = xa.get_daily("BB-FGERBIU:ID", prev=10)


def test_get_yahoo_daily():
    df = xa.get_daily("YH-CSGOLD.SW", end="20200323")
    assert round(df.iloc[-1]["close"], 1) == 149.4


def test_get_ft_daily():
    df = xa.get_daily("FT-22065529", start="20190101", end="20200323")
    assert len(df) == 306
    df = xa.get_daily("FT-AUCHAH:SWX:CHF", prev=10, end="20200327")
    assert round(df.iloc[-1]["close"], 2) == 66.37
    xa.get_daily("FTE-DVN:NYQ", prev=10)


def test_cache():
    get_daily_cache = xa.universal.cached("20190101")(xa.universal._get_daily)
    l1 = get_daily_cache("EUR/CNY", start="20200101")
    l2 = get_daily_cache("EUR/CNY", start="20190101")
    l3 = get_daily_cache("EUR/CNY", start="20180101")
    assert l2.iloc[0]["date"] == l3.iloc[0]["date"]


def test_cache_io():
    get_daily_csv = xa.universal.cachedio(path="./", prefix="pytestl-", backend="csv")(
        xa.universal._get_daily
    )
    df = get_daily_csv("SH501018", start="2020-01-24", end="2020/02/02")
    assert len(df) == 0
    df = get_daily_csv("SH501018", start="2020-01-23", end="20200203")
    assert len(df) == 2
    df = get_daily_csv("SH501018", start="2020-01-24", end="20200205")
    assert len(df) == 3
    df = get_daily_csv("SH501018", start="2020-01-23")
    df = get_daily_csv("SH501018")
    df = get_daily_csv("SH501018", end="2020-02-01")
    assert df.iloc[0]["date"].strftime("%Y%m%d") == "20190201"
    xa.universal.check_cache("SH501018", prev=32, omit_lines=1)


def test_ioconf_keyfunc():
    get_daily_key = xa.universal.cachedio(
        path="./", backend="csv", key_func=lambda s: s[::-1]
    )(xa.universal._get_daily)
    df1 = get_daily_key("BA", start="2020-03-03")
    get_daily_key = xa.universal.cachedio(path="./", backend="csv")(
        xa.universal._get_daily
    )
    df2 = get_daily_key("AB", fetchonly=True)
    assert df2.iloc[-1]["close"] == df1.iloc[-1]["close"]


def test_cache_mm():
    df = xa.get_daily("SH501018", prev=100)
    l1 = len(df)
    # xa.set_backend(backend="memory", prefix="pytestm-")
    xa.get_daily("SH501018", prev=50)
    df = xa.get_daily("SH501018", prev=100)
    l2 = len(df)
    assert l1 == l2
    xa.universal.check_cache("SH501018", start="2018/09/01", omit_lines=1)


def test_get_bar_xq():
    xa.get_bar("HK00700", interval=60)
    xa.get_bar("SH600000", interval=3600)
    # xa.get_bar("commodities/brent-oil", interval=300, prev=20)


def test_set_handler():
    def alt_get_bar(code, **kws):
        if code == 1:
            return 1
        else:
            return

    xa.set_handler(method="bar", f=alt_get_bar)
    assert xa.get_bar(1) == 1
    assert len(xa.get_bar("PDD")) == 24
    xa.set_handler(method="bar")


def test_cache_time():
    class F:
        def __init__(self):
            self.r = 0

        def __call__(self):
            self.r += 1
            return self.r

        __name__ = "F"

    f = xa.universal.lru_cache_time(ttl=5)(F())

    assert f() == 1
    assert f() == 1
    time.sleep(5)
    assert f() == 2


def test_get_ttjj():
    assert xa.get_rt("F501018")["name"] == "南方原油A"
    assert xa.get_rt("F511600")["type"] == "货币型"
    assert xa.get_rt("F003816")["market"] == "CN"


@pytest.mark.local
def test_get_zzindex():
    assert len(xa.get_daily("ZZH30533")) > 100


def test_get_gzindex():
    df = xa.get_daily("GZB30018", start="20200202", end="20200204")
    assert round(df.iloc[-1]["close"], 1) == 107.4


def test_get_hzindex():
    assert len(xa.get_daily("HZ999002")) > 100


@pytest.mark.skip(reason="esunny website down")
def test_get_es():
    df = xa.get_daily("ESCI000302", start="20190419", end="2019/04/22")
    assert round(df.iloc[-1]["settlement"], 2) == 1074.80


@pytest.mark.local
def test_get_ycharts():
    # ycharts 可能有时也需要代理了。。。。
    d = xa.get_daily(code="yc-companies/DBP", start="20200401", end="20200402")
    assert d.iloc[0]["close"] == 41.04

    d = xa.get_daily(
        code="yc-companies/DBP/net_asset_value", start="20200401", end="20200402"
    )
    assert d.iloc[0]["close"] == 40.7144

    d = xa.get_daily(code="yc-indices/^SPGSCICO", start="20200401", end="20200402")
    assert d.iloc[0]["close"] == 111.312

    d = xa.get_daily(
        code="yc-indices/^SPGSCICO/total_return_forward_adjusted_price",
        start="20200401",
        end="20200402",
    )
    assert d.iloc[0]["close"] == 169.821

    assert xa.get_rt("yc-companies/DBO")["currency"] == "USD"


def test_get_bond_rates():
    df = xa.get_daily("B-AA+.3", end="2020-05-17")
    assert df.iloc[-1]["close"] == 2.7743


def test_get_ttjj_rt_oversea():
    r = xa.get_rt("F968012")
    assert r["name"] == "中银香港高息债"


def test_ttjj_oversea_daily():
    df = xa.get_daily("F968054", start="2019-05-01", end="20190606")
    assert df.iloc[-1]["close"] == 10.18


@pytest.mark.skip(reason="futu API refactor")
def test_get_futu():
    df = xa.get_daily("fu-03690.HK", start="2021-01-01")
    assert df.iloc[0]["open"] == 293.4
    df = xa.get_daily("fu-BNO.US", start="2021-01-01")
