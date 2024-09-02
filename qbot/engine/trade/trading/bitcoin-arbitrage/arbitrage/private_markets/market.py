# Copyright (C) 2013, Maxime Biais <maxime@biais.org>

import logging

from arbitrage.fiatconverter import FiatConverter


class TradeException(Exception):
    pass


class Market:
    def __init__(self):
        self.name = self.__class__.__name__
        self.btc_balance = 0.0
        self.eur_balance = 0.0
        self.usd_balance = 0.0
        self.fc = FiatConverter()

    def __str__(self):
        return "%s: %s" % (
            self.name,
            str(
                {
                    "btc_balance": self.btc_balance,
                    "eur_balance": self.eur_balance,
                    "usd_balance": self.usd_balance,
                }
            ),
        )

    def buy(self, amount, price):
        """Orders are always priced in USD"""
        local_currency_price = self.fc.convert(price, "USD", self.currency)
        logging.info(
            "Buy %f BTC at %f %s (%f USD) @%s"
            % (amount, local_currency_price, self.currency, price, self.name)
        )
        self._buy(amount, local_currency_price)

    def sell(self, amount, price):
        """Orders are always priced in USD"""
        local_currency_price = self.fc.convert(price, "USD", self.currency)
        logging.info(
            "Sell %f BTC at %f %s (%f USD) @%s"
            % (amount, local_currency_price, self.currency, price, self.name)
        )
        self._sell(amount, local_currency_price)

    def _buy(self, amount, price):
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)

    def _sell(self, amount, price):
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)

    def deposit(self):
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)

    def withdraw(self, amount, address):
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)

    def get_info(self):
        raise NotImplementedError("%s.sell(self, amount, price)" % self.name)
