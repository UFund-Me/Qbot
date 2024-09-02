import json
import urllib.error
import urllib.parse
import urllib.request

from arbitrage.public_markets.market import Market


class PaymiumEUR(Market):
    def __init__(self):
        super(PaymiumEUR, self).__init__("EUR")
        # bitcoin central maximum call / day = 5000
        # keep 2500 for other operations
        self.update_rate = 24 * 60 * 60 / 2500

    def update_depth(self):
        url = "https://paymium.com/api/data/eur/depth"
        req = urllib.request.Request(
            url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)",
            },
        )
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode("utf8"))
        self.depth = self.format_depth(depth)

    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x["price"]), reverse=reverse)
        r = []
        for i in l:
            r.append({"price": float(i["price"]), "amount": float(i["amount"])})
        return r

    def format_depth(self, depth):
        bids = self.sort_and_format(depth["bids"], True)
        asks = self.sort_and_format(depth["asks"], False)
        return {"asks": asks, "bids": bids}


if __name__ == "__main__":
    market = PaymiumEUR()
    print(market.get_ticker())
