from arbitrage.public_markets._bitfinex import Bitfinex


class BitfinexEUR(Bitfinex):
    def __init__(self):
        super().__init__("EUR", "btceur")
