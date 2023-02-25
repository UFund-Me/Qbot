import sys

sys.path.insert(0, "../")
from xalpha import remain
import pandas as pd
import pytest

rem = [
    [pd.Timestamp("2017-02-09"), 20],
    [pd.Timestamp("2017-02-19"), 30],
    [pd.Timestamp("2017-02-21"), 10.6],
]

_errmsg = "One cannot move share before the lastest operation"


def test_buy():
    assert remain.buy(rem, 2.5, pd.Timestamp("2017-02-21"))[2][1] == 13.1
    assert rem[2][1] == 10.6
    with pytest.raises(Exception) as excinfo:
        remain.buy(rem, 2.5, pd.Timestamp("2017-02-20"))
    assert str(excinfo.value) == _errmsg


def test_sell():
    assert remain.sell(rem, 25, pd.Timestamp("2017-02-21"))[0][1][1] == 5
    assert remain.sell(rem, 250, pd.Timestamp("2017-02-21"))[0] == rem
    assert len(remain.sell(rem, 60.596, pd.Timestamp("2017-02-21"))[1]) == 0


def test_trans():
    with pytest.raises(Exception) as excinfo:
        remain.trans(rem, 0.9, pd.Timestamp("2017-02-21"))
    assert str(excinfo.value) == _errmsg
    assert remain.trans(rem, 1.2, "2020-01-01")[2][1] == 12.72
    assert rem[1][1] == 30
    assert len(remain.trans([], 0, "2018-01-01")) == 0
