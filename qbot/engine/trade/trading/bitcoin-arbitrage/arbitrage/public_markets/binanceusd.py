from arbitrage.public_markets._binance import Binance


class BinanceUSD(Binance):
    def __init__(self):
        super().__init__("USD", "BTCUSDT")
