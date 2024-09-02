from arbitrage.public_markets._bitflyer import BitFlyer


class BitFlyerUSD(BitFlyer):
    def __init__(self):
        super().__init__("USD", "BTC_USD")
