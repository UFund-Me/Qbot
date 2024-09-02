from qbot.engine.trade.engine_apis.btc.btc_trade_engine import (
    BinanceTradeEngine,
    CcxtTradeEngine,
    # HuobiTradeEngine,
    OkxTradeEngine,
)


class BtcTradeEngine:
    def __init__(self, account, trade_opts: dict, syslog_obj=None):
        self.account = account
        self.strategy = trade_opts["strategy"]
        self.syslog = syslog_obj
        self.trade_engine = None

        if trade_opts["platform"] == "欧易OKX":
            self.trade_engine = OkxTradeEngine(self.account, trade_opts, syslog_obj)
        elif trade_opts["platform"] == "币安Binance":
            self.trade_engine = BinanceTradeEngine(self.account, trade_opts, syslog_obj)
        else:
            self.trade_engine = CcxtTradeEngine(self.account, trade_opts, syslog_obj)

        if not self.trade_engine:
            logger.error("trade engine is null")
            return

    def login(self):
        uid = self.account["uid"]
        apikey = self.account["apikey"]
        secretkey = self.account["secretkey"]

        print(uid, apikey, secretkey)

    def start_trade(self):
        self.syslog.re_print("BtcTradeEngine start trade ...\n")
        pass

    def get_balance(self):
        pass

    def get_positions(self):
        # 获取登录账户的持仓，如登录多个账户需要指定账户ID
        poses = self.trade_engine.get_positions()
        print(f"get_positions poes={poses}")

    def get_all_tickers(self):
        pass

    def get_order_book(self, symbol="BTCUSDT"):
        pass

    def get_account(self):
        pass

    def get_asset_balance(self):
        pass

    def order_market_buy(self, symbol, quantity):
        pass


if __name__ == "__main__":
    trade_opts = {
        "class": "虚拟盘",
        "platform": "欧易OKX",
        "trade_type": "BTC",
        "trade_code": "ETHUSDT",
        "strategy": "单因子-相对强弱指数RSI",
    }

    from qbot.common.file_utils import file2dict
    from qbot.engine.config import BTC_REAL_ACCOUNT, BTC_SIM_ACCOUNT

    # 实盘交易
    real_accounts = file2dict(BTC_SIM_ACCOUNT)
    print(real_accounts[trade_opts["platform"]])

    trade_engine = BtcTradeEngine(
        account=real_accounts[trade_opts["platform"]],
        trade_opts=trade_opts,
        syslog_obj=None,
    )
    trade_engine.login()
    trade_engine.get_balance()
    trade_engine.get_positions()
    trade_engine.start_trade()
    if trade_opts["platform"] not in real_accounts:
        logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

    run_sim_test = False
    if run_sim_test:
        # 虚拟交易
        trade_opts["class"] = "实盘"
        trade_opts["platform"] = "BTCUSDT"
        sim_accounts = file2dict(BTC_REAL_ACCOUNT)

        trade_engine = BtcTradeEngine(
            account=sim_accounts[trade_opts["platform"]],
            trade_opts=trade_opts,
            syslog_obj=None,
        )
        trade_engine.login()
        trade_engine.get_balance()
        trade_engine.get_position()
        trade_engine.start_trade()
        if trade_opts["platform"] not in sim_accounts:
            logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")
