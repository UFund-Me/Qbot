import backtrader as bt
import backtrader.indicators as ind  # 导入策略分析模块


class MyStrategy(bt.Strategy):
    # 先在 __init__ 中提前算好指标
    def __init__(self):
        sma1 = ind.SimpleMovingAverage(self.data)
        ema1 = ind.ExponentialMovingAverage()
        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1
        # 生成交易信号
        self.buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)

    # 在 next 中直接调用计算好的指标
    def next(self):
        if self.buy_sig:
            self.buy()


class MyStrategy2(bt.Strategy):
    def __init__(self):
        self.sma5 = ind.SimpleMovingAverage(period=5)  # 5日均线
        self.sma10 = ind.SimpleMovingAverage(period=10)  # 10日均线
        # bt.And 中所有条件都满足时返回 1；有一个条件不满足就返回 0
        self.And = bt.And(self.data > self.sma5, self.data > self.sma10, self.sma5 > self.sma10)
        # bt.Or 中有一个条件满足时就返回 1；所有条件都不满足时返回 0
        self.Or = bt.Or(self.data > self.sma5, self.data > self.sma10, self.sma5 > self.sma10)
        # bt.If(a, b, c) 如果满足条件 a，就返回 b，否则返回 c
        self.If = bt.If(self.data > self.sma5, 1000, 5000)
        # bt.All,同 bt.And
        self.All = bt.All(self.data > self.sma5, self.data > self.sma10, self.sma5 > self.sma10)
        # bt.Any，同 bt.Or
        self.Any = bt.Any(self.data > self.sma5, self.data > self.sma10, self.sma5 > self.sma10)
        # bt.Max，返回同一时刻所有指标中的最大值
        self.Max = bt.Max(self.data, self.sma10, self.sma5)
        # bt.Min，返回同一时刻所有指标中的最小值
        self.Min = bt.Min(self.data, self.sma10, self.sma5)
        # bt.Sum，对同一时刻所有指标进行求和
        self.Sum = bt.Sum(self.data, self.sma10, self.sma5)
        # bt.Cmp(a,b), 如果 a>b ，返回 1；否则返回 -1
        self.Cmp = bt.Cmp(self.data, self.sma5)


class TALibStrategy(bt.Strategy):
    def __init__(self):
        # 计算 5 日均线
        bt.talib.SMA(self.data.close, timeperiod=5)
        bt.indicators.SMA(self.data, period=5)
        # 计算布林带
        bt.talib.BBANDS(self.data, timeperiod=25)
        bt.indicators.BollingerBands(self.data, period=25)