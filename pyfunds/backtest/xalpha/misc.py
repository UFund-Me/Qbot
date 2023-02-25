# -*- coding: utf-8 -*-
"""
modules for misc crawler without unfied API
"""

import re
import pandas as pd
import datetime as dt
import logging
import numpy as np
from bs4 import BeautifulSoup
from functools import lru_cache

logger = logging.getLogger(__name__)

from xalpha.cons import (
    rget,
    rpost,
    rget_json,
    rpost_json,
    today_obj,
    region_trans,
    holidays,
    _float,
)
from xalpha.universal import lru_cache_time
from xalpha.exceptions import ParserFailure

# 该模块只是保存其他一些爬虫的函数，其接口很不稳定，不提供文档和测试，且随时增删，慎用！


@lru_cache_time(ttl=600, maxsize=64)
def get_ri_status(suburl=None):
    """
    broken due to the website redesign
    """
    if not suburl:
        suburl = "m=cb&a=cb_all"  # 可转债

    # url = "http://www.richvest.com/index.php?"
    url = "http://www.ninwin.cn/index.php?"
    url += suburl
    r = rget(url, headers={"user-agent": "Mozilla/5.0"})
    b = BeautifulSoup(r.text, "lxml")
    cl = []
    for c in b.findAll("th"):
        cl.append(c.text)
    nocl = len(cl)
    rl = []
    for i, c in enumerate(b.findAll("td")):
        if i % nocl == 0:
            r = []
        r.append(c.text)
        if i % nocl == nocl - 1:
            rl.append(r)
    return pd.DataFrame(rl, columns=cl)


@lru_cache_time(ttl=120)
def get_jsl_cb_status():
    url = "https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=%s" % (
        int(dt.datetime.now().timestamp() * 100)
    )
    r = rpost_json(url)
    return [item["cell"] for item in r["rows"]]


@lru_cache_time(ttl=7200, maxsize=512)
def get_sh_status(category="cb", date=None):
    url = "http://query.sse.com.cn/commonQuery.do?jsonCallBack=&"
    if category in ["cb", "kzz"]:
        url += "isPagination=false&sqlId=COMMON_BOND_KZZFLZ_ALL&KZZ=1"
    elif category in ["fund", "fs"]:
        if not date:
            date = today_obj().strftime("%Y%m%d")
        date = date.replace("/", "").replace("-", "")
        url += "&sqlId=COMMON_SSE_FUND_LOF_SCALE_CX_S&pageHelp.pageSize=10000&FILEDATE={date}".format(
            date=date
        )
    else:
        raise ParserFailure("unrecoginzed category %s" % category)

    r = rget_json(
        url,
        headers={
            "user-agent": "Mozilla/5.0",
            "Host": "query.sse.com.cn",
            "Referer": "http://www.sse.com.cn/market/bonddata/data/convertible/",
        },
    )
    return pd.DataFrame(r["result"])


@lru_cache_time(ttl=7200, maxsize=512)
def get_sz_status(category="cb", date=None):
    if not date:
        date = today_obj().strftime("%Y%m%d")
    date = date.replace("/", "").replace("-", "")
    date = date[:4] + "-" + date[4:6] + "-" + date[6:]
    url = "http://www.szse.cn/api/report/ShowReport/data?"
    if category in ["cb", "kzz"]:
        pageno = 1
        data = []
        while True:
            suburl = "SHOWTYPE=JSON&CATALOGID=1277&TABKEY=tab1&PAGENO={pageno}&txtDate={date}".format(
                date=date, pageno=pageno
            )
            r = rget_json(url + suburl)
            if r[0]["data"]:
                data.extend(r[0]["data"])
                pageno += 1
            else:
                break
        # df = pd.DataFrame(r[0]["data"])
        df = pd.DataFrame(data)
        if len(df) == 0:
            return
        pcode = re.compile(r".*&DM=([\d]*)&.*")
        pname = re.compile(r"^([^&]*)&.*")
        df["证券代码"] = df["kzjcurl"].apply(lambda s: re.match(pcode, s).groups()[0])
        df["证券简称"] = df["kzjcurl"].apply(lambda s: re.match(pname, s).groups()[0])
        df["上市日期"] = pd.to_datetime(df["ssrq"])
        df["发行量"] = df["fxlnew"]
        df["换股价格"] = df["kzjg"]
        df["未转股数量"] = df["kzsl"]
        df["未转股比例"] = df["kzbl"]
        df["转股截止日期"] = pd.to_datetime(df["kzzzrq"])
        df = df[["证券代码", "证券简称", "上市日期", "发行量", "换股价格", "未转股数量", "未转股比例", "转股截止日期"]]
        return df


@lru_cache_time(ttl=7200, maxsize=512)
def get_sz_fs(code):
    url = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&\
CATALOGID=1945_LOF&txtQueryKeyAndJC={code}".format(
        code=code
    )
    r = rget_json(url)
    return _float(r[0]["data"][0]["dqgm"]) * 1e4


def get_tdx_holidays(holidays=None, format="%Y-%m-%d"):
    r = rget("https://www.tdx.com.cn/url/holiday/")
    r.encoding = "gbk"
    b = BeautifulSoup(r.text, "lxml")
    l = b.find("textarea").string.split("\n")
    if not holidays:
        holidays = {}
    for item in l:
        if item.strip():
            c = item.split("|")
            if c[2] in region_trans:
                rg = region_trans[c[2]]
                tobj = dt.datetime.strptime(c[0], "%Y%m%d")
                tstr = tobj.strftime(format)
                if rg not in holidays:
                    holidays[rg] = [tstr]
                elif tstr not in holidays[rg]:
                    holidays[rg].append(tstr)
    return holidays


def get_163_fundamentals(code, category="lrb"):
    # category xjllb zcfzb
    url = "http://quotes.money.163.com/service/{category}_{code}.html".format(
        category=category, code=code
    )
    logger.debug("Fetching from %s . in `get_163_fundamentals`" % url)
    df = pd.read_csv(url, encoding="gbk")
    df = df.set_index("报告日期")
    return df.T


@lru_cache()
def get_ttjj_suggestions(keyword):
    url = "http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?callback=&m=1&key={key}".format(
        key=keyword
    )
    r = rget_json(url)
    return r["Datas"]


def get_cb_historical_from_ttjj(code):
    if code.startswith("SH") or code.startswith("SZ"):
        code = code[2:]
    params = {
        "type": "RPTA_WEB_KZZ_LS",
        "sty": "ALL",
        "source": "WEB",
        "p": "1",
        "ps": "8000",
        "st": "date",
        "sr": "1",
        "filter": "(zcode={code})".format(code=code),
    }
    url = "http://datacenter.eastmoney.com/api/data/get"
    data = []
    r = rget_json(url, params=params)
    data.extend(r["result"]["data"])
    if int(r["result"]["pages"]) > 1:
        for i in range(2, int(r["result"]["pages"]) + 1):
            params["p"] = str(i)
            r = rget_json(url, params=params)
            data.extend(r["result"]["data"])
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["DATE"])
    df["bond_value"] = df["PUREBONDVALUE"]
    df["swap_value"] = df["SWAPVALUE"]
    df["close"] = df["FCLOSE"]
    return df[["date", "close", "bond_value", "swap_value"]]


@lru_cache()
def get_fund_list(ft):
    # hh, zq, zs, gp, qdii, fof
    r = rget(
        "http://fund.eastmoney.com/data/FundGuideapi.aspx?\
dt=0&ft={ft}&sd=&ed=&sc=z&st=desc&pi=1&pn=10000&zf=diy&sh=list".format(
            ft=ft
        ),
        headers={
            "Host": "fund.eastmoney.com",
            "Referer": "http://fund.eastmoney.com/daogou/",
        },
    )
    d = eval(r.text.split("=")[1].replace("null", "None"))
    return [code.split(",")[0] for code in d["datas"] if code.strip()]


def update_caldate(path, year, path_out=None):
    """
    Update caldate.csv based on ``cons.holidays["CN"]``
    """
    r = {"cal_date": [], "is_open": []}
    for d in pd.date_range(str(year) + "-01-01", str(year) + "-12-31"):
        r["cal_date"].append(d.strftime("%Y-%m-%d"))
        if d.weekday() in [5, 6]:
            r["is_open"].append(0)
        elif d.strftime("%Y-%m-%d") in holidays["CN"]:
            r["is_open"].append(0)
        else:
            r["is_open"].append(1)
    ncal = pd.DataFrame(r)
    cal = pd.read_csv(path)
    if int(year) <= int(cal.iloc[-1]["cal_date"][:4]):
        raise ValueError("We already have cal date for year %s" % year)
    tcal = pd.concat([cal, ncal], ignore_index=True)
    if path_out is None:
        path_out = path
    tcal.to_csv(path_out, index=False)


## 常见标的合集列表，便于共同分析, 欢迎贡献:)

# 战略配售封基
zlps = ["SZ160142", "SZ161131", "SZ161728", "SH501186", "SH501188", "SH501189"]

# 科创封基
kcfj = [
    "SH501073",
    "SH501075",
    "SH501076",
    "SH501078",
    "SH501079",
    "SH501080",
    "SH501081",
    "SH501082",
    "SH501082",
    "SH501085",
]

# 混合基
hh_cand = [
    "001500",
    "001278",
    "001103",
    "519697",
    "001182",
    "001510",
    "001508",
    "519700",
    "519732",
    "519056",
    "213001",
    "161606",
    "519091",
    "000717",
    "000878",
    "000452",
]

## some small tools and calculators below


def summary_cb(df, l=None, cutoff=5):
    # not functional since richinvest change
    for c in ["转债代码"]:
        df[c] = df[c].apply(lambda s: s.strip())
    for c in ["老式双低", "转债价格", "股票市值", "转债余额"]:
        df[c] = df[c].apply(_float)
    for c in ["转股溢价率", "价值溢价", "税后收益率"]:
        df[c] = df[c].apply(lambda s: float(str(s).strip("%")))
    if l is not None:
        df = df[df["转债代码"].isin(l)]
    d = {}
    for c in ["老式双低", "转债价格", "转股溢价率", "价值溢价", "税后收益率", "股票市值"]:
        if cutoff == 0:
            yj = sorted(df[c])
        else:
            yj = sorted(df[c])[cutoff:-cutoff]
        d[c + "中位数"] = yj[int(len(yj) / 2)]
        d[c + "均值"] = round(np.mean(yj), 3)
    d["破面值转债数目"] = len([v for v in df["转债价格"] if v < 100])
    d["总转债余额"] = round(np.sum(df["转债余额"]), 0)
    return d
