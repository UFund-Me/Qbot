import json
import os
import time

from arbitrage.observers.observer import Observer


class HistoryDumper(Observer):
    out_dir = "history/"

    def __init__(self):
        try:
            os.mkdir(self.out_dir)
        except Exception:
            pass

    def begin_opportunity_finder(self, depths):
        filename = self.out_dir + "order-book-" + str(int(time.time())) + ".json"
        fp = open(filename, "w")
        json.dump(depths, fp)

    def end_opportunity_finder(self):
        pass

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
        pass
