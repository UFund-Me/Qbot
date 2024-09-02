from arbitrage.public_markets._gdax import GDAX


class GDAXUSD(GDAX):
    def __init__(self):
        super().__init__("USD", "BTC-USD")
