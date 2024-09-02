from arbitrage.public_markets._bitflyer import BitFlyer


class BitFlyerEUR(BitFlyer):
    def __init__(self):
        super().__init__("EUR", "BTC_EUR")
