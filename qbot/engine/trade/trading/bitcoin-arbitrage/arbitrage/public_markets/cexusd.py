from arbitrage.public_markets._cex import CEX


class CEXUSD(CEX):
    def __init__(self):
        super().__init__("USD", "USD")
