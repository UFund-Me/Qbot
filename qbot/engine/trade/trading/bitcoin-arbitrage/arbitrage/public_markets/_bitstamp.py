import json
import urllib.error
import urllib.parse
import urllib.request

from arbitrage.public_markets.market import Market


class Bitstamp(Market):
    def __init__(self, currency, code):
        super().__init__(currency)
        self.code = code
        self.update_rate = 20

    def update_depth(self):
        url = "https://www.bitstamp.net/api/v2/order_book/" + self.code
        req = urllib.request.Request(
            url,
            None,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)",
            },
        )
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode("utf8"))
        self.depth = self.format_depth(depth)

    def sort_and_format(self, l, reverse):
        r = []
        for i in l:
            r.append({"price": float(i[0]), "amount": float(i[1])})
        r.sort(key=lambda x: float(x["price"]), reverse=reverse)
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth["bids"], True)
        asks = self.sort_and_format(depth["asks"], False)
        return {"asks": asks, "bids": bids}
