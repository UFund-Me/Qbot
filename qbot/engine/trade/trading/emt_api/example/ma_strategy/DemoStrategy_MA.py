# -*-coding:utf-8-*-
__author__ = "Administrator"

import matplotlib.pyplot as plt
import numpy as np

# reload(sys)
# sys.setdefaultencoding('Cp1252')
import pandas as pd
from EmQuantAPI import *  # noqa: F403

stock = pd.DataFrame()
MAstock = {}


def trade(data):
    # 计算长线金叉，长线死叉，短线金叉，短线死叉，长线金叉全部买入，长线死叉全部卖出，短线金叉买入30%，短线死叉卖出30%
    data.ix[
        (data["MA_5"].shift(1) < data["MA_10"].shift(1))
        & (data["MA_5"] > data["MA_10"])
        & (data["VOLUME"] > 0),
        "POSITION",
    ] = 0.3
    data.ix[
        (data["MA_5"].shift(1) > data["MA_10"].shift(1))
        & (data["MA_5"] < data["MA_10"])
        & (data["VOLUME"] > 0),
        "POSITION",
    ] = -0.3
    data.ix[
        (data["MA_10"].shift(1) < data["MA_15"].shift(1))
        & (data["MA_10"] > data["MA_15"])
        & (data["VOLUME"] > 0),
        "POSITION",
    ] = 1
    data.ix[
        (data["MA_10"].shift(1) > data["MA_15"].shift(1))
        & (data["MA_10"] < data["MA_15"])
        & (data["VOLUME"] > 0),
        "POSITION",
    ] = -1
    # POSITION：买卖点，TRUEPOSITION：实际持仓，TYPE：实际买卖点，STOCKNUMBER：持仓数量，CAPITAL：流动资金，STOCKAMOUNT：持仓总额，REVNUE：市值,DD:回撤率
    # 首次出现长线金叉时设为首次买入点
    if len(data[(data["POSITION"] == 1)]) == 0:
        startposition = data["DATES"].tolist()[-1]
        data["TRUEPOSITION"] = 0
        data["TYPE"] = 0
        data["STOCKNUMBER"] = 0
        data["CAPITAL"] = capital
        data["STOCKAMOUNT"] = 0
        data["REVNUE"] = capital
        data["MAX"] = capital
        data["DD"] = 0
        return data
    else:
        startposition = data[(data["POSITION"] == 1)]["DATES"].tolist()[0]
        first = data["DATES"].tolist()[0]
        data.ix[
            (data["DATES"] >= first) & (data["DATES"] < startposition), "POSITION"
        ] = 0
        data = data.fillna(0)
        position = data["POSITION"].tolist()
        Trueposition = []
        Trueposition.append(position[0])
        # 计算实际买卖点，满仓时不再买入卖出，非满仓时执行买入卖出
        for i in range(0, len(position) - 1):
            try:
                if (position[i + 1] + Trueposition[i]) >= 0 and (
                    position[i + 1] + Trueposition[i]
                ) <= 1:
                    Trueposition.append(position[i + 1] + Trueposition[i])
                elif (position[i + 1] + Trueposition[i]) > 1:
                    Trueposition.append(1)
                elif (position[i + 1] + Trueposition[i]) < 0:
                    Trueposition.append(0)
            except Exception:
                pass
        data.insert(0, "TRUEPOSITION", 0)
        data["TRUEPOSITION"] = np.array(Trueposition)  # 实际仓位
        data["TYPE"] = data["TRUEPOSITION"] - data["TRUEPOSITION"].shift(1)
        data["TYPE"] = data["TYPE"].fillna(0)  # 减仓幅度
        DATA = data[data["TYPE"] != 0]
        DATA = DATA.reset_index()  # 发生仓位变化的表
        for j in range(0, len(DATA)):
            # 首次全仓买入时计算持仓数量和流动资金，CAPITAL为流动资金
            if j == 0:
                DATA.ix[j, "STOCKNUMBER"] = capital // DATA.ix[j, "CLOSE"] // 100 * 100
                DATA.ix[j, "CAPITAL"] = (
                    capital - DATA.ix[j, "CLOSE"] * DATA.ix[j, "STOCKNUMBER"]
                )
            else:
                # 实际持仓为0时，卖出持仓的数量和流动资金
                if DATA.ix[j - 1, "TRUEPOSITION"] == 0:
                    DATA.ix[j, "STOCKNUMBER"] = (
                        DATA.ix[j - 1, "CAPITAL"]
                        // DATA.ix[j, "CLOSE"]
                        // 100
                        * 100
                        * DATA.ix[j, "TYPE"]
                    )
                    DATA.ix[j, "CAPITAL"] = (
                        DATA.ix[j - 1, "CAPITAL"]
                        - DATA.ix[j, "CLOSE"] * DATA.ix[j, "STOCKNUMBER"]
                    )
                # 实际持仓不为0时，卖出持仓的数量和流动资金
                else:
                    DATA.ix[j, "STOCKNUMBER"] = (
                        DATA.ix[j - 1, "STOCKNUMBER"]
                        / DATA.ix[j - 1, "TRUEPOSITION"]
                        * DATA.ix[j, "TRUEPOSITION"]
                    )
                    DATA.ix[j, "CAPITAL"] = (
                        DATA.ix[j - 1, "STOCKNUMBER"] - DATA.ix[j, "STOCKNUMBER"]
                    ) * DATA.ix[j, "CLOSE"] + DATA.ix[j - 1, "CAPITAL"]
            data.ix[data["DATES"] == DATA.ix[j, "DATES"], "STOCKNUMBER"] = DATA.ix[
                j, "STOCKNUMBER"
            ]
            data.ix[data["DATES"] == DATA.ix[j, "DATES"], "CAPITAL"] = DATA.ix[
                j, "CAPITAL"
            ]
        # 计算非买卖点的持仓数量、持仓金额、流动资金、市值、回撤率
        data["STOCKNUMBER"] = data["STOCKNUMBER"].fillna(method="pad")
        data["STOCKNUMBER"] = data["STOCKNUMBER"].fillna(0)
        data["CAPITAL"] = data["CAPITAL"].fillna(method="pad")
        data["STOCKAMOUNT"] = data["STOCKNUMBER"] * data["CLOSE"]
        data["REVNUE"] = data["STOCKAMOUNT"] + data["CAPITAL"]
        data["MAX"] = pd.expanding_max(data["REVNUE"])
        data["DD"] = data["REVNUE"] / data["MAX"] - 1
        data["REVNUE"] = data["REVNUE"].fillna(capital)
        return data


# 获取均线短线、长线数据
def ma(MA, Tradedate):
    Ma, Mx = pd.DataFrame(), pd.DataFrame()
    for i in range(len(MA)):
        for j in range(len(Tradedate)):
            try:
                ma = c.css(
                    code,
                    "MA",
                    "Period=1,ispandas=1,AdjustFlag=2,n="
                    + str(MA[i])
                    + ",Tradedate="
                    + Tradedate[j],
                )
                # time.sleep(1)
            except Exception:
                loginResult = c.start("ForceLogin=1")
                ma = c.css(
                    code,
                    "MA",
                    "Period=1,ispandas=1,AdjustFlag=2,n="
                    + str(MA[i])
                    + ",Tradedate="
                    + Tradedate[j],
                )
            ma.insert(0, "Tradedate", Tradedate[j])
            Ma = Ma.append(ma)
        Mx = pd.concat([Ma, Mx], axis=1, ignore_index=True)
        Ma = pd.DataFrame()
    Mx = Mx[[0, 2, 5, 8]]
    Mx.rename(columns={0: "Tradedate", 8: "MA_5", 5: "MA_10", 2: "MA_15"}, inplace=True)
    return Mx


# 登录Choice接口
loginResult = c.start("ForceLogin=1")
# 获取股票池   #获取当日的上证50指数成分股票
code = c.sector("2000043296", "2016-12-31")
# code=["000002.SZ","600004.SH"]#code=c.sector("2000043296",time.strftime("%Y-%m-%d"))
code = ["600519.SH", "600999.SH", "601318.SH", "600837.SH"]
index = "000016.SH"
startdate = "20170101"  # 设置起始日期
enddate = "20170630"  # 设置截止日期
MA = [5, 10, 15]  # 设置均线短线、长线周期
capital = 1000000  # 设置初始资金
Tradedate = []
FORMAT = "%d-%02d-%02d"
# 获取交易日序列
date = c.tradedates(startdate, enddate)
# 获取交易日序列八位标准格式
for i in range(len(date.Dates)):
    list1 = date.Dates[i].split("/")
    Tradedate.append(FORMAT % (int(list1[0]), int(list1[1]), int(list1[2])))

# 获取均线短线、长线数据
Mx = ma(MA, Tradedate)

# 获取股票的不复权和后复权收盘价：CLOSE，成交量：VOLUME
stockdata = c.csd(code, "CLOSE,VOLUME", startdate, enddate, "ispandas=1,AdjustFlag=2")
stockdata1 = c.csd(code, "CLOSE", startdate, enddate, "ispandas=1,AdjustFlag=1")
stockdata = stockdata[["CLOSE", "VOLUME"]]
stockdata.rename(columns={"CLOSE": "ADJCLOSE"}, inplace=True)

# 调用函数计算金叉，死叉
for i in range(0, len(code)):
    data = pd.concat(
        [stockdata1.ix[code[i]], stockdata.ix[code[i]], Mx.ix[code[i], [1, 2, 3]]],
        axis=1,
    )
    data = data.dropna(axis=0, how="any")
    data = trade(data)
    # 计算每个代码的最大回撤率：RETREAT、收益率：REVNUE
    RETREAT = data.sort_values(by="DD").iloc[0]["DD"]
    REVNUE = (data.ix[-1, "REVNUE"] - capital) / capital
    MAstock[code[i]] = [RETREAT, REVNUE]
    data = data.set_index("DATES")
    # 获取每个代码的每日收益率变化值
    data[code[i] + "_RTN"] = (data["REVNUE"] / capital) - 1
    if i == 0:
        stock = data[code[i] + "_RTN"]
    else:
        stock = pd.concat([stock, data[code[i] + "_RTN"]], axis=1)
MAstock = pd.DataFrame(MAstock, index=["RETREAT", "REVNUE"])
MAstock = MAstock.T
# 个股最大回撤率
RETREATMAX = MAstock.sort_values(by="RETREAT").iloc[0]["RETREAT"]
print("最大回撤率为%s：" % RETREATMAX)
# 输出股票池的回撤率和收益变化率数据
MAstock.to_csv("MAstock.csv")
# 计算得到股票池的收益率变化均值
combine = pd.DataFrame(stock.mean(1), columns=["RTN"])

# 上证50指数
indexdata = c.csd(
    index, "CLOSE", startdate, enddate, "rowindex=2,ispandas=1,AdjustFlag=2"
)
# 计算上证指数收益率变化值
indexdata["000016.SH"] = (indexdata["CLOSE"] / indexdata.ix[0, "CLOSE"]) - 1
# 绘制上证指数和股票池收益率曲线变化曲线
indexdata["COMBINE"] = combine["RTN"]
finaldata = indexdata[["000016.SH", "COMBINE"]]
finaldata[["000016.SH", "COMBINE"]].plot(figsize=(10, 8))
plt.legend()
plt.xlabel("date")
plt.ylabel("revnue")
plt.title("CombineRevnue")
plt.show()
