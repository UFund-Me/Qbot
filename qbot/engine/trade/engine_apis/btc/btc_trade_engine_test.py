from qbot.common.logging.logger import LOGGER as logger
from qbot.engine.trade.engine_apis.btc.btc_trade_engine import (
    CcxtTradeEngine,
    OkxTradeEngine,
)


# 获取 5 分钟的 K 线数据
def fetch_ohlcv(exchange, symbol, timeframe="5m", limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df


# 计算 MACD 指标
def calculate_macd(df):
    import talib as ta

    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()


# 检查交易信号
def check_trade_signals(df):
    last_row = df.iloc[-1]
    previous_row = df.iloc[-2]

    # 买入条件：MACD 越过零线
    if previous_row["macd"] < 0 and last_row["macd"] > 0:
        return "buy"

    # 卖出条件：MACD 低于零线
    if previous_row["macd"] > 0 and last_row["macd"] < 0:
        return "sell"

    return "hold"


# ref: https://mp.weixin.qq.com/s?__biz=MzIzMjE3NTAxNw==&mid=2649269697&idx=1&sn=f562d5de13bd125237b888ff89f25112&chksm=f084e107c7f36811d64e7e51c523ea8a54085937c28949ddc930f4d0e6506d6ccf5f5e1dc59a&cur_album_id=3563545010618269709&scene=189#wechat_redirect
def cctx_main(account, trade_opts, symbol="BTC/USDT"):
    if "/" not in symbol:
        symbol = symbol[:3] + "/" + symbol[-4:]

    ccxt_engine = CcxtTradeEngine(account, trade_opts, syslog_obj=None)

    print(ccxt_engine.exchange)

    entry_price = None
    while True:
        df = fetch_ohlcv(ccxt_engine.exchange, symbol)
        calculate_macd(df)
        calculate_ema(df)
        calculate_kdj(df)
        signal = check_trade_signals(df)
        ccxt_engine.execute_trade(signal, symbol, entry_price=entry_price)
        time.sleep(300)  # 每5分钟运行一次


def okx_main(account, trade_opts, symbol="BTC/USDT"):
    trade_engine = OkxTradeEngine(account, trade_opts)

    trade_engine.get_ticker(symbol)
    trade_engine.get_balance()
    # trade_engine.get_positions()
    # trade_engine.start_trade()


def main():
    from qbot.common.file_utils import file2dict
    from qbot.engine.config import BTC_REAL_ACCOUNT, BTC_SIM_ACCOUNT

    trade_opts = {
        "class": "虚拟盘",
        "platform": "欧易OKX",
        "trade_type": "BTC",
        "trade_code": "ETHUSDT",
        "strategy": "单因子-相对强弱指数RSI",
    }

    # 虚拟盘交易
    sim_accounts = file2dict(BTC_SIM_ACCOUNT)

    # cctx_main(account=sim_accounts[trade_opts["platform"]], trade_opts=trade_opts, symbol='BTC/USDT')

    # trade_opts["class"] = "虚拟盘"
    # trade_opts["platform"] = "币安Binance"
    logger.info(sim_accounts[trade_opts["platform"]])
    okx_main(
        account=sim_accounts[trade_opts["platform"]],
        trade_opts=trade_opts,
        symbol="BTC/USDT",
    )

    # 实盘交易
    real_accounts = file2dict(BTC_REAL_ACCOUNT)
    trade_opts["class"] = "实盘"
    trade_opts["platform"] = "币安Binance"
    logger.info(real_accounts[trade_opts["platform"]])
    okx_main(
        account=real_accounts[trade_opts["platform"]],
        trade_opts=trade_opts,
        symbol="BTC/USDT",
    )


if __name__ == "__main__":
    main()
