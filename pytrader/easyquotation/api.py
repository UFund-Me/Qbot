# coding:utf8
from easyquotation.basequotation import BaseQuotation

from . import boc, daykline, hkquote, jsl, sina, tencent, timekline, sinatimekline, minutekline


# pylint: disable=too-many-return-statements
def use(source) -> BaseQuotation:
    if source in ["sina"]:
        return sina.Sina()
    if source in ["jsl"]:
        return jsl.Jsl()
    if source in ["qq", "tencent"]:
        return tencent.Tencent()
    if source in ["boc"]:
        return boc.Boc()
    if source in ["timekline"]:
        return timekline.TimeKline()
    if source in ["minutekline"]:
        return minutekline.MinuteTimeKline()
    if source in ["sinatimekline"]:
        return sinatimekline.SinaTimeKline()
    if source in ["daykline"]:
        return daykline.DayKline()
    if source in ["hkquote"]:
        return hkquote.HKQuote()
    raise NotImplementedError
