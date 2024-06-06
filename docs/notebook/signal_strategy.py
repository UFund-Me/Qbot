import backtrader as bt


# 自定义信号指标
class MySignal(bt.Indicator):
    lines = ('signal',)  # 声明 signal 线，交易信号放在 signal line 上
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)


# 定义交易信号1
class SMACloseSignal(bt.Indicator):
    lines = ('signal',)
    params = (('period', 30),)

    def __init__(self):
        self.lines.signal = self.data - bt.indicators.SMA(period=self.p.period)


# 定义交易信号2
class SMAExitSignal(bt.Indicator):
    lines = ('signal',)
    params = (('p1', 5), ('p2', 30),)

    def __init__(self):
        sma1 = bt.indicators.SMA(period=self.p.p1)
        sma2 = bt.indicators.SMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2


# 实例化大脑
cerebro = bt.Cerebro()

import pandas as pd


def load_data(name):
    df = pd.read_csv('../data/csv/{}.csv'.format(name))
    df['date'] = df['date'].apply(lambda x: str(x))
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    df.dropna(inplace=True)
    return df


df = load_data('000300.SH')


# df_spx = load_data('spx')


def to_backtrader_dataframe(df):
    df.index = pd.to_datetime(df.index)
    df['openinterest'] = 0
    if 'amount' not in df.columns:
        df['amount'] = 0
    df = df[['open', 'high', 'low', 'close', 'volume', 'amount', 'openinterest']]
    return df


df = to_backtrader_dataframe(df)
# 加载数据
cerebro.adddata(bt.feeds.PandasData(dataname=df))
# 添加交易信号1
cerebro.add_signal(bt.SIGNAL_LONG, MySignal, period=30)
# 添加交易信号2
cerebro.add_signal(bt.SIGNAL_LONGEXIT, SMAExitSignal, p1=5, p2=30)

# 添加分析指标
# 返回年初至年末的年度收益率
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
# 计算最大回撤相关指标
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
# 计算年化收益：日度收益
cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns', tann=252)
# 计算年化夏普比率：日度收益
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio', timeframe=bt.TimeFrame.Days, annualize=True,
                    riskfreerate=0)  # 计算夏普比率
cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
# 返回收益率时序
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

cerebro.signal_accumulate(False)
cerebro.signal_concurrent(False)
result = cerebro.run()

# 提取结果
print("--------------- AnnualReturn -----------------")
print(result[0].analyzers._AnnualReturn.get_analysis())
print("--------------- DrawDown -----------------")
print(result[0].analyzers._DrawDown.get_analysis())
print("--------------- Returns -----------------")
print(result[0].analyzers._Returns.get_analysis())
print("--------------- SharpeRatio -----------------")
print(result[0].analyzers._SharpeRatio.get_analysis())
print("--------------- SharpeRatio_A -----------------")
print(result[0].analyzers._SharpeRatio_A.get_analysis())

# 常用指标提取
analyzer = {}
# 提取年化收益
analyzer['年化收益率'] = result[0].analyzers._Returns.get_analysis()['rnorm']
analyzer['年化收益率（%）'] = result[0].analyzers._Returns.get_analysis()['rnorm100']
# 提取最大回撤
analyzer['最大回撤（%）'] = result[0].analyzers._DrawDown.get_analysis()['max']['drawdown'] * (-1)
# 提取夏普比率
analyzer['年化夏普比率'] = result[0].analyzers._SharpeRatio_A.get_analysis()['sharperatio']
print(analyzer)
cerebro.plot()
