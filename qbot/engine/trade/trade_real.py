import easytrader

from qbot.common.file_utils import file2dict
from qbot.common.logging.logger import LOGGER as logger


class RealTradeEngine:
    def __init__(self, trade_opts: dict, syslog_obj, user=None):
        if syslog_obj:
            self.syslog = syslog_obj
        else:
            logger.error("syslog_obj is null.")
            return

        self.syslog.re_print("RealTradeEngine start init ...\n")

        if trade_opts:
            logger.info(trade_opts)
        else:
            logger.error("trade_opts is empty.")
            return

        if not user:
            if trade_opts["trade_type"] == "股票":
                from qbot.engine.config import STOCK_REAL_ACCOUNT

                accounts = file2dict(STOCK_REAL_ACCOUNT)

                from qbot.engine.trade.engine_apis.stocks.stock_engine import (
                    StockTradeEngine,
                )

                if trade_opts["platform"] not in accounts:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")
                    return

                self.trade_engine = StockTradeEngine(
                    account=accounts[trade_opts["platform"]],
                    trade_opts=trade_opts,
                    syslog_obj=self.syslog,
                )
                self.trade_engine.login()

                if trade_opts["platform"] == "华泰证券":
                    self.user = easytrader.use("ht_client")
                    self.user.prepare(
                        "华泰证券",
                        username = accounts["华泰证券"]["user"],
                        password = accounts["华泰证券"]["password"],
                    )
                elif trade_opts["platform"] == "通达信":
                    self.user = easytrader.use("tongda")
                    self.user.prepare(
                        "通达信",
                        username = accounts["通达信"]["user"],
                        password = accounts["通达信"]["password"],
                    )
                elif trade_opts["platform"] == "银河证券":
                    self.user = easytrader.use("yinhe")
                    self.user.prepare(
                        "银河证券",
                        username = accounts["银河证券"]["user"],
                        password = accounts["银河证券"]["password"],
                    )
                elif trade_opts["platform"] == "同花顺":
                    self.user = easytrader.use("tonghuashun")
                    self.user.prepare(
                        "同花顺",
                        username = accounts["同花顺"]["user"],
                        password = accounts["同花顺"]["password"],
                    )
                elif trade_opts["platform"] == "雪球":
                    self.user = easytrader.use("xuqiu")
                    self.user.prepare(
                        "雪球",
                        username = accounts["雪球"]["user"],
                        password = accounts["雪球"]["password"],
                    )
                else:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")
            elif trade_opts["trade_type"] == "基金":
                from qbot.engine.config import FUNDS_REAL_ACCOUNT

                accounts = file2dict(FUNDS_REAL_ACCOUNT)

            elif trade_opts["trade_type"] == "期货":
                from qbot.engine.config import FUTURES_REAL_ACCOUNT

                accounts = file2dict(FUTURES_REAL_ACCOUNT)

                from qbot.engine.trade.engine_apis.futures.futures_engine import (
                    FuturesTradeEngine,
                )

                btc_engine = FuturesTradeEngine(
                    accounts[trade_opts["platform"]], trade_opts, self.syslog
                )
                btc_engine.start_trade()
                if trade_opts["platform"] not in accounts:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

            elif trade_opts["trade_type"] == "BTC":
                from qbot.engine.config import BTC_REAL_ACCOUNT

                accounts = file2dict(BTC_REAL_ACCOUNT)

                from qbot.engine.trade.engine_apis.btc.btc_engine import BtcTradeEngine

                btc_engine = BtcTradeEngine(
                    accounts[trade_opts["platform"]], trade_opts, self.syslog
                )
                btc_engine.start_trade()
                if trade_opts["platform"] not in accounts:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

            elif trade_opts["trade_type"] == "期权":
                from qbot.engine.config import OPTIONS_REAL_ACCOUNT

                accounts = file2dict(OPTIONS_REAL_ACCOUNT)

            else:
                logger.error("当前还不支持该交易标的, 请联系微信 Yida_Zhang2")
        else:
            self.user = user

        if not self.trade_engine:
            logger.error("trade engine is null")
            return

    def login(self):
        self.trade_engine.login()

    def get_cash(self):
        self.trade_engine.get_cash()

    def get_positions(self):
        self.trade_engine.get_positions()

    def load_strategy(self):
        pass

    def start_trade(self):
        self.trade_engine.start_trade()

    def close(self):
        self.trade_engine.close()


if __name__ == "__main__":
    trade_opts = {
        "class": "实盘",
        "platform": "掘金",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }

    # 实盘交易
    sim_trade_engine = SimTradeEngine(trade_opts=trade_opts, syslog_obj=None)
    sim_trade_engine.login()
    sim_trade_engine.get_cash()
    sim_trade_engine.get_positions()
    sim_trade_engine.start_trade()
    sim_trade_engine.close()

    # 虚拟交易
    trade_opts["class"] = "虚拟盘"
    trade_opts["platform"] = "东方财富"
    real_accounts = file2dict(STOCK_SIM_ACCOUNT)

    real_trade_engine = RealTradeEngine(trade_opts=trade_opts, syslog_obj=None)
    real_trade_engine.login()
    real_trade_engine.get_cash()
    real_trade_engine.get_positions()
    real_trade_engine.start_trade()
    if trade_opts["platform"] not in sim_accounts:
        logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")
