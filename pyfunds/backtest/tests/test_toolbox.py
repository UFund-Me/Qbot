import sys
import pytest

sys.path.insert(0, "../")
import xalpha as xa

xa.set_backend(backend="memory", prefix="pytest-")


def test_compare():
    c = xa.Compare(("FT-JBGOUA:SWX:USD", "USD"), "SH501018", start="20200101")
    c.corr()
    c.v()


def test_stock_peb():
    h = xa.StockPEBHistory("HK00700")
    h.summary()


def test_overpriced():
    xa.OverPriced("SZ161815", prev=360).v([-1.5, 3.5])


@pytest.mark.local
def test_set_display():
    xa.set_display("notebook")
    df = xa.get_daily("PDD", prev=30)
    df._repr_javascript_()
    xa.set_display()
    assert getattr(df, "_repre_javascript_", None) is None


def test_get_currency():
    assert (
        xa.toolbox.get_currency_code("indices/india-50-futures") == "currencies/inr-cny"
    )
    assert xa.toolbox._get_currency_code("JPY") == "100JPY/CNY"


@pytest.mark.skip(reason="cninvesting server check")
def test_qdii_predict():
    hb = xa.QDIIPredict(
        "SZ162411",
        t1dict={".SPSIOP": 91},
        t0dict={
            "commodities/brent-oil": 40 * 0.9,
            "commodities/crude-oil": 60 * 0.9,
        },
        positions=True,
    )
    hb.get_t1()
    hb.get_t0(percent=True)
    hb.benchmark_test("20200202", "20200302")
    hb.analyse()


# @pytest.mark.local
@pytest.mark.skip(reason="cninvesting server check")
def test_qdii_predict_local():
    xc = xa.QDIIPredict("SZ165513", positions=True)
    xc.get_t0_rate()


def test_rt_predict():
    p = xa.RTPredict("SH512500", t0dict="SH000905")
    p.get_t0_rate()


def test_cbcaculator():
    c = xa.CBCalculator("SH113577")
    d = c.analyse()
    assert d["name"] == "春秋转债"
    # obtain correct redeem_price from superscipt
    c = xa.CBCalculator("SH113604")
    d = c.analyse()
    assert d["name"] == "多伦转债"
