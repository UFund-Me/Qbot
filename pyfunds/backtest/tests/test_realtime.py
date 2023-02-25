import sys

sys.path.insert(0, "../")
import xalpha as xa
import pytest
import pandas as pd

gf = xa.rfundinfo("001469")


def test_rfundinfo():
    gf.info()
    assert gf.code == "001469"


def test_review(capsys):
    st1 = xa.policy.buyandhold(gf, start="2018-08-10", end="2019-01-01")
    st2 = xa.policy.scheduled_tune(
        gf,
        totmoney=1000,
        times=pd.date_range("2018-01-01", "2019-01-01", freq="W-MON"),
        piece=[(0.1, 2), (0.15, 1)],
    )
    check = xa.review([st1, st2], ["Plan A", "Plan Z"])
    assert isinstance(check.content, str) == True
    conf = {}
    check.notification(conf)
    captured = capsys.readouterr()
    assert captured.out == "没有提醒待发送\n"
    check.content = "a\nb"
    check.notification(conf)
    captured = capsys.readouterr()
    assert captured.out == "邮件发送失败\n"
