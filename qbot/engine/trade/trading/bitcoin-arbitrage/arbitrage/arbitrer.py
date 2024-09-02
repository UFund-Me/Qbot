# Copyright (C) 2013, Maxime Biais <maxime@biais.org>

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, wait

from arbitrage import config, observers, public_markets  # noqa:F401


class Arbitrer(object):
    def __init__(self):
        self.markets = []
        self.observers = []
        self.depths = {}
        self.init_markets(config.markets)
        self.init_observers(config.observers)
        self.max_tx_volume = config.max_tx_volume
        self.threadpool = ThreadPoolExecutor(max_workers=10)

    def init_markets(self, markets):
        self.market_names = markets
        for market_name in markets:
            try:
                exec("import arbitrage.public_markets." + market_name.lower())
                market = eval(
                    "arbitrage.public_markets."
                    + market_name.lower()
                    + "."
                    + market_name
                    + "()"
                )
                self.markets.append(market)
            except (ImportError, AttributeError) as e:
                print(
                    "%s market name is invalid: Ignored (you should check your config file)"
                    % (market_name)
                )

    def init_observers(self, _observers):
        self.observer_names = _observers
        for observer_name in _observers:
            try:
                exec("import arbitrage.observers." + observer_name.lower())
                observer = eval(
                    "arbitrage.observers."
                    + observer_name.lower()
                    + "."
                    + observer_name
                    + "()"
                )
                self.observers.append(observer)
            except (ImportError, AttributeError) as e:
                print(
                    "%s observer name is invalid: Ignored (you should check your config file)"
                    % (observer_name)
                )

    def get_profit_for(self, mi, mj, kask, kbid):
        if (
            self.depths[kask]["asks"][mi]["price"]
            >= self.depths[kbid]["bids"][mj]["price"]
        ):
            return 0, 0, 0, 0

        max_amount_buy = 0
        for i in range(mi + 1):
            max_amount_buy += self.depths[kask]["asks"][i]["amount"]
        max_amount_sell = 0
        for j in range(mj + 1):
            max_amount_sell += self.depths[kbid]["bids"][j]["amount"]
        max_amount = min(max_amount_buy, max_amount_sell, self.max_tx_volume)

        buy_total = 0
        w_buyprice = 0
        for i in range(mi + 1):
            price = self.depths[kask]["asks"][i]["price"]
            amount = (
                min(max_amount, buy_total + self.depths[kask]["asks"][i]["amount"])
                - buy_total
            )
            if amount <= 0:
                break
            buy_total += amount
            if w_buyprice == 0:
                w_buyprice = price
            else:
                w_buyprice = (
                    w_buyprice * (buy_total - amount) + price * amount
                ) / buy_total

        sell_total = 0
        w_sellprice = 0
        for j in range(mj + 1):
            price = self.depths[kbid]["bids"][j]["price"]
            amount = (
                min(max_amount, sell_total + self.depths[kbid]["bids"][j]["amount"])
                - sell_total
            )
            if amount < 0:
                break
            sell_total += amount
            if w_sellprice == 0 or sell_total == 0:
                w_sellprice = price
            else:
                w_sellprice = (
                    w_sellprice * (sell_total - amount) + price * amount
                ) / sell_total

        profit = sell_total * w_sellprice - buy_total * w_buyprice
        return profit, sell_total, w_buyprice, w_sellprice

    def get_max_depth(self, kask, kbid):
        i = 0
        if len(self.depths[kbid]["bids"]) != 0 and len(self.depths[kask]["asks"]) != 0:
            while (
                self.depths[kask]["asks"][i]["price"]
                < self.depths[kbid]["bids"][0]["price"]
            ):
                if i >= len(self.depths[kask]["asks"]) - 1:
                    break
                i += 1
        j = 0
        if len(self.depths[kask]["asks"]) != 0 and len(self.depths[kbid]["bids"]) != 0:
            while (
                self.depths[kask]["asks"][0]["price"]
                < self.depths[kbid]["bids"][j]["price"]
            ):
                if j >= len(self.depths[kbid]["bids"]) - 1:
                    break
                j += 1
        return i, j

    def arbitrage_depth_opportunity(self, kask, kbid):
        maxi, maxj = self.get_max_depth(kask, kbid)
        best_profit = 0
        best_i, best_j = (0, 0)
        best_w_buyprice, best_w_sellprice = (0, 0)
        best_volume = 0
        for i in range(maxi + 1):
            for j in range(maxj + 1):
                profit, volume, w_buyprice, w_sellprice = self.get_profit_for(
                    i, j, kask, kbid
                )
                if profit >= 0 and profit >= best_profit:
                    best_profit = profit
                    best_volume = volume
                    best_i, best_j = (i, j)
                    best_w_buyprice, best_w_sellprice = (w_buyprice, w_sellprice)
        return (
            best_profit,
            best_volume,
            self.depths[kask]["asks"][best_i]["price"],
            self.depths[kbid]["bids"][best_j]["price"],
            best_w_buyprice,
            best_w_sellprice,
        )

    def arbitrage_opportunity(self, kask, ask, kbid, bid):
        perc = (bid["price"] - ask["price"]) / bid["price"] * 100
        profit, volume, buyprice, sellprice, weighted_buyprice, weighted_sellprice = (
            self.arbitrage_depth_opportunity(kask, kbid)
        )
        if volume == 0 or buyprice == 0:
            return
        perc2 = (1 - (volume - (profit / buyprice)) / volume) * 100
        for observer in self.observers:
            observer.opportunity(
                profit,
                volume,
                buyprice,
                kask,
                sellprice,
                kbid,
                perc2,
                weighted_buyprice,
                weighted_sellprice,
            )

    def __get_market_depth(self, market, depths):
        depths[market.name] = market.get_depth()

    def update_depths(self):
        depths = {}
        futures = []
        for market in self.markets:
            futures.append(
                self.threadpool.submit(self.__get_market_depth, market, depths)
            )
        wait(futures, timeout=20)
        return depths

    def tickers(self):
        for market in self.markets:
            logging.verbose("ticker: " + market.name + " - " + str(market.get_ticker()))

    def replay_history(self, directory):
        import os

        # import pprint

        files = os.listdir(directory)
        files.sort()
        for f in files:
            depths = json.load(open(directory + "/" + f, "r"))
            self.depths = {}
            for market in self.market_names:
                if market in depths:
                    self.depths[market] = depths[market]
            self.tick()

    def tick(self):
        for observer in self.observers:
            observer.begin_opportunity_finder(self.depths)

        for kmarket1 in self.depths:
            for kmarket2 in self.depths:
                if kmarket1 == kmarket2:  # same market
                    continue
                market1 = self.depths[kmarket1]
                market2 = self.depths[kmarket2]
                if (
                    market1["asks"]
                    and market2["bids"]
                    and len(market1["asks"]) > 0
                    and len(market2["bids"]) > 0
                ):
                    if float(market1["asks"][0]["price"]) < float(
                        market2["bids"][0]["price"]
                    ):
                        self.arbitrage_opportunity(
                            kmarket1, market1["asks"][0], kmarket2, market2["bids"][0]
                        )

        for observer in self.observers:
            observer.end_opportunity_finder()

    def loop(self):
        while True:
            self.depths = self.update_depths()
            self.tickers()
            self.tick()
            time.sleep(config.refresh_rate)
