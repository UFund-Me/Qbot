from pandas import DataFrame
from talib._ta_lib import *

from backtest_strategies.backtest_strategy_template import BacktestStrategyTemplate


class RSIStrategy(BacktestStrategyTemplate):

    # 买入线
    lower_rsi = 40

    # 卖出线
    upper_rsi = 65

    def get_singal(self, df: DataFrame):
        rsi = self.get_scores(df)[-1]
        if rsi < self.lower_rsi:
            return 1

        if rsi > self.upper_rsi:
            return 0

        return -1

    def get_scores(self, df: DataFrame):
        return RSI(df.close, 21)
