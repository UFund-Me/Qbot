'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-18 18:06:06
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-18 18:14:39
FilePath: /Qbot/qbot/strategies/adx_strategy.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 获取股票数据并进行量化回测——基于ADX和MACD趋势策略

https://blog.csdn.net/ndhtou222/article/details/121219649

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
#不显示警告信息
import warnings
warnings.filterwarnings('ignore')

from get_stack_data import get_from_tushare
import pyfolio as pf
import talib as ta

def adx_strategy(df,ma1=13,ma2=55,ma3=89,adx=25):
    #计算MACD和ADX指标
    df['EMA1'] = ta.EMA(df.close,ma1)
    df['EMA2'] = ta.EMA(df.close,ma2)
    df['EMA3'] = ta.EMA(df.close,ma3)
    df['MACD'],df['MACDSignal'],df['MACDHist'] = ta.MACD(df.close,12,26,9)
    df['ADX'] = ta.ADX(df.high,df.low,df.close,14)
    #设计买卖信号:21日均线大于42日均线且42日均线大于63日均线;ADX大于前值小于25；MACD大于前值
    df['Buy_Sig'] =(df['EMA1']>df['EMA2'])&(df['EMA2']>df['EMA3'])&(df['ADX']<=adx)\
                    &(df['ADX']>df['ADX'].shift(1))&(df['MACDHist']>df['MACDHist'].shift(1))
    df.loc[df.Buy_Sig,'Buy_Trade'] = 1
    df.loc[df.Buy_Trade.shift(1)==1,'Buy_Trade'] = " "
    #避免最后三天内出现交易
    df.Buy_Trade.iloc[-3:]  = " " 
    df.loc[df.Buy_Trade==1,'Buy_Price'] = df.close
    df.Buy_Price = df.Buy_Price.ffill()
    df['Buy_Daily_Return']= (df.close - df.Buy_Price)/df.Buy_Price
    df.loc[df.Buy_Trade.shift(3)==1,'Sell_Trade'] = -1
    df.loc[df.Sell_Trade==-1,'Buy_Total_Return'] = df.Buy_Daily_Return
    df.loc[(df.Sell_Trade==-1)&(df.Buy_Daily_Return==0),'Buy_Total_Return'] = \
                                (df.Buy_Price - df.Buy_Price.shift(1))/df.Buy_Price.shift(1)
    df.loc[(df.Sell_Trade==-1)&(df.Buy_Trade.shift(1)==1),'Buy_Total_Return'] = \
                                (df.close-df.Buy_Price.shift(2))/df.Buy_Price.shift(2)
    #返回策略的日收益率
    return df.Buy_Total_Return.fillna(0)

df=get_from_tushare('300002')
df.close.plot(figsize=(12,6))
plt.title('神州泰岳股价走势\n2010-2021',size=15)

pf.create_simple_tear_sheet((df.close.pct_change()).fillna(0).tz_localize('UTC'))

pf.create_simple_tear_sheet(adx_strategy(df).tz_localize('UTC'))