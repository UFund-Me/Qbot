'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-04-16 01:28:13
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-04-16 01:57:58
FilePath: /Qbot/pytrader/strategies/multi_factor_strategy.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import backtrader as bt
import tushare as ts
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class PEFetcher:
    def __init__(self, ts):
        self.ts = ts

    def get_factor_data(self, symbol, date):
        df = self.ts.get_k_data(symbol, start=date.strftime('%Y-%m-%d'), end=date.strftime('%Y-%m-%d'))
        if len(df) > 0:
            return df.iloc[0]['close'] / df.iloc[0]['eps']
        else:
            return np.nan

class PBFetcher:
    def __init__(self, ts):
        self.ts = ts

    def get_factor_data(self, symbol, date):
        df = self.ts.get_k_data(symbol, start=date.strftime('%Y-%m-%d'), end=date.strftime('%Y-%m-%d'))
        if len(df) > 0:
            return df.iloc[0]['close'] / df.iloc[0]['bvps']
        else:
            return np.nan

class ROEFetcher:
    def __init__(self, ts):
        self.ts = ts

    def get_factor_data(self, symbol, date):
        df = self.ts.pro_bar(
            ts_code=symbol,
            asset='E',
            start_date=date.strftime('%Y%m%d'),
            end_date=date.strftime('%Y%m%d')
        )
        if len(df) > 0:
            return df.iloc[0]['roe']
        else:
            return np.nan


def get_data(symbol, data_fetchers, start_date, end_date):
    ts.set_token('e96f18882532434b7692388cb028eb267d3f0d56845dc92eef06ea4a')
    
    data = {}
    dates = ts.trade_cal()
    trade_dates = dates[dates.isOpen == 1]['calendarDate']
    
    for date in trade_dates:
        hist_data = ts.get_hist_data(symbol, start=date, end=date)
        factors_data = {}
        for factor in data_fetchers:
            factor_data = factor['data_fetcher'].get_factor_data(hist_data, factor['code'])
            factors_data[factor['code']] = factor_data
        data[date] = factors_data
    
    return data


class MultiFactorModelStrategy(bt.Strategy):
    params = (
        ('num_stocks', 10),
    )

    def __init__(self, factors):
        self.factors = factors
        self.coef_ = None

    def calculate_signal(self, data):
        features = []
        for factor in self.factors:
            feature = factor['function'](data)
            if 'scaling' in factor:
                feature = factor['scaling'](feature)
            features.append(feature)

        X = np.array(features).T
        y = data.close[-1] / data.close[-2] - 1 # 当日涨跌幅度作为因变量
        reg = LinearRegression().fit(X, y)

        return reg.coef_

    def rebalance_portfolio(self):
        # 获取当前所有股票的因子数据
        factors_data = {}
        for factor in self.factors:
            data = factor['data_fetcher'].get_factor_data(factor['code'], self.data.datetime.date(0))
            factors_data[factor['code']] = data

        # 合并所有因子数据
        merged_data = pd.concat(factors_data, axis=1)

        # 计算每个股票的综合因子得分
        scores = {}
        for symbol in merged_data.index.levels[1]:
            stock_factors = merged_data.loc[:, symbol].dropna()
            score = np.dot(stock_factors, self.coef_)
            scores[symbol] = score

        # 选择得分最高的股票作为持仓
        top_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.params.num_stocks]
        for symbol, _ in top_stocks:
            current_price = self.data.close[0]
            available_balance = self.broker.get_cash() / current_price
            max_buy_volume = int(available_balance)
            if max_buy_volume > 0:
                buy_volume = min(100, max_buy_volume)
                cost = current_price * buy_volume
                commission = cost * 0.001
                total_cost = cost + commission
                self.buy(size=buy_volume)

    def next(self):
        if not self.position:
            # 如果当前没有持仓，计算因子得分并重新调整组合
            signal = self.calculate_signal(self.data)
            self.coef_ = signal / np.sum(np.abs(signal))
            self.rebalance_portfolio()
        else:
            # 如果当前有持仓，检查是否需要清仓
            positions = self.broker.get_positions()
            for symbol, position in positions.items():
                if not self.getdatabyname(symbol).close:
                    continue
                current_price = self.getdatabyname(symbol).close[0]
                revenue = current_price * position.size
                commission = revenue * 0.001
                total_revenue = revenue - commission
                self.sell(data=self.getdatabyname(symbol), size=position.size)
               

if __name__ == '__main__':
    # 加载数据
    ts.set_token('e96f18882532434b7692388cb028eb267d3f0d56845dc92eef06ea4a')
    pro = ts.pro_api()
    data_fetchers = [
        {'code': 'pe_ttm', 'data_fetcher': PEFetcher(pro)},
        {'code': 'pb', 'data_fetcher': PBFetcher(pro)},
        {'code': 'roe_ttm', 'data_fetcher': ROEFetcher(pro)},
    ]
    data = bt.feeds.PandasData(dataname=get_data('600438.SH', data_fetchers, '2018-01-01', '2021-09-01'))

    # 添加策略
    factors = [
        {'code': 'pe_ttm', 'function': lambda data: data.pe_ttm},
        {'code': 'pb', 'function': lambda data: data.pb},
        {'code': 'roe_ttm', 'function': lambda data: data.roe_ttm},
    ]
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiFactorModelStrategy, factors=factors)

    # 设置初始资金和手续费
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(commission=0.001)

    # 运行回测
    cerebro.adddata(data)
    cerebro.run()

    # 输出回测结果
    final_value = cerebro.broker.getvalue()