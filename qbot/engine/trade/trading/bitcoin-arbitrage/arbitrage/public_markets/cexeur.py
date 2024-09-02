from arbitrage.public_markets._cex import CEX


class CEXEUR(CEX):
    def __init__(self):
        super().__init__("EUR", "EUR")
