from arbitrage.public_markets._bitfinex import Bitfinex


class BitfinexUSD(Bitfinex):
    def __init__(self):
        super().__init__("USD", "btcusd")
