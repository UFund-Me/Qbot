import requests
import tushare as ts
from tushare.pro import client
from pytz import timezone
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime, timedelta
import time
import traceback

from vnpy.trader.object import HistoryRequest, BarData
from vnpy.trader.constant import Exchange, Interval

from utils import log

CHINA_TZ = timezone("Asia/Shanghai")

tushare_token: str = ""

MAX_QUERY_SIZE: int = 5000
TS_DATE_FORMATE: str = '%Y%m%d'
MAX_QUERY_TIMES: int = 500

EXCHANGE_TS2VT: Dict[str, Exchange] = {
    'SH': Exchange.SSE,
    'SZ': Exchange.SZSE
}

EXCHANGE_VT2TS: Dict[Exchange, str] = {v: k for k, v in EXCHANGE_TS2VT.items()}


def to_ts_symbol(symbol: str, exchange: Exchange):
    """
    转换合约代码为tushare查询代码
    """
    if exchange == Exchange.SSE:
        tcode = f'{symbol}' + '.' + f'{EXCHANGE_VT2TS[exchange]}'
    elif exchange == Exchange.SZSE:
        tcode = f'{symbol}' + '.' + f'{EXCHANGE_VT2TS[exchange]}'
    else:
        print("目前只研究深圳证券交易所和上海证券交易所A股股票！")
        raise TypeError("目前只研究深圳证券交易所和上海证券交易所A股股票！")
    return tcode


def to_split_ts_codes(tscode: str):
    symbol, exchange_ts = tscode.split('.')
    exchange = EXCHANGE_TS2VT[exchange_ts]
    return symbol, exchange


class TuShareClient:
    """
    从TuShare中查询历史数据的Client
    tushare日线数据说明：交易日每天15点~16点之间更新数据，daily接口是未复权行情，停牌期间不提供数据。
    tushare调取说明：基础积分每分钟内最多调取500次，每次5000条数据
    """

    def __init__(self):
        """"""

        self.pro: client.DataApi = None

        self.inited: bool = False

        # 获得所有股票代码
        self.symbols: pd.DataFrame = None

        # 获得交易日历
        self.trade_cal: Dict[str, pd.DataFrame] = None

    def init(self, token: str = "") -> bool:
        """"""
        if self.inited:
            return True

        if token:
            ts.set_token(tushare_token)
        else:
            ts.set_token(tushare_token)

        try:
            self.pro = ts.pro_api()
            self.stock_list()
            self.trade_day_list()
        except (BaseException, "tushare连接失败"):
            return False

        self.inited = True
        return True

    def query_history(self, req: HistoryRequest) -> Optional[List[BarData]]:
        """
        从tushare里查询历史数据
        :param req:查询请求
        :return: Optional[List[BarData]]
        """
        if self.symbols is None:
            return None

        symbol = req.symbol
        exchange = req.exchange
        interval = req.interval
        start = req.start.strftime(TS_DATE_FORMATE)
        end = req.end.strftime(TS_DATE_FORMATE)

        if interval is not Interval.DAILY:
            return None
        if exchange not in [Exchange.SSE, Exchange.SZSE]:
            return None

        tscode = to_ts_symbol(symbol, exchange)

        # 修改查询数据逻辑，在每次5000条数据的限制下，很可能一次无法读取完
        cnt = 0
        df: pd.DataFrame = None
        while datetime.strptime(start, TS_DATE_FORMATE) <= datetime.strptime(end, TS_DATE_FORMATE):
            # 保证每次查询最多5000天数据
            start_date = datetime.strptime(start, TS_DATE_FORMATE)
            simulate_end_date = min(datetime.strptime(end, TS_DATE_FORMATE),
                                    start_date + timedelta(days=MAX_QUERY_SIZE))
            simulate_end = simulate_end_date.strftime(TS_DATE_FORMATE)

            # 保证每次调用时间在60/500=0.12秒内，以保证每分钟调用次数少于500次
            # begin_time = time.time()
            tushare_df = None
            while True:
                try:
                    tushare_df = self.pro.query('daily', ts_code=tscode, start_date=start, end_date=simulate_end)
                except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                    log.error(e)
                    # traceback.print_exc()
                    # ('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
                    if '10054' in str(e):
                        sleep_time = 60.0
                        log.info("请求过于频繁，sleep：" + str(sleep_time) + "s")
                        time.sleep(sleep_time)
                        log.info("继续发送请求：" + tscode)
                        continue  # 继续发请求
                    else:
                        raise Exception(e)  # 其他异常，抛出来
                break
            if tushare_df is not None:
                if df is None:
                    df = tushare_df
                else:
                    df = pd.concat([df, tushare_df], ignore_index=True)
            # end_time = time.time()
            # delta = round(end_time - begin_time, 3)
            # if delta < 60 / MAX_QUERY_TIMES:
            sleep_time = 0.50
            log.info("sleep：" + str(sleep_time) + "s")
            time.sleep(sleep_time)

            cnt += 1
            start = (simulate_end_date + timedelta(days=1)).strftime(TS_DATE_FORMATE)

        data: List[BarData] = []

        if df is not None:
            for ix, row in df.iterrows():
                date = datetime.strptime(row.trade_date, '%Y%m%d')
                date = CHINA_TZ.localize(date)

                if pd.isnull(row['open']):
                    log.info(symbol + '.' + EXCHANGE_VT2TS[exchange] + row['trade_date'] + "open_price为None")
                elif pd.isnull(row['high']):
                    log.info(symbol + '.' + EXCHANGE_VT2TS[exchange] + row['trade_date'] + "high_price为None")
                elif pd.isnull(row['low']):
                    log.info(symbol + '.' + EXCHANGE_VT2TS[exchange] + row['trade_date'] + "low_price为None")
                elif pd.isnull(row['close']):
                    log.info(symbol + '.' + EXCHANGE_VT2TS[exchange] + row['trade_date'] + "close_price为None")
                elif pd.isnull(row['amount']):
                    log.info(symbol + '.' + EXCHANGE_VT2TS[exchange] + row['trade_date'] + "volume为None")

                row.fillna(0)
                bar = BarData(
                    symbol=symbol,
                    exchange=exchange,
                    interval=interval,
                    datetime=date,
                    open_price=row['open'],
                    high_price=row['high'],
                    low_price=row['low'],
                    close_price=row['close'],
                    volume=row['amount'],
                    gateway_name='tushare'
                )

                data.append(bar)
        return data

    def stock_list(self):
        """
        调用tushare stock_basic 接口
        获得上海证券交易所和深圳证券交易所所有股票代码
        获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
        :return:
        """
        if self.symbols is None:
            symbols_sse = self.pro.query('stock_basic', exchange=Exchange.SSE.value, fields='ts_code,symbol,name,'
                                                                                            'fullname,enname,market,'
                                                                                            'list_status,list_date,'
                                                                                            'delist_date,is_hs')
            symbols_szse = self.pro.query('stock_basic', exchange=Exchange.SZSE.value, fields='ts_code,symbol,name,'
                                                                                              'fullname,enname,market,'
                                                                                              'list_status,list_date,'
                                                                                              'delist_date,is_hs')
            self.symbols = pd.concat([symbols_sse, symbols_szse], axis=0, ignore_index=True)

    def trade_day_list(self):
        """
        查询交易日历
        :return:
        """
        if self.trade_cal is None:
            self.trade_cal = dict()
            self.trade_cal[Exchange.SSE.value] = self.pro.query('trade_cal', exchange=Exchange.SSE.value, is_open='1')
            self.trade_cal[Exchange.SZSE.value] = self.pro.query('trade_cal', exchange=Exchange.SZSE.value, is_open='1')


tushare_client = TuShareClient()

if __name__ == "__main__":
    print("测试TuShare数据接口")
    # tushare_client = TuShareClient()
    tushare_client.init()
    # print(tushare_client.symbols)
    # print(tushare_client.trade_cal)

    req = HistoryRequest(symbol='600600', exchange=Exchange.SSE,
                         start=datetime(year=1999, month=11, day=10), end=datetime.now(), interval=Interval.DAILY)

    ts_data = tushare_client.query_history(req)
    print(len(ts_data))
