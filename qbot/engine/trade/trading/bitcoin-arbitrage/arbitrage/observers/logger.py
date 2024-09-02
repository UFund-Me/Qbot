import logging

from arbitrage.observers.observer import Observer


class Logger(Observer):
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
        logging.info(
            "profit: %f USD with volume: %f BTC - buy from %s sell to %s ~%.2f%%"
            % (profit, volume, kask, kbid, perc)
        )
