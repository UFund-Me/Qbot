import logging
import time

from arbitrage import config
from arbitrage.observers.emailer import send_email
from arbitrage.observers.observer import Observer
from arbitrage.private_markets import bitstampusd, paymium


class SpecializedTraderBot(Observer):
    def __init__(self):
        self.bitstamp = bitstampusd.PrivateBitstampUSD()
        self.btcentral = paymium.PrivatePaymium()
        self.clients = {"BitStampUSD": self.bitstamp, "PaymiumEUR": self.btcentral}
        self.profit_percentage_thresholds = {  # Graph
            "BitStampUSD": {"PaymiumEUR": 3.5},
            "PaymiumEUR": {"BitStampUSD": 1},
        }
        self.trade_wait = 60 * 5  # in seconds
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

    def get_min_tradeable_volume(self, buyprice, eur_bal, btc_bal):
        min1 = float(eur_bal) / ((1.0 + config.balance_margin) * buyprice)
        min2 = float(btc_bal) / (1.0 + config.balance_margin)
        return min(min1, min2) * 0.95

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
        if kask not in self.clients:
            logging.warn("Can't automate this trade, client not available: %s" % (kask))
            return
        if kbid not in self.clients:
            logging.warn("Can't automate this trade, client not available: %s" % (kbid))
            return
        if perc < self.profit_percentage_thresholds[kask][kbid]:
            logging.warn(
                "Can't automate this trade, profit=%f is lower than defined threshold %f"
                % (perc, self.profit_percentage_thresholds[kask][kbid])
            )
            return

        if (
            perc > 20
        ):  # suspicous profit, added after discovering btc-central may send corrupted order book
            logging.warn("Profit=%f seems malformed" % (perc,))
            return

        # Update client balance
        self.update_balance()

        # maximum volume transaction with current balances
        max_volume = self.get_min_tradeable_volume(
            buyprice, self.clients[kask].eur_balance, self.clients[kbid].btc_balance
        )
        volume = min(volume, max_volume, config.max_tx_volume)
        if volume < config.min_tx_volume:
            logging.warn(
                "Can't automate this trade, minimum volume transaction not reached %f/%f"
                % (volume, config.min_tx_volume)
            )
            logging.info(
                "Balance on %s: %f EUR - Balance on %s: %f BTC"
                % (
                    kask,
                    self.clients[kask].eur_balance,
                    kbid,
                    self.clients[kbid].btc_balance,
                )
            )
            return

        current_time = time.time()
        if current_time - self.last_trade < self.trade_wait:
            logging.warn(
                "Can't automate this trade, last trade occured %s seconds ago"
                % (current_time - self.last_trade)
            )
            return

        self.potential_trades.append(
            [profit, volume, kask, kbid, weighted_buyprice, weighted_sellprice]
        )

    def execute_trade(self, volume, kask, kbid, weighted_buyprice, weighted_sellprice):
        self.last_trade = time.time()
        logging.info("Buy @%s %f BTC and sell @%s" % (kask, volume, kbid))
        send_email(
            "Bought @%s %f BTC and sold @%s" % (kask, volume, kbid),
            "weighted_buyprice=%f weighted_sellprice=%f"
            % (weighted_buyprice, weighted_sellprice),
        )
        self.clients[kask].buy(volume)
        self.clients[kbid].sell(volume)
