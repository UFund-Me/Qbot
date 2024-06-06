# -*- coding:utf-8 -*-
__author__ = "Administrator"
import sys

from EmQuantAPI import *

reload(sys)
sys.setdefaultencoding("Cp1252")
import datetime
import time

import matplotlib.pyplot as plt
import pandas as pd

reportdate, adjustlist = [], []
tcode = {}
revnuedata = pd.DataFrame()


# 筛选EPS、净利润、营业收入、净资产、销售收入增长率、PEG符合高增长条件的股票
def pick(number, startyear, code):
    EpsMr, EPS3, MBREVENUE3 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for i in range(0, number):
        reportdate = str(startyear - 4 + i) + "/12/31"
        # 获取每股收益EPS(基本)：EPS、主营营业收入：MBREVENUE的数据
        data = c.css(
            code.Codes, "EPSBASIC,MBREVENUE", "ispandas=1,ReportDate=" + reportdate
        )
        data.rename(columns=lambda x: x + "_" + reportdate, inplace=True)
        EpsMr = pd.concat(
            [
                EpsMr,
                data[["EPSBASIC" + "_" + reportdate, "MBREVENUE" + "_" + reportdate]],
            ],
            axis=1,
        )
        if i > 2:
            # 计算3年EPS增长率，以及3年销售收入增长率
            EPS3 = (
                (EpsMr[EpsMr.columns[i * 2]] - EpsMr[EpsMr.columns[i * 2 - 2]])
                / EpsMr[EpsMr.columns[i * 2 - 2]]
                + (EpsMr[EpsMr.columns[i * 2 - 2]] - EpsMr[EpsMr.columns[i * 2 - 4]])
                / EpsMr[EpsMr.columns[i * 2 - 4]]
                + (EpsMr[EpsMr.columns[i * 2 - 4]] - EpsMr[EpsMr.columns[i * 2 - 6]])
                / EpsMr[EpsMr.columns[i * 2 - 6]]
            ) / 3
            MBREVENUE3 = (
                (EpsMr[EpsMr.columns[i * 2 + 1]] - EpsMr[EpsMr.columns[i * 2 - 1]])
                / EpsMr[EpsMr.columns[i * 2 - 1]]
                + (EpsMr[EpsMr.columns[i * 2 - 1]] - EpsMr[EpsMr.columns[i * 2 - 3]])
                / EpsMr[EpsMr.columns[i * 2 - 3]]
                + (EpsMr[EpsMr.columns[i * 2 - 3]] - EpsMr[EpsMr.columns[i * 2 - 5]])
                / EpsMr[EpsMr.columns[i * 2 - 5]]
            ) / 3
            EPS3 = pd.DataFrame(EPS3, columns=["EPS3"])
            MBREVENUE3 = pd.DataFrame(MBREVENUE3, columns=["MBREVENUE3"])
            # 获取净利润同比增长率：YOYNI，营业总收入同比增长率：YOYGR，净资产同比增长率：YOYEQUITY的数据
            df = c.css(
                code.Codes,
                "YOYNI,YOYGR,YOYEQUITY",
                "ispandas=1,ReportDate=" + reportdate,
            )
            FinancialData = pd.concat(
                [df[["YOYNI", "YOYGR", "YOYEQUITY"]], EPS3, MBREVENUE3], axis=1
            )
            FinancialData = FinancialData.dropna(axis=0, how="any")
            # 筛选3年EPS增长率大于股票池中间值，筛选3年销售收入增长率大于股票池中间值的股票
            FinancialData = FinancialData.ix[
                (FinancialData["EPS3"] > FinancialData["EPS3"].median())
                & (FinancialData["MBREVENUE3"] > FinancialData["MBREVENUE3"].median())
            ]
            # 筛选所有增长率为正的股票
            FinancialData = FinancialData[FinancialData > 0.0]
            FinancialData = FinancialData.dropna(how="any")
            newcode = FinancialData.index.tolist()
            # 筛选当年PEG<1的的股票
            newcode = c.cps(",".join(newcode), "s2,PEG," + reportdate + ",6", "[s2]<1")
            # tcode为符合持仓的股票池
            tcode[startyear - 3 + i] = newcode.Codes
            FinancialData = pd.DataFrame()
    return tcode


# 获取每年调仓日的持仓数据，包括持仓比例：STOCKPRO，持仓量：STOCKNUMBER，持仓金额：STOCKAMOUNT，流动资金：CAPITAL等
# 获取每年持仓变动明细数据，包括持仓变动量：NUMADJ，买卖类型：TYPE，持仓变动次数：ADJUSTNUMBER，价格：PRICE等
def transfer(number, startyear, code):
    k = 0
    ADJUSTdata, STOCKdata, ADJUST = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for i in range(startyear, endyear):
        try:
            # 获取每年调仓日的股票的简称：NAME，收盘价：CLOSE和市值：MV
            data = c.css(
                ",".join(tcode[i]),
                "NAME,CLOSE,MV",
                "ispandas=1,adjustflag=2,TradeDate=" + adjustlist[i - startyear],
            )
            data.insert(0, "ADJUSTDATE", adjustlist[i - startyear])
        except:
            # 当持仓为空时，判断首次持仓不为空，且前次持仓不为空的，将前次持仓全部卖出
            if tcode[i] == [] and k == 1:
                if tcode[i - 1] != [] and k == 1:
                    ADJUSTdata = STOCKdata[
                        STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]
                    ]
                    ADJUSTdata = pd.DataFrame(
                        ADJUSTdata[["STOCKNUMBER", "ADJUSTDATE", "CLOSE"]]
                    )
                    ADJUSTdata.rename(
                        columns={"STOCKNUMBER": "NUMADJ", "CLOSE": "PRICE"},
                        inplace=True,
                    )
                    ADJUSTdata["NUMADJ"] = (-1) * ADJUSTdata["NUMADJ"]
                    ADJUSTdata["ADJUSTNUMBER"] = i - startyear + 1
                    ADJUSTdata["TYPE"] = -1
                else:
                    pass
            else:
                continue
        # 当持仓不为空时，判断为首次持仓时，全部持仓买入
        if tcode[i] != [] and k == 0:
            data["STOCKPRO"] = data["MV"] / data["MV"].sum()
            data["STOCKNUMBER"] = capital * data["STOCKPRO"] // data["CLOSE"]
            data["STOCKAMOUNT"] = data["STOCKNUMBER"] * data["CLOSE"]
            ADJUSTdata = pd.DataFrame(data[["STOCKNUMBER", "ADJUSTDATE", "CLOSE"]])
            ADJUSTdata.rename(
                columns={"STOCKNUMBER": "NUMADJ", "CLOSE": "PRICE"}, inplace=True
            )
            ADJUSTdata["ADJUSTNUMBER"] = i - startyear + 1
            # TYPE=1时为买入，TYPE=-1为卖出，TYPE=0时无买入卖出
            ADJUSTdata["TYPE"] = 1
            data["CAPITAL"] = capital - data["STOCKAMOUNT"].sum()
            STOCKdata = STOCKdata.append(data)
            ADJUST = ADJUST.append(ADJUSTdata)
            ADJUSTdata = pd.DataFrame()
            k = 1
        # 当持仓不为空时，判断为非首次持仓时，根据前后持仓明细计算持仓变动
        elif tcode[i] != [] and k == 1:
            # 获取调仓当日，调仓前的股票池的收盘价
            data1 = c.css(
                ",".join(tcode[i - 1]),
                "CLOSE",
                "ispandas=1,adjustflag=2,TradeDate=" + adjustlist[i - startyear],
            )
            data["STOCKPRO"] = data["MV"] / data["MV"].sum()
            data["STOCKNUMBER"] = (
                (
                    (
                        STOCKdata[
                            STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]
                        ]["CAPITAL"].sum()
                        / len(tcode[i])
                        + (
                            STOCKdata[
                                STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]
                            ]["STOCKNUMBER"]
                            * data1["CLOSE"]
                        )
                    ).sum()
                )
                * data["STOCKPRO"]
                // data["CLOSE"]
            )
            data["STOCKAMOUNT"] = data["STOCKNUMBER"] * data["CLOSE"]
            # 流动资金=调仓前股票当日持股数量*当日价格+调仓前流动资金-调仓后股票当日持仓金额
            data["CAPITAL"] = (
                STOCKdata[STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]][
                    "CAPITAL"
                ].sum()
                / len(tcode[i])
                + (
                    STOCKdata[STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]][
                        "STOCKNUMBER"
                    ]
                    * data1["CLOSE"]
                )
            ).sum() - (data["STOCKAMOUNT"].sum())
            ADJUSTdata = pd.DataFrame(
                0,
                index=list(set(tcode[i - 1]).union(set(tcode[i]))),
                columns=["NUMADJ"],
            )
            # 当股票调仓前和调仓后都有时，持仓变动=调仓前持股数——调仓后持股数
            ADJUSTdata.ix[[l for l in tcode[i] if l in tcode[i - 1]], "NUMADJ"] = (
                data["STOCKNUMBER"]
                - STOCKdata[STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]][
                    "STOCKNUMBER"
                ]
            )
            # 当股票调仓后新买入时，持仓变动=调仓后持股数
            ADJUSTdata.ix[[l for l in tcode[i] if l not in tcode[i - 1]], "NUMADJ"] = (
                data.ix[[l for l in tcode[i] if l not in tcode[i - 1]], "STOCKNUMBER"]
            )
            # 当股票调仓后全部卖出时，持仓变动=-调仓前持股数
            ADJUSTdata.ix[[l for l in tcode[i - 1] if l not in tcode[i]], "NUMADJ"] = (
                -1
            ) * STOCKdata[STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear - 1]].ix[
                [l for l in tcode[i - 1] if l not in tcode[i]], "STOCKNUMBER"
            ]
            ADJUSTdata["ADJUSTDATE"] = data["ADJUSTDATE"]
            ADJUSTdata.ix[
                [l for l in tcode[i - 1] if l not in tcode[i]], "ADJUSTDATE"
            ] = adjustlist[i - startyear]
            ADJUSTdata["PRICE"] = data["CLOSE"]
            ADJUSTdata.ix[[l for l in tcode[i - 1] if l not in tcode[i]], "PRICE"] = (
                data1.ix[[l for l in tcode[i - 1] if l not in tcode[i]], "CLOSE"]
            )
            ADJUSTdata["ADJUSTNUMBER"] = i - startyear + 1
            # 根据持仓变动的正负判定买卖类型
            ADJUSTdata.ix[ADJUSTdata["NUMADJ"] < 0, "TYPE"] = -1
            ADJUSTdata.ix[ADJUSTdata["NUMADJ"] > 0, "TYPE"] = 1
            ADJUSTdata["TYPE"].fillna(0)
            STOCKdata = STOCKdata.append(data)
            ADJUST = ADJUST.append(ADJUSTdata)
            ADJUSTdata = pd.DataFrame()
    STOCKdata = STOCKdata.reset_index()
    # 输出调仓日当日持仓数据，输出调仓日当日持仓变动数据
    STOCKdata.to_csv("STOCKdata.csv", encoding="gbk")
    ADJUST.to_csv("AdjustData.csv")
    return STOCKdata


# 登录Choice接口
loginResult = c.start("ForceLogin=1")
startyear = 2012  # 设置起始年份
endyear = 2017  # 设置截止年份
index = "000016.SH"  # 以上证指数为标的指数
capital = 10000000  # 设置初始资金
today = datetime.date.today()
codeyear = str(startyear - 4) + "/01/01"
# 筛选上市为起始年份前四年之前上市的股票，009007063为上证50板块
code = c.cps("B_009007063", "s1,LISTDATE", "s1<d(" + codeyear + ")")
# 调仓日期设置为每年4月第一个交易日，判断当前月份是否>3月，大于时调仓次数+1
if datetime.datetime.now().month > 3:
    number = endyear - startyear + 4
else:
    number = endyear - startyear + 3

# 筛选EPS、净利润、营业收入、净资产、销售收入增长率、PEG符合高增长条件的股票
tcode = pick(number, startyear, code)

# 获取每年4月第一周交易日期
for i in range(startyear, endyear):
    adjustdate = c.tradedates(str(i) + "/04/01", str(i) + "/04/20", "period=2")
    adjustlist.append(adjustdate.Dates[0])
# 获取每年调仓日持仓数据和持仓变动数据
STOCKdata = transfer(tcode, startyear, endyear)

# 根据每周持仓情况，计算净值，收益率和最大回撤率
for i in range(startyear, endyear):
    try:
        # 获取每年持仓股票的每周的收盘价
        data = c.csd(
            ",".join(tcode[i]),
            "CLOSE",
            str(i) + "/04/01",
            str(i + 1) + "/03/31",
            "ispandas=1,period=2,adjustflag=2",
        )
    except:
        continue
    data = data.reset_index()
    STOCK = STOCKdata[STOCKdata["ADJUSTDATE"] == adjustlist[i - startyear]]
    # 填充持仓股票每周持股数量
    for n in tcode[i]:
        data.ix[data["CODES"] == n, "STOCKNUMBER"] = STOCK.ix[
            STOCK["CODES"] == n, "STOCKNUMBER"
        ][(STOCK.ix[STOCK["CODES"] == n].index.tolist())[0]]
    data["STOCKAMOUNT"] = data["STOCKNUMBER"] * data["CLOSE"]
    # revnue=pd.DataFrame(((data['STOCKNUMBER']*data['CLOSE']).sum()+STOCK.iat[0,9]),columns=['TOTAL'])
    # 根据日期，分组计算组合市值
    revnue = data.groupby("DATES")[["STOCKAMOUNT"]].sum()
    # 计算组合收益
    revnue["REVNUE"] = revnue["STOCKAMOUNT"] + STOCK.iat[0, 9]
    revnuedata = revnuedata.append(revnue)
    revnue = pd.DataFrame()
    data = pd.DataFrame()
# 计算回撤率
revnuedata["MAX"] = revnuedata["REVNUE"].expanding(min_periods=1).max()
revnuedata["DD"] = revnuedata["REVNUE"] / revnuedata["MAX"] - 1
# 计算最大回撤率
RETREAT = revnuedata.sort_values(by="DD").iloc[0]["DD"]
print("最大回撤率为: ", RETREAT)
# 计算组合收益率
revnuedata["REVNUE"] = (revnuedata["REVNUE"] / capital) - 1

# 获取上证指数每周的收盘价
indexdata = c.csd(
    index,
    "CLOSE",
    str(startyear) + "/04/01",
    str(endyear) + "/03/31",
    "ispandas=1,period=2,Rowindex=2",
)
closef = c.css(index, "CLOSE", "Tradedate=" + adjustlist[0])
# 计算上证指数收益率
indexdata["REVNUE"] = indexdata["CLOSE"] / closef.Data[index][0] - 1

# 绘制收益率曲线
indexdata["COMBINE"] = revnuedata["REVNUE"]
indexdata["000001.SH"] = indexdata["REVNUE"]
finaldata = indexdata[["000001.SH", "COMBINE"]]
finaldata[["000001.SH", "COMBINE"]].plot(figsize=(10, 8))
plt.legend()
plt.xlabel("date")
plt.ylabel("revnue")
plt.title("CombineRevnue")
plt.show()
