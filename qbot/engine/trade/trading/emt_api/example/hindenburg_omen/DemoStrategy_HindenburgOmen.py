# -*- coding:utf-8 -*-
__author__ = "Administrator"
import sys

from EmQuantAPI import *  # noqa: F403

reload(sys)
sys.setdefaultencoding("Cp1252")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

tcode = {}
codenumber = []
xcode, k, X, Y = [], [], [], []
Rsq = pd.DataFrame()
loginResult = c.start("ForceLogin=1")

index = "000001.SH"  # 上证指数
sectorcode = "2000032255"  # 上证A股成分
startdate = "20160101"  # 起始日期
enddate = "20161231"  # 截止日期
# 后推30日获取

Ndate = c.getdate(enddate, 30)
enddateN30 = Ndate.Dates[0]
date = c.tradedates(startdate, enddateN30)

# 获取上证A股的板块成分，每日新增的代码也获取对应的收盘价数据
for i in range(len(date.Dates) - 30):
    if i == 0:
        code = c.sector(sectorcode, date.Dates[i])
        data = c.csd(code.Codes, "CLOSE", startdate, enddateN30, "Period=1,ispandas=1")
        codenumber = code.Codes
        code2 = code
    else:
        code1 = c.sector(sectorcode, date.Dates[i])
        addcode = [i for i in code1.Codes if i not in code2.Codes]
        if len(addcode) != 0:
            adddata = c.csd(
                addcode, "CLOSE", startdate, enddateN30, "Period=1,ispandas=1"
            )
            data = data.append(adddata)
            codenumber = codenumber + addcode
        code2 = code1
data.to_csv("data.csv")
data = pd.read_csv("data.csv")
data = data.set_index("CODES")
# 获取对比指数收盘价数据
indexdata = c.csd(
    index, "CLOSE", startdate, enddateN30, "Period=1,ispandas=1,rowindex=1"
)
# 板块成分和指数线性回归，并计算30日间隔的Rsq系数
for i in range(len(codenumber)):
    for x, y in zip(data.ix[codenumber[i], "CLOSE"], indexdata["CLOSE"]):
        X.append([float(x)])
        Y.append(float(y))
    for j in range(0, len(Y)):
        try:
            regr = linear_model.LinearRegression()
            regr = regr.fit(X[j : j + 30], Y[j : j + 30])
            regr = regr.score(X[j : j + 30], Y[j : j + 30])
            xcode.append(regr)
            if j + 30 >= len(Y) - 1:
                break
        except Exception:
            xcode.append(0)
    tcode[codenumber[i]] = xcode
    xcode = []
    X = []
    Y = []
Rsq = pd.DataFrame(tcode)
Rsq.to_csv("rsq.csv", index=None)
Rsq = pd.read_csv("rsq.csv")
# 求每日Rsq系数的均值
FORMAT = "%d/%02d/%02d"
Rsq = Rsq.T
mean = pd.DataFrame(Rsq.mean(), columns=["MEAN"])
for i in range(Rsq.columns.size):
    mean["MEAN"] = mean["MEAN"] * len(Rsq) / len(Rsq[Rsq[i] != 0.0])
mean["DATE"] = date.Dates[30:]

# 求每日Rsq系数的均值间隔3日变动幅度超过30%的日期进行标记
for i in range(len(mean) - 33):
    x = (mean.ix[i, "MEAN"] - mean.ix[i + 3, "MEAN"]) / mean.ix[i, "MEAN"]
    if x > 0.3 or x < -0.3:
        k.append(mean.ix[i + 3, "DATE"])
        list1 = mean.ix[i + 3, "DATE"].split("/")
        list1 = FORMAT % (int(list1[0]), int(list1[1]), int(list1[2]))
        indexdata.ix[indexdata["DATES"] == list1, "MARKER"] = 1
    else:
        pass
# 绘制指数收盘价
indexdata = indexdata.set_index("DATES")
indexdata.index = pd.to_datetime(indexdata.index)
# 标记吉登堡凶兆所标记的时间点
for i in range(0, len(indexdata.ix[indexdata["MARKER"] == 1, "CLOSE"])):
    plt.scatter(
        pd.to_datetime((indexdata.ix[indexdata["MARKER"] == 1, "CLOSE"]).index)[i],
        indexdata.ix[indexdata["MARKER"] == 1, "CLOSE"][i],
        color="red",
        marker="o",
    )
indexdata["CLOSE"].plot(figsize=(10, 8))
plt.xlabel("date")
plt.ylabel("close")
plt.title("000001.SH")
plt.show()
