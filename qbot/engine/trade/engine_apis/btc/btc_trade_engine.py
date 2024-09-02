from qbot.common.logging.logger import LOGGER as logger

# ref: https://mp.weixin.qq.com/s/tQCmrQ3iWxND0VPABYWW2g


class BinanceTradeEngine:
    def __init__(self, account, trade_opts: dict, syslog_obj=None):
        self.account = account
        self.trade_opts = trade_opts
        self.strategy = trade_opts["strategy"]
        self.syslog = syslog_obj

        from binance.client import Client

        api_key = self.account["apikey"]
        api_secret = self.account["secretkey"]

        logger.info(f"api_key: {api_key}")
        logger.info(f"api_secret: {api_secret}")

        self.client = Client(api_key, api_secret)

    # 获取市场价格
    def get_all_tickers(self):

        prices = self.client.get_all_tickers()
        logger.info(prices)
        return prices

    # 获取订单簿深度
    def get_order_book(self, symbol="BTCUSDT"):

        depth = self.client.get_order_book(symbol)
        logger.info(depth)
        return depth

    # 获取账户信息
    def get_account(self):

        account = self.client.get_account()
        logger.info(account)
        return account

    # 获取账户余额
    def get_balance(self, asset="BTC"):

        balances = self.client.get_asset_balance(asset)
        logger.info(balances)
        return balances

    # 获取账户持仓
    def get_positions(self, asset="BTC"):

        balances = self.client.get_positions(asset)
        logger.info(balances)
        return balances

    # 市价买入
    def order_market_buy(self, symbol="BTCUSDT", quantity=0.001):
        from binance.exceptions import BinanceAPIException, BinanceOrderException

        try:
            order = self.client.order_market_buy(symbol, quantity)
            logger.info(order)
        except BinanceAPIException as err:
            # 捕获API错误
            logger.error(err)
            return err
        except BinanceOrderException as err:
            # 捕获订单错误
            logger.error(err)
            return err
        return True

    # 限价卖出
    def order_limit_sell(self, symbol="BTCUSDT", quantity=0.001, price="50000"):
        from binance.exceptions import BinanceAPIException, BinanceOrderException

        try:
            order = self.client.order_limit_sell(symbol, quantity, price)
            logger.info(order)
        except BinanceAPIException as err:
            # 捕获API错误
            logger.error(err)
            return err
        except BinanceOrderException as err:
            # 捕获订单错误
            logger.error(err)
            return err
        return True


import base64
# import hashlib
import hmac
import json
import time

import requests


class OkxTradeEngine:
    def __init__(self, account, trade_opts: dict, syslog_obj=None):
        self.account = account
        self.trade_opts = trade_opts
        self.strategy = trade_opts["strategy"]
        self.syslog = syslog_obj

        # 替换为你的API密钥、秘密密钥和Passphrase
        api_key = self.account["apikey"]
        api_secret = self.account["secretkey"]
        passphrase = self.account["passphrase"]

        # OKX API基础URL
        self.base_url = "https://www.okx.com"

    def sign(self, message, secret):
        mac = hmac.new(
            bytes(secret, encoding="utf8"),
            bytes(message, encoding="utf-8"),
            digestmod="sha256",
        )
        return base64.b64encode(mac.digest()).decode()

    def get_timestamp(self):
        return str(int(time.time()))

    def get_headers(self, method, endpoint, api_key="", api_secret="", passphrase=""):
        timestamp = self.get_timestamp()
        message = timestamp + method + endpoint
        signature = self.sign(message, self.api_secret)

        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }
        return headers

    # 获取BTC/USDT市场价格
    def get_ticker(self, symbol):
        endpoint = f"/api/v5/market/ticker?instId={symbol}"
        url = self.base_url + endpoint
        response = requests.get(url)
        return response.json()

    # 获取市场价格
    def get_all_tickers(self):

        pass

    # 获取账户持仓
    def get_positions(self):

        pass

    # 获取订单簿深度
    def get_order_book(self, symbol="BTCUSDT"):

        pass

    # 获取账户信息
    def get_account(self):

        account = self.client.get_account()
        logger.info(account)
        return account

    # 获取账户余额
    def get_balance(self, asset="BTC"):

        def get_account_balance():
            endpoint = "/api/v5/account/balance"
            url = self.base_url + endpoint
            headers = self.get_headers("GET", endpoint)
            response = requests.get(url, headers=headers)
            return response.json()

        try:
            balance = get_account_balance()
            print(json.dumps(balance, indent=4))
            return balance
        except requests.exceptions.RequestException as err:
            logger.error(err)
        except Exception as err:
            logger.error(err)

    def order_market_buy(self, symbol="BTCUSDT", quantity=0.001, side="buy"):
        return self.place_order(symbol, quantity, side)

    def order_limit_sell_2(
        self, symbol="BTCUSDT", quantity=0.001, side="sell", price="50000"
    ):
        return self.place_order(symbol, quantity, side, price)

    # 市价买入
    def place_order(self, symbol="BTCUSDT", quantity=0.001, side="buy"):
        endpoint = "/api/v5/trade/order"
        url = base_url + endpoint

        order_data = {
            "instId": symbol,
            "tdMode": "cash",  # "cash" for spot trading
            "side": side,
            "ordType": "limit" if price else "market",
            "sz": quantity,
        }
        if price:
            order_data["px"] = price

        body = json.dumps(order_data)
        headers = self.get_headers("POST", endpoint)
        response = requests.post(url, headers=headers, data=body)
        return response.json()

    # 限价卖出
    def order_limit_sell(self, symbol="BTCUSDT", quantity=0.001, price="50000"):
        from binance.exceptions import BinanceAPIException, BinanceOrderException

        try:
            order = self.client.order_limit_sell(symbol, quantity, price)
            logger.info(order)
        except BinanceAPIException as err:
            # 捕获API错误
            logger.error(err)
            return err
        except BinanceOrderException as err:
            # 捕获订单错误
            logger.error(err)
            return err
        return True


class HuobiTradeEngine:
    def __init__(self, account, trade_opts: dict, syslog_obj=None):
        self.account = account
        self.trade_opts = trade_opts
        self.syslog = syslog_obj

        from binance.client import Client

        api_key = self.account["apikey"]
        api_secret = self.account["secretkey"]

        self.client = Client(api_key, api_secret)

    # 获取市场价格
    def get_all_tickers(self):

        prices = self.client.get_all_tickers()
        logger.info(prices)
        return prices

    # 获取订单簿深度
    def get_order_book(self, symbol="BTCUSDT"):

        depth = self.client.get_order_book(symbol)
        logger.info(depth)
        return depth

    # 获取账户信息
    def get_account(self):

        account = self.client.get_account()
        logger.info(account)
        return account

    # 获取账户余额
    def get_balance(self, asset="BTC"):

        balances = self.client.get_asset_balance(asset)
        logger.info(balances)
        return balances

    # 市价买入
    def order_market_buy(self, symbol="BTCUSDT", quantity=0.001):
        from binance.exceptions import BinanceAPIException, BinanceOrderException

        try:
            order = self.client.order_market_buy(symbol, quantity)
            logger.info(order)
        except BinanceAPIException as err:
            # 捕获API错误
            logger.error(err)
            return err
        except BinanceOrderException as err:
            # 捕获订单错误
            logger.error(err)
            return err
        return True

    # 限价卖出
    def order_market_sell(self, symbol="BTCUSDT", quantity=0.001, price="50000"):
        from binance.exceptions import BinanceAPIException, BinanceOrderException

        try:
            order = self.client.order_limit_sell(symbol, quantity, price)
            logger.info(order)
        except BinanceAPIException as err:
            # 捕获API错误
            logger.error(err)
            return err
        except BinanceOrderException as err:
            # 捕获订单错误
            logger.error(err)
            return err
        return True


class CcxtTradeEngine:
    def __init__(self, account, trade_opts: dict, syslog_obj):
        self.account = account
        self.trade_opts = trade_opts
        self.syslog = syslog_obj

        import ccxt

        self.exchange = None
        if self.trade_opts["platform"] == "币安Binance":
            # 初始化 Binance 交易所实例
            self.exchange = ccxt.binance(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )

        if self.trade_opts["platform"] == "欧易OKX":
            # 初始化 Binance 交易所实例
            self.exchange = ccxt.okx(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )

        elif self.trade_opts["platform"] == "Bitget":
            # 初始化 Bitget 交易所实例
            self.exchange = ccxt.bitget(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )

        elif self.trade_opts["platform"] == "coinex":
            # 初始化 coinex 交易所实例
            self.exchange = ccxt.coinex(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )

        elif self.trade_opts["platform"] == "kucoin":
            # 初始化 kucoin 交易所实例
            self.exchange = ccxt.kucoin(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )

        elif self.trade_opts["platform"] == "coinbase":
            # 初始化 coinbase 交易所实例
            self.exchange = ccxt.coinbase(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )

        elif self.trade_opts["platform"] == "Bitmart":
            # 初始化 Bitmart 交易所实例
            self.exchange = ccxt.bitmart(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        elif self.trade_opts["platform"] == "bitmex":
            # 初始化 bitmex 交易所实例
            self.exchange = ccxt.bitmex(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        elif self.trade_opts["platform"] == "bingx":
            # 初始化 bingx 交易所实例
            self.exchange = ccxt.bingx(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        elif self.trade_opts["platform"] == "bitget":
            # 初始化 bitget 交易所实例
            self.exchange = ccxt.bitget(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        elif self.trade_opts["platform"] == "okcoin":
            # 初始化 okcoin 交易所实例
            self.exchange = ccxt.okcoin(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        elif self.trade_opts["platform"] == "火币Huobi":
            # 初始化 火币Huobi 交易所实例
            self.exchange = ccxt.huobi(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        elif self.trade_opts["platform"] == "htx":
            # 初始化 htx 交易所实例
            self.exchange = ccxt.htx(
                {
                    "apiKey": self.account["apikey"],  # 替换为你的 API Key
                    "secret": self.account["secretkey"],  # 替换为你的 Secret Key
                }
            )
        else:
            logger.warning(f"{trade_opts['platform']} 还未支持，可联系微信 Yida_Zhang2")

    # 检查交易信号
    def check_trade_signals(self, df):
        last_row = df.iloc[-1]
        previous_row = df.iloc[-2]

        # 买入条件：MACD 越过零线
        if previous_row["macd"] < 0 and last_row["macd"] > 0:
            return "buy"

        # 卖出条件：MACD 低于零线
        if previous_row["macd"] > 0 and last_row["macd"] < 0:
            return "sell"

        return "hold"

    # 获取当前持仓方向和数量
    def get_positions(self, symbol):
        balance = self.exchange.fetch_balance()
        if symbol in balance["total"]:
            return balance["total"][symbol]
        return 0

    # 计算持仓盈亏比例
    def calculate_profit_loss(self, entry_price, current_price):
        return (current_price - entry_price) / entry_price

    # 执行交易
    def execute_trade(self, signal, symbol="BTC/USDT", amount=0.001, entry_price=None):
        base_currency = symbol.split("/")[0]
        position = self.get_positions(symbol)

        if signal == "buy":
            if position <= 0:
                order = self.exchange.create_market_buy_order(symbol, amount)
                logger.info(f"Buy order executed: {order}")
                entry_price = order["price"]
            else:
                logger.info("Already holding a buy position. No action taken.")
        elif signal == "sell":
            if position > 0:
                order = self.exchange.create_market_sell_order(symbol, amount)
                logger.info(f"Sell order executed: {order}")
                entry_price = None
        else:
            logger.error("No buy position to sell. No action taken.")

        # 止盈止损逻辑
        if entry_price:
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker["last"]
            profit_loss_ratio = self.calculate_profit_loss(entry_price, current_price)

            if profit_loss_ratio >= 0.05:  # 止盈条件
                if position > 0:
                    order = self.exchange.create_market_sell_order(symbol, amount)
                    logger.info(f"Take profit order executed: {order}")
                    entry_price = None
            elif profit_loss_ratio <= -0.03:  # 止损条件
                if position > 0:
                    order = self.exchange.create_market_sell_order(symbol, amount)
                    logger.info(f"Stop loss order executed: {order}")
                    entry_price = None
