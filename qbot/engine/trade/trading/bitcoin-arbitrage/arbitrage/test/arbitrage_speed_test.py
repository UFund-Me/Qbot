import sys

sys.path.append("../")
import json
import time

import arbitrage
from arbitrage.observers import observer


class TestObserver(observer.Observer):
    def opportunity(
        self,
        profit,
        volume,
        buyprice,
        kask,
        sellprice,
        kbid,
        perc,
        weighted_buyprice,
        weighted_sellprice,
    ):
        print("Time: %.3f" % profit)


def main():
    arbitrer = arbitrage.Arbitrer()
    depths = arbitrer.depths = json.load(open("speed-test.json"))
    start_time = time.time()
    testobs = TestObserver()
    arbitrer.observers = [testobs]
    arbitrer.arbitrage_opportunity(
        "BitstampUSD",
        depths["BitstampUSD"]["asks"][0],
        "KrakenEUR",
        depths["KrakenEUR"]["asks"][0],
    )
    # FIXME: add asserts
    elapsed = time.time() - start_time
    print("Time: %.3f" % elapsed)


if __name__ == "__main__":
    main()
