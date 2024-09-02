import sys

sys.path.append("../")
import unittest

from arbitrage import arbitrer

depths1 = {
    "BitstampEUR": {
        "asks": [
            {"amount": 4, "price": 32.8},
            {"amount": 8, "price": 32.9},
            {"amount": 2, "price": 33.0},
            {"amount": 3, "price": 33.6},
        ],
        "bids": [
            {"amount": 2, "price": 31.8},
            {"amount": 4, "price": 31.6},
            {"amount": 6, "price": 31.4},
            {"amount": 2, "price": 30},
        ],
    },
    "KrakenEUR": {
        "asks": [
            {"amount": 1, "price": 34.2},
            {"amount": 2, "price": 34.3},
            {"amount": 3, "price": 34.5},
            {"amount": 3, "price": 35.0},
        ],
        "bids": [
            {"amount": 2, "price": 33.2},
            {"amount": 3, "price": 33.1},
            {"amount": 5, "price": 32.6},
            {"amount": 10, "price": 32.3},
        ],
    },
}

depths2 = {
    "BitstampEUR": {
        "asks": [
            {"amount": 4, "price": 32.8},
            {"amount": 8, "price": 32.9},
            {"amount": 2, "price": 33.0},
            {"amount": 3, "price": 33.6},
        ]
    },
    "KrakenEUR": {
        "bids": [
            {"amount": 2, "price": 33.2},
            {"amount": 3, "price": 33.1},
            {"amount": 5, "price": 32.6},
            {"amount": 10, "price": 32.3},
        ]
    },
}

depths3 = {
    "BitstampEUR": {
        "asks": [
            {"amount": 1, "price": 34.2},
            {"amount": 2, "price": 34.3},
            {"amount": 3, "price": 34.5},
            {"amount": 3, "price": 35.0},
        ]
    },
    "KrakenEUR": {
        "bids": [
            {"amount": 2, "price": 33.2},
            {"amount": 3, "price": 33.1},
            {"amount": 5, "price": 32.6},
            {"amount": 10, "price": 32.3},
        ]
    },
}


class TestArbitrage(unittest.TestCase):
    def setUp(self):
        self.arbitrer = arbitrer.Arbitrer()
        self.arbitrer.max_tx_volume = 10000

    def test_getprofit1(self):
        self.arbitrer.depths = depths2
        profit, vol, wb, ws = self.arbitrer.get_profit_for(
            0, 0, "BitstampEUR", "KrakenEUR"
        )
        assert 80 == int(profit * 100)
        assert vol == 2

    def test_getprofit2(self):
        self.arbitrer.depths = depths2
        profit, vol, wb, ws = self.arbitrer.get_profit_for(
            2, 1, "BitstampEUR", "KrakenEUR"
        )
        assert 159 == int(profit * 100)
        assert vol == 5

    def test_getprofit3(self):
        self.arbitrer.depths = depths3
        profit, vol, wb, ws = self.arbitrer.get_profit_for(
            2, 1, "BitstampEUR", "KrakenEUR"
        )
        assert profit == 0
        assert vol == 0


if __name__ == "__main__":
    unittest.main()
