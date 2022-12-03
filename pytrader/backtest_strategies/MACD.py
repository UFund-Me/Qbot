from pandas import DataFrame
from talib._ta_lib import *

from backtest_strategies.backtest_strategy_template import BacktestStrategyTemplate


class MACDStrategy(BacktestStrategyTemplate):
    """MACD指标策略"""

    def get_singal(self, df: DataFrame):
        macd_raw, signal, hist  = self.get_score(df)

        macd = macd_raw[-1] - signal[-1]

        if macd > 0:
            return 1

        if macd < 0:
            return 0

        return -1

    def get_score(self, df: DataFrame):
        return MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)

    def show_score(self, df, ax):
        macd_raw, signal, hist  = self.get_score(df)
        macd = macd_raw - signal
        df['macd'] = macd
        df[['macd']].plot(ax=ax, grid=True, title='MACD', figsize=(20, 10))
