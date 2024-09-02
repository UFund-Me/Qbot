from qbot.common.logging.logger import LOGGER as logger


class StockTradeEngine:
    def __init__(self, account, trade_opts: dict, syslog_obj):
        self.account = account
        self.strategy = trade_opts["strategy"]
        self.syslog = syslog_obj
        self.trade_engine = None
        if trade_opts["platform"] == "掘金" and trade_opts["class"] == "虚拟盘":
            self.trade_engine = GmSimTrader(self.account, trade_opts, syslog_obj)
        elif trade_opts["platform"] == "东方财富":
            self.trade_engine = EastmoneyTrader(self.account, trade_opts, syslog_obj)
        else:
            logger.warnning(
                f"{trade_opts['platform']} 还未支持，可联系微信 Yida_Zhang2"
            )

        if not self.trade_engine:
            logger.error("trade engine is null")
            return

    def login(self):
        self.trade_engine.login()

    def get_balance(self):
        self.trade_engine.get_balance()

    def get_positions(self):
        self.trade_engine.get_positions()

    def load_strategy(self):
        pass

    def close(self):
        self.trade_engine.close()

    def start_trade(self):
        self.syslog.re_print("StockTradeEngine start trade ...\n")
        # logger.info(f"start trade, {self.account}")
        self.trade_engine.start_trade()
        # self.trade_engine.close()
        pass


# 掘金
# 本示例运行于python3.6及以上版本
from gmtrade.api import *  # noqa:F403

from qbot.engine.tokens import GMTRADE_ACCOUNT, GMTRADE_TOKEN

# token身份认证，掘金登录后可在仿真交易官网获取
set_token(GMTRADE_TOKEN)

# 示例中为掘金官方仿真服务地址，如接入掘金终端，则填空
set_endpoint("api.myquant.cn:9000")

# 登录账户，账户ID由登录并申请仿真账户后，可复制获取；account_alias为账号别名，选填
a1 = account(account_id=GMTRADE_ACCOUNT, account_alias="")
login(a1)  # 注意，可以输入账户也可以输入账户组成的list


# 回报到达时触发
def on_execution_report(rpt):
    print(f"exec_rpt_count={rpt}")


# 委托状态变化时触发
def on_order_status(order):
    print(f"order_stats_count={order}")


# 交易服务连接成功后触发
def on_trade_data_connected():
    print("已连接交易服务.................")


# 交易服务断开后触发
def on_trade_data_disconnected():
    print("已断开交易服务.................")


# 回报到达时触发
def on_account_status(account_status):
    print(f"on_account_status status={account_status}")


class GmSimTrader:
    def __init__(self, account, trade_opts: dict, syslog_obj):
        self.account = account
        self.trade_opts = trade_opts
        self.syslog = syslog_obj

    def __del__(self):
        self.close()

    def login(self):
        # start函数用于启动回调事件接收，非必要；事件函数为非阻塞函数，如需要同步执行需自行阻塞
        # filename=__file__用于指定当前运行的文件，如需要指定其他文件filename=‘xxx’
        status = start(filename=__file__)
        if status == 0:
            print("连接交易服务成功.................")
        else:
            print("接交易服务失败.................")
            stop()

    def load_strategy(self):
        self.strategy = self.trade_opts["strategy"]
        print("交易策略: ", self.strategy)
        pass

    def get_balance(self):
        # 获取登录账户的资金，如登录多个账户需要指定账户ID
        cash = get_cash()
        print(f"get_cash cash={cash}")
        self.syslog.re_print(f"get_cash cash: \n{cash}")

    def get_positions(self):
        # 获取登录账户的持仓，如登录多个账户需要指定账户ID
        poses = get_positions()
        print(f"get_positions poes=\n{poses}")
        self.syslog.re_print(f"get_positions poes: \n{poses}")

    def start_trade(self):
        self.syslog.re_print("GmSimTrader start trade ...\n")
        logger.info(f"start trade, {self.account}")
        self.load_strategy()

        symbol = self.trade_opts["trade_code"]
        # data = order_volume(symbol=symbol, volume=1000, side=OrderSide_Buy, order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=11)

        # 限价、定量委托买入浦发银行股票
        # data = order_volume(symbol='SHSE.600000', volume=1000, side=OrderSide_Buy, order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=11)
        # 结束交易业务
        pass

    def close(self):
        # 保持进程不退出，否则回调不再生效
        info = input("输入任字符退出")


# 东方财富
class EastmoneyTrader:
    def __init__(self, account, trade_opts: dict, syslog_obj):
        self.account = account
        self.trade_opts = trade_opts
        self.syslog = syslog_obj

    def __del__(self):
        self.close()

    def login(self):
        pass

    def load_strategy(self):
        self.strategy = self.trade_opts["strategy"]
        print("交易策略: ", self.strategy)
        pass

    def get_balance(self):
        # 获取登录账户的资金，如登录多个账户需要指定账户ID
        cash = get_cash()
        print(f"get_cash cash={cash}")

    def get_positions(self):
        # 获取登录账户的持仓，如登录多个账户需要指定账户ID
        poses = get_positions()
        print(f"get_positions poes={poses}")

    def start_trade(self):
        self.syslog.re_print("EastmoneyTrader start trade ...\n")
        # logger.info(f"start trade, {self.account}")
        self.load_strategy()

        symbol = self.trade_opts["trade_code"]
        # data = order_volume(symbol=symbol, volume=1000, side=OrderSide_Buy, order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=11)

        # 限价、定量委托买入浦发银行股票
        # data = order_volume(symbol='SHSE.600000', volume=1000, side=OrderSide_Buy, order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=11)
        # 结束交易业务
        pass

    def close(self):
        # 保持进程不退出，否则回调不再生效
        info = input("输入任字符退出")


if __name__ == "__main__":
    trade_opts = {
        "class": "虚拟盘",
        "platform": "掘金",
        "trade_type": "股票",
        "trade_code": "399006.SZ",
        "strategy": "单因子-相对强弱指数RSI",
    }

    from qbot.common.file_utils import file2dict
    from qbot.engine.config import STOCK_REAL_ACCOUNT, STOCK_SIM_ACCOUNT  # noqa: F401

    # 实盘交易
    real_accounts = file2dict(STOCK_SIM_ACCOUNT)

    stock_engine = StockTradeEngine(
        account=real_accounts[trade_opts["platform"]],
        trade_opts=trade_opts,
        syslog_obj=None,
    )
    stock_engine.login()
    stock_engine.get_balance()
    stock_engine.get_positions()
    stock_engine.start_trade()
    if trade_opts["platform"] not in real_accounts:
        logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")

    # 虚拟交易
    trade_opts["class"] = "虚拟盘"
    trade_opts["platform"] = "东方财富"
    sim_accounts = file2dict(STOCK_SIM_ACCOUNT)

    stock_engine = StockTradeEngine(
        account=sim_accounts[trade_opts["platform"]],
        trade_opts=trade_opts,
        syslog_obj=None,
    )
    stock_engine.login()
    stock_engine.get_balance()
    stock_engine.get_positions()
    stock_engine.start_trade()
    if trade_opts["platform"] not in sim_accounts:
        logger.error("当前还不支持该平台, 请联系微信 Yida_Zhang2")
