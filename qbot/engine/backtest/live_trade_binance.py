import datetime as dt

import backtrader as bt
from backtrader_binance import BinanceStore

from qbot.engine.tokens import binance_api

# https://github.com/lindomar-oliveira/backtrader-binance


class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(period=14)  # RSI indicator

    def next(self):
        print(
            "Open: {}, High: {}, Low: {}, Close: {}".format(
                self.data.open[0],
                self.data.high[0],
                self.data.low[0],
                self.data.close[0],
            )
        )
        print("RSI: {}".format(self.rsi[0]))

        if not self.position:
            if self.rsi < 30:  # Enter long
                self.buy()
        else:
            if self.rsi > 70:
                self.sell()  # Close long position

    def notify_order(self, order):
        print(order)


if __name__ == "__main__":
    cerebro = bt.Cerebro(quicknotify=True)

    store = BinanceStore(
        api_key=binance_api["apikey"],
        api_secret=binance_api["secretkey"],
        coin_refer="BTC",
        coin_target="USDT",
        testnet=True,
    )

    broker = store.getbroker()
    cerebro.setbroker(broker)

    from_date = dt.datetime.utcnow() - dt.timedelta(minutes=5 * 16)
    data = store.getdata(timeframe_in_minutes=5, start_date=from_date)

    cerebro.addstrategy(RSIStrategy)
    cerebro.adddata(data)
    cerebro.run()
