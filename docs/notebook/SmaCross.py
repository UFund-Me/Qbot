import backtrader as bt


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        super().__init__()
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position.size:
            if self.crossover > 0:  # if fast crosses slow to the upside
                # self.order_target_size(target=1)  # enter long
                self.order_target_percent(target=1)
                # self.buy()
        elif self.crossover < 0:  # in the market & cross to the downside
            # self.order_target_size(target=0)  # close long position
            # self.close()
            self.order_target_percent(target=0)
