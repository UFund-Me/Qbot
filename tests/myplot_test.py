'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-24 10:25:21
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-04-13 22:17:32
FilePath: /Qbot/myplot.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import tushare as ts # 导入tushare库
import pandas as pd # 导入pandas库
import matplotlib.pyplot as plt # 导入matplotlib库
from mpl_finance import candlestick_ochl # 导入candlestick_ochl函数
from matplotlib.pylab import date2num # 导入date2num函数
import datetime # 导入datetime库
import talib # 导入talib库

# 指定字体
plt.rcParams['font.sans-serif']=['Arial Unicode MS']
# plt.rcParams['axes.unicode_minus']=False

# 获取贵州茅台从2018年元旦至2023年3月20日的行情数据
start_date = '2018-01-01' # 起始日期
end_date = '2023-03-20' # 结束日期
df = ts.get_k_data('600519', start=start_date, end=end_date) # 获取贵州茅台的K线数据

# 计算MACD指标
df['EMA12'] = talib.EMA(df['close'], timeperiod=12) # 计算12日指数移动平均线
df['EMA26'] = talib.EMA(df['close'], timeperiod=26) # 计算26日指数移动平均线
df['DIF'] = df['EMA12'] - df['EMA26'] # 计算DIF
df['DEA'] = talib.EMA(df['DIF'], timeperiod=9) # 计算DEA
df['MACD'] = 2 * (df['DIF'] - df['DEA']) # 计算MACD

# 画图展示
df['date'] = pd.to_datetime(df['date']) # 将日期转换为datetime格式
df['date'] = df['date'].apply(date2num) # 将日期转换为数字
df_values = [tuple(vals) for vals in df[['date', 'open', 'close', 'high', 'low']].values] # 将数据转换为元组

# fig, ax = plt.subplots(figsize=(20, 10)) # 创建画布
# candlestick_ochl(ax, df_values, width=0.6, colorup='red', colordown='green', alpha=0.8) # 绘制K线图
# plt.plot(df['date'], df['DIF'], label='DIF') # 绘制DIF曲线
# plt.plot(df['date'], df['DEA'], label='DEA') # 绘制DEA曲线
# plt.bar(df['date'], df['MACD'], label='MACD', width=0.03 * len(df)) # 绘制MACD柱状图
# plt.legend() # 显示图例
# plt.show() # 显示图形
# plt.legend()
# plt.show()

fig, ax = plt.subplots(figsize=(20, 10)) # 创建画布
candlestick_ochl(ax, df_values, width=0.6, colorup='red', colordown='green', alpha=0.8) # 绘制K线图
plt.plot(df['date'], df['DIF'], label='DIF') # 绘制DIF曲线
plt.plot(df['date'], df['DEA'], label='DEA') # 绘制DEA曲线
plt.bar(df['date'], df['MACD'], label='MACD', width=0.03 * len(df)) # 绘制MACD柱状图
plt.legend() # 显示图例
plt.xticks(rotation=30) # 旋转横轴刻度标签
ax.xaxis_date() # 将横轴刻度设为日期格式
plt.title('贵州茅台从2018年元旦至2023年3月20日的行情数据')
plt.show() # 显示图形
