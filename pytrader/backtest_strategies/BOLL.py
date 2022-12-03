from pandas import DataFrame
from talib._ta_lib import BBANDS, MA_Type

from backtest_strategies.backtest_strategy_template import BacktestStrategyTemplate


class BOLLStrategy(BacktestStrategyTemplate):
    """BOLL指标策略"""

    def get_singal(self, df: DataFrame):
        upper, middle, lower = self.get_boll(df)
         # 获取最新价格
        current_price = df.close[-1]

        # 穿越上轨，买入信号
        if current_price > upper[-1]:
            return 1

        # 穿越下轨，卖出信号
        if current_price < lower[-1]:
            return  0

        return -1

    def get_boll(self, df: DataFrame):
        return BBANDS(df.close, timeperiod=14, nbdevup=2, nbdevdn=2, matype=0)

    def show_score(self, df, ax):
        upper, middle, lower = self.get_boll(df)
        df['upper'] = upper
        df['middle'] = middle
        df['lower'] = lower
        df[['close','middle', 'upper','lower']].plot(ax=ax, grid=True, title='BOOL', figsize=(20, 10))
