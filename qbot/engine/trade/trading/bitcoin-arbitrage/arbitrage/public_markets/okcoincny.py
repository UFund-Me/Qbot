from arbitrage.public_markets._okcoin import OKCoin


class OKCoinCNY(OKCoin):
    def __init__(self):
        super().__init__("CNY", "btc_cny")
