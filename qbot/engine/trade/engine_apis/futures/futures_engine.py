from qbot.common.logging.logger import LOGGER as logger

class FuturesTradeEngine:
    
    def __init__(self, account, trade_opts: dict, syslog_obj):
        self.account = account
        self.strategy = trade_opts["strategy"]
        self.syslog = syslog_obj
        self.trade_engine = None
    
    def start_trade(self):
        self.syslog.re_print("FuturesTradeEngine start trade ...\n")
        pass


if __name__ == "__main__":
    trade_opts = {
        "class": "实盘",
        "platform": "东方财富",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }
    futures_engine = FuturesTradeEngine(trade_opts["platform"], trade_opts, self.syslog)
    futures_engine.start_trade()
    if trade_opts["platform"] not in accounts:
        logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")