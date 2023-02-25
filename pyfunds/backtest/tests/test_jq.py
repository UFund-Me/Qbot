import sys

sys.path.insert(0, "../")
import xalpha as xa
import pandas as pd
import pytest
import shutil

xa.provider.set_jq_data(debug=True)


@pytest.fixture
def csv_cache():
    xa.set_backend(backend="csv", path="./")
    yield
    xa.set_backend(backend="memory", path="pytest-")


# 防止peb csv 数字位长反复变化
@pytest.fixture
def reset_table():
    l = ["./peb-SH000807.csv", "./sw-801180.csv", "./teb-SH000300.csv"]
    for f in l:
        shutil.copyfile(f, f + ".backup")
    yield

    for f in l:
        shutil.move(f + ".backup", f)


def test_jq_provider():
    assert xa.show_providers() == ["jq"]


def test_peb_history(csv_cache, reset_table):
    h = xa.PEBHistory("SH000807", end="20200302")
    h.summary()
    h.v()  # matplotlib is required for this
    assert round(h.df.iloc[0]["pe"], 2) == 19.67


def test_swpeb_history(csv_cache, reset_table):
    h = xa.toolbox.SWPEBHistory("801180", start="2012-01-04", end="20200202")
    h.summary()
    assert h.fluctuation() == 1
    assert round(h.df.iloc[-1]["dividend_ratio"], 2) == 2.89


def test_iw(csv_cache):
    df = xa.get_daily("iw-SZ399006", end="20200226")
    assert (
        df[(df["date"] == "2019-04-01") & (df["code"] == "300271.XSHE")].iloc[0].weight
        == 0.9835
    )
    df = xa.universal.get_index_weight_range(
        "SZ399006", start="2018-01-01", end="2020-02-01"
    )
    assert (
        df[(df["date"] == "2019-04-01") & (df["code"] == "300271.XSHE")].iloc[0].weight
        == 0.9835
    )


def test_peb_range(csv_cache, reset_table):
    df = xa.get_daily("peb-SH000807", prev=100, end="20200202")
    assert round(df[df["date"] == "2020-01-03"].iloc[0]["pe"], 2) == 30.09


def test_fund_share(csv_cache):
    df = xa.get_daily("fs-SZ161129", start="20200303", end="20200305")
    assert len(df) == 3
    df = xa.get_daily("fs-SZ161129", start="20200303", end="20200305")
    assert len(df) == 3


def test_teb_range(csv_cache, reset_table):
    df = xa.get_daily("teb-SH000300", start="20070101", end="20200212")
    assert round(df[df["date"] == "20200207"].iloc[0]["e"], 1) == 31168.6


@pytest.mark.skip
def test_get_macro():
    df = xa.get_daily("mcq-MAC_INDUSTRY_AGR_PRODUCT_IDX_QUARTER", start="20180101")
    assert df.iloc[0]["wheat"] == 0
