'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-14 01:49:02
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-14 01:50:11
FilePath: /Qbot/qbot/strategies/util.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import baostock as bs
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt


def computeMACD(code, startdate, enddate):
    login_result = bs.login(user_id='anonymous', password='123456')
    print(login_result)
    # 获取股票日 K 线数据
    rs = bs.query_history_k_data(code,
                                 "date,code,close,tradeStatus",
                                 start_date=startdate,
                                 end_date=enddate,
                                 frequency="d", adjustflag="3")
    # 打印结果集
    result_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        result_list.append(rs.get_row_data())
        df = pd.DataFrame(result_list, columns=rs.fields)
        # 剔除停盘数据
        df2 = df[df['tradeStatus'] == '1']
        # 获取 dif,dea,hist，它们的数据类似是 tuple，且跟 df2 的 date 日期一一对应
        # 记住了 dif,dea,hist 前 33 个为 Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的 3 倍
    # 这里计算的 hist 就是 dif-dea,而很多证券商计算的 MACD=hist*2=(difdea)*2
    dif, dea, hist = ta.MACD(df2['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    df3 = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist':hist[33:]},index=df2['date'][33:], columns=['dif', 'dea','hist'])
    df3.plot(title='MACD')
    plt.show()
    # 寻找 MACD 金叉和死叉
    datenumber = int(df3.shape[0])
    for i in range(datenumber - 1):
        if ((df3.iloc[i, 0] <= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] >= df3.iloc[i + 1, 1])):
            print("MACD 金叉的日期：" + df3.index[i + 1])
    if ((df3.iloc[i, 0] >= df3.iloc[i, 1]) & (df3.iloc[i + 1, 0] <=df3.iloc[i + 1, 1])):
        print("MACD 死叉的日期：" + df3.index[i + 1])
    bs.logout()
    return (dif, dea, hist)

def calculateEMA(period, closeArray, emaArray=[]):
    length = len(closeArray)
    nanCounter = np.count_nonzero(np.isnan(closeArray))
    if not emaArray:
        emaArray.extend(np.tile([np.nan], (nanCounter + period - 1)))
        firstema = np.mean(closeArray[nanCounter:nanCounter + period - 1])
        emaArray.append(firstema)
        for i in range(nanCounter + period, length):
            ema = (2 * closeArray[i] + (period - 1) * emaArray[-1]) / (period + 1)
            emaArray.append(ema)
    return np.array(emaArray)


def calculateMACD(closeArray, shortPeriod=12, longPeriod=26, signalPeriod=9):
    ema12 = calculateEMA(shortPeriod, closeArray, [])
    ema26 = calculateEMA(longPeriod, closeArray, [])
    diff = ema12 - ema26

    dea = calculateEMA(signalPeriod, diff, [])
    macd = (diff - dea)*2

    fast_values = diff   # 快线
    slow_values = dea    # 慢线
    diff_values = macd   # macd
    # return fast_values, slow_values, diff_values  # 返回所有的快慢线和macd值
    return fast_values[-1], slow_values[-1], diff_values[-1]    # 返回最新的快慢线和macd值
    # return round(fast_values[-1],5), round(slow_values[-1],5), round(diff_values[-1],5)

def getMACD():
    data = RequestUtil.sendRequest_GET(UrlConstant.Get_K_Line)
    closeArray = [float(i[4]) for i in data]
    closeArray.reverse()
    return calculateMACD(closeArray)


if __name__ == '__main__':
    code = 'sh.600000'
    startdate = '2022-03-01'
    enddate = '2023-03-18'
    (dif, dea, hist) = computeMACD(code, startdate, enddate)
    print((dif, dea, hist))