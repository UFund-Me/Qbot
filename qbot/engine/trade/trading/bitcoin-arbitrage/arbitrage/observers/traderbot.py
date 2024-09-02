import logging
import time

from arbitrage import config
from arbitrage.fiatconverter import FiatConverter

# from arbitrage.observers.emailer import send_email
from arbitrage.observers.observer import Observer


class TraderBot(Observer):
    def __init__(self):
        self.clients = {
            # TODO: move that to the config file
            # "BitstampUSD": bitstampusd.PrivateBitstampUSD(),
        }
        self.fc = FiatConverter()
        self.trade_wait = 120  # in seconds
        self.last_trade = 0
        self.potential_trades = []

    def begin_opportunity_finder(self, depths):
        self.potential_trades = []

    def end_opportunity_finder(self):
        if not self.potential_trades:
            return
        self.potential_trades.sort(key=lambda x: x[0])
        # Execute only the best (more profitable)
        self.execute_trade(*self.potential_trades[0][1:])

    def get_min_tradeable_volume(self, buyprice, usd_bal, btc_bal):
        min1 = float(usd_bal) / ((1 + config.balance_margin) * buyprice)
        min2 = float(btc_bal) / (1 + config.balance_margin)
        return min(min1, min2)

    def update_balance(self):
        for kclient in self.clients:
            self.clients[kclient].get_info()

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
        if profit < config.profit_thresh or perc < config.perc_thresh:
            logging.verbose(
                "[TraderBot] Profit or profit percentage lower than" + " thresholds"
            )
            return
        if kask not in self.clients:
            logging.warn(
                "[TraderBot] Can't automate this trade, client not "
                + "available: %s" % kask
            )
            return
        if kbid not in self.clients:
            logging.warn(
                "[TraderBot] Can't automate this trade, "
                + "client not available: %s" % kbid
            )
            return
        volume = min(config.max_tx_volume, volume)

        # Update client balance
        self.update_balance()
        max_volume = self.get_min_tradeable_volume(
            buyprice, self.clients[kask].usd_balance, self.clients[kbid].btc_balance
        )
        volume = min(volume, max_volume, config.max_tx_volume)
        if volume < config.min_tx_volume:
            logging.warn(
                "Can't automate this trade, minimum volume transaction"
                + " not reached %f/%f" % (volume, config.min_tx_volume)
            )
            logging.warn(
                "Balance on %s: %f USD - Balance on %s: %f BTC"
                % (
                    kask,
                    self.clients[kask].usd_balance,
                    kbid,
                    self.clients[kbid].btc_balance,
                )
            )
            return
        current_time = time.time()
        if current_time - self.last_trade < self.trade_wait:
            logging.warn(
                "[TraderBot] Can't automate this trade, last trade "
                + "occured %.2f seconds ago" % (current_time - self.last_trade)
            )
            return
        self.potential_trades.append(
            [
                profit,
                volume,
                kask,
                kbid,
                weighted_buyprice,
                weighted_sellprice,
                buyprice,
                sellprice,
            ]
        )

    def watch_balances(self):
        pass

    def execute_trade(
        self,
        volume,
        kask,
        kbid,
        weighted_buyprice,
        weighted_sellprice,
        buyprice,
        sellprice,
    ):
        self.last_trade = time.time()
        logging.info("Buy @%s %f BTC and sell @%s" % (kask, volume, kbid))
        self.clients[kask].buy(volume, buyprice)
        self.clients[kbid].sell(volume, sellprice)
