from qbot.common.logging.logger import LOGGER as logger
from qbot.engine.trade.trade_real import RealTradeEngine
from qbot.engine.trade.trade_sim import SimTradeEngine


class TradeEngine:
    def __init__(self, trade_opts: dict, syslog_obj):

        if syslog_obj:
            self.syslog = syslog_obj
        else:
            logger.error("syslog_obj is null.")
            return

        self.syslog.re_print("TradeEngine start init ...\n")

        if trade_opts:
            logger.info(f"trade_opts: {trade_opts}")
        else:
            logger.error("trade_opts is empty.")
            return

        self.trade_opts = trade_opts
        if self.trade_opts["class"] == "虚拟盘":
            self.TradeEngine = SimTradeEngine(self.trade_opts, syslog_obj=self.syslog)
        elif self.trade_opts["class"] == "实盘":
            self.TradeEngine = RealTradeEngine(self.trade_opts, syslog_obj=self.syslog)
        else:
            logger.error(
                f"parameter is invalid, trade class is {self.trade_opts['class']}"
            )

    def login(self):
        logger.info(f"{self.trade_opts['platform']} login ....")
        self.syslog.re_print(f"{self.trade_opts['platform']} login ....\n")
        self.TradeEngine.login()
        pass

    def get_cash(self):
        self.TradeEngine.get_cash()

    def get_positions(self):
        self.TradeEngine.get_positions()

    def load_strategy(self):
        pass

    def start_trade(self):
        logger.info("start_trade ....")
        self.TradeEngine.start_trade()
        pass

    def close(self):
        logger.info("close engine ....")
        self.TradeEngine.close()
        pass


if __name__ == "__main__":
    trade_opts = {
        "class": "虚拟盘",
        "platform": "掘金",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }

    trade_engine = TradeEngine(trade_opts, syslog_obj=None)
    trade_engine.login()
    trade_engine.get_cash()
    trade_engine.get_positions()
    trade_engine.start_trade()
    trade_engine.close()
