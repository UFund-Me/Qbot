#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ****************************************************************************
#  Description:  收盘价大于简单移动平均价。
#       1、仅制作单股票的日K图，添加网格
#       2、添加网格
#       3、优化x轴和y轴
#       4、给x轴的刻度加上日期标签
#       5、添加均线
#  
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************


import pandas
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mpf

dir_name = './'

def paint_dayk(code):
    # 1、获取数据
    stock_data = pandas.read_csv(dir_name + code + '.txt')  # 读取数据
    begin = len(stock_data) - 120  # 取最近120天的数据
    if begin < 0:  # 如果上市未满120天，则从上市当天开始显示
        begin = 0
    # 2、画日K图
    fig = plt.figure(  # 添加fig对象
        figsize=(54, 28),  # 设置fig大小，长和宽，单位为英寸
        dpi=120)  # 每英寸的像素点数
    gs = fig.add_gridspec(1, 1)  # 在fig中添加一个一行一列的网格
    ax = fig.add_subplot(gs[0, 0])  # 在fig中添加网格的第一块，并返回一套坐标轴
    mpf.candlestick2_ochl(  # 调用candlestick2_ochl画日K图
        ax,  # 在这套坐标轴内画日K图
        stock_data.open[begin:], stock_data.close[begin:],  # 开盘价和收盘价
        stock_data.high[begin:], stock_data.low[begin:],  # 最高价和最低价
        width=0.8, colorup='red', colordown='green')  # 收盘价大于开盘价则红柱，收盘价小于开盘价则绿柱
    ax.grid(axis='x', linestyle='-.')  # 添加x轴方向的网格
    ax.grid(axis='y', linestyle='-.')  # 添加y轴方向的网格
    ax.yaxis.tick_right()  # 将y轴的数值显示在右边
    ax.set_xlim(0, len(stock_data.index)-begin, 1)  # 设置x轴的范围
    ax.set_xticks(range(0, len(stock_data.index)-begin, 1))  # 设置x轴的刻度
    ax.axes.set_xticklabels(stock_data.week[begin:])

    for label in ax.xaxis.get_ticklabels():  # 设置x轴标签的字体大小
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():  # 设置y轴标签的字体大小
        label.set_fontsize(40)

    # 3、绘制移动平均线图
    stock_data['Ma5'] = stock_data.close.rolling(window=5).mean()  # 求5日均线
    stock_data['Ma10'] = stock_data.close.rolling(window=10).mean()  # 求10日均线
    stock_data['Ma20'] = stock_data.close.rolling(window=20).mean()  # 求20日均线
    ax.plot(
        np.arange(0, len(stock_data.index)-begin),  # [x]的数据范围
        stock_data['Ma5'][begin:],  # [y]的数据范围
        'black',  # 均线颜色
        label='M5',  # 均线标签
        lw=2.5)  # 均线宽度
    ax.plot(np.arange(0, len(stock_data.index)-begin), stock_data['Ma10'][begin:], 'orange', label='M10', lw=2.5)
    ax.plot(np.arange(0, len(stock_data.index)-begin), stock_data['Ma20'][begin:], 'purple', label='M20', lw=2.5)
    # 4、输出日K图
    plt.savefig(dir_name + code + '.jpg')  # 保存图片


def main():
    code = '000001'
    paint_dayk(code)


if __name__ == '__main__':
    main()
