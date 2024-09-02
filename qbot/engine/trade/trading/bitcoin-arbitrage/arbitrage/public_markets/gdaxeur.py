from arbitrage.public_markets._gdax import GDAX


class GDAXEUR(GDAX):
    def __init__(self):
        super().__init__("EUR", "BTC-EUR")
