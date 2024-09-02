# Copyright (C) 2013, Maxime Biais <maxime@biais.org>

# import base64
# import hashlib
# import hmac
import json

# import sys
import urllib.error
import urllib.parse
import urllib.request

from arbitrage import config
from arbitrage.private_markets.market import Market, TradeException


class PrivateBitstampUSD(Market):
    balance_url = "https://www.bitstamp.net/api/balance/"
    buy_url = "https://www.bitstamp.net/api/buy/"
    sell_url = "https://www.bitstamp.net/api/sell/"

    def __init__(self):
        super().__init__()
        self.username = config.bitstamp_username
        self.password = config.bitstamp_password
        self.currency = "USD"
        self.get_info()

    def _send_request(self, url, params={}, extra_headers=None):
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
        }
        if extra_headers is not None:
            for k, v in extra_headers.items():
                headers[k] = v

        params["user"] = self.username
        params["password"] = self.password
        postdata = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, postdata, headers=headers)
        response = urllib.request.urlopen(req)
        code = response.getcode()
        if code == 200:
            jsonstr = response.read().decode("utf-8")
            return json.loads(jsonstr)
        return None

    def _buy(self, amount, price):
        """Create a buy limit order"""
        params = {"amount": amount, "price": price}
        response = self._send_request(self.buy_url, params)
        if "error" in response:
            raise TradeException(response["error"])

    def _sell(self, amount, price):
        """Create a sell limit order"""
        params = {"amount": amount, "price": price}
        response = self._send_request(self.sell_url, params)
        if "error" in response:
            raise TradeException(response["error"])

    def get_info(self):
        """Get balance"""
        response = self._send_request(self.balance_url)
        if response:
            self.btc_balance = float(response["btc_available"])
            self.usd_balance = float(response["usd_available"])
