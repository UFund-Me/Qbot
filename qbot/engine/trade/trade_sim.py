import easytrader

from qbot.common.file_utils import file2dict
from qbot.common.logging.logger import LOGGER as logger


class SimTradeEngine:
    def __init__(self, trade_opts: dict, syslog_obj, user=None):
        if syslog_obj:
            self.syslog = syslog_obj
        else:
            logger.error("syslog_obj is null.")
            return

        self.syslog.re_print("SimTradeEngine start init ...\n")

        if trade_opts:
            logger.info(f"trade_opts: {trade_opts}")
        else:
            logger.error("trade_opts is empty.")
            return

        self.trade_opts = trade_opts
        if not user:
            if self.trade_opts["trade_type"] == "股票":
                from qbot.engine.config import STOCK_SIM_ACCOUNT

                sim_accounts = file2dict(STOCK_SIM_ACCOUNT)

                from qbot.engine.trade.engine_apis.stocks.stock_engine import (
                    StockTradeEngine,
                )

                self.trade_engine = StockTradeEngine(
                    account=sim_accounts[self.trade_opts["platform"]],
                    trade_opts=trade_opts,
                    syslog_obj=self.syslog,
                )
                self.trade_engine.login()

                if self.trade_opts["platform"] not in sim_accounts:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

                if self.trade_opts["platform"] == "华泰证券":
                    self.user = easytrader.use("ht_client")
                    self.user.prepare(
                        "华泰证券",
                        username=sim_accounts["华泰证券"]["user"],
                        password=accounts["华泰证券"]["password"],
                    )
                elif self.trade_opts["platform"] == "通达信":
                    self.user = easytrader.use("tongda")
                    self.user.prepare(
                        "通达信",
                        username=sim_accounts["通达信"]["user"],
                        password=accounts["通达信"]["password"],
                    )
                elif self.trade_opts["platform"] == "银河证券":
                    self.user = easytrader.use("yinhe")
                    self.user.prepare(
                        "银河证券",
                        username=sim_accounts["银河证券"]["user"],
                        password=accounts["银河证券"]["password"],
                    )
                elif self.trade_opts["platform"] == "同花顺":
                    self.user = easytrader.use("tonghuashun")
                    self.user.prepare(
                        "同花顺",
                        username=sim_accounts["同花顺"]["user"],
                        password=accounts["同花顺"]["password"],
                    )
                elif self.trade_opts["platform"] == "雪球":
                    self.user = easytrader.use("xuqiu")
                    self.user.prepare(
                        "雪球",
                        username=sim_accounts["雪球"]["user"],
                        password=accounts["雪球"]["password"],
                    )
                else:
                    logger.error(
                        f"{self.trade_opts['platform']} 当前还不支持该平台, 请联系微信 Yida_Zhang2"
                    )
            elif self.trade_opts["trade_type"] == "基金":
                from qbot.engine.config import FUNDS_SIM_ACCOUNT

                accounts = file2dict(FUNDS_SIM_ACCOUNT)

            elif self.trade_opts["trade_type"] == "期货":
                from qbot.engine.config import FUTURES_SIM_ACCOUNT

                accounts = file2dict(FUTURES_SIM_ACCOUNT)

                from qbot.engine.trade.engine_apis.futures.futures_engine import (
                    FuturesTradeEngine,
                )

                self.trade_engine = FuturesTradeEngine(
                    accounts[self.trade_opts["platform"]], trade_opts, self.syslog
                )
                self.trade_engine.start_trade()
                if self.trade_opts["platform"] not in accounts:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

            elif trade_opts["trade_type"] == "BTC":
                from qbot.engine.config import BTC_SIM_ACCOUNT

                accounts = file2dict(BTC_SIM_ACCOUNT)

                from qbot.engine.trade.engine_apis.btc.btc_engine import BtcTradeEngine

                self.trade_engine = BtcTradeEngine(
                    accounts[trade_opts["platform"]], trade_opts, self.syslog
                )
                self.trade_engine.start_trade()
                if trade_opts["platform"] not in accounts:
                    logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

            elif self.trade_opts["trade_type"] == "期权":
                from qbot.engine.config import OPTIONS_SIM_ACCOUNT

                accounts = file2dict(OPTIONS_SIM_ACCOUNT)

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
        "class": "虚拟盘",
        "platform": "掘金",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }

    sim_trade_engine = SimTradeEngine(trade_opts=trade_opts, syslog_obj=None)

    # sim_trade_engine.login()
    sim_trade_engine.get_cash()
    sim_trade_engine.get_positions()
    sim_trade_engine.start_trade()
    sim_trade_engine.close()
