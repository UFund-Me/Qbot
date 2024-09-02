from arbitrage.public_markets._kraken import Kraken


class KrakenUSD(Kraken):
    def __init__(self):
        super().__init__("USD", "XXBTZUSD")
