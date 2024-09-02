import json
import urllib.error
import urllib.parse
import urllib.request

from arbitrage.public_markets.market import Market


class Binance(Market):
    def __init__(self, currency, code):
        super().__init__(currency)
        self.code = code
        self.update_rate = 30

    def update_depth(self):
        url = "https://api.binance.com/api/v1/depth?symbol=%s" % self.code
        req = urllib.request.Request(url, headers={"Accept": "*/*"})
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode("utf8"))
        self.depth = self.format_depth(depth)

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x[0]), reverse=reverse)
        r = []
        for i in l:
            r.append({"price": float(i[0]), "amount": float(i[1])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth["bids"], True)
        asks = self.sort_and_format(depth["asks"], False)
        return {"asks": asks, "bids": bids}
