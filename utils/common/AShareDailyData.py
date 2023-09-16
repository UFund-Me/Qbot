'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-12 20:11:54
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-12 20:12:24
FilePath: /Qbot/utils/common/AShareDailyData.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import multiprocessing
import os
import sys
import traceback
from datetime import datetime, timedelta, time
from time import sleep
from typing import List

from tqdm import tqdm
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.database import database_manager, BarOverview
from vnpy.trader.object import HistoryRequest, BarData

from utils import log

sys.path.append(os.getcwd())

from TuShare import tushare_client, to_split_ts_codes, TS_DATE_FORMATE


class AShareDailyDataManager:

    def __init__(self):
        """"""
        self.tushare_client = tushare_client
        self.symbols = None
        self.trade_cal = None
        self.bar_overviews: List[BarOverview] = None
        self.init()

    def init(self):
        """"""
        self.tushare_client.init()
        self.symbols = self.tushare_client.symbols
        self.trade_cal = self.tushare_client.trade_cal
        self.bar_overviews = database_manager.get_bar_overview()

    def download_all(self):
        """
        使用tushare下载A股股票全市场日线数据
        :return:
        """
        log.info("开始下载A股股票全市场日线数据")
        if self.symbols is not None:
            with tqdm(total=len(self.symbols)) as pbar:
                for tscode, list_date in zip(self.symbols['ts_code'], self.symbols['list_date']):
                    symbol, exchange = to_split_ts_codes(tscode)

                    pbar.set_description_str("下载A股日线数据股票代码:" + tscode)
                    start_date = datetime.strptime(list_date, TS_DATE_FORMATE)
                    req = HistoryRequest(symbol=symbol,
                                         exchange=exchange,
                                         start=start_date,
                                         end=datetime.now(),
                                         interval=Interval.DAILY)
                    bardata = self.tushare_client.query_history(req=req)

                    if bardata:
                        try:
                            database_manager.save_bar_data(bardata)
                        except Exception as ex:
                            log.error(tscode + "数据存入数据库异常")
                            log.error(ex)
                            traceback.print_exc()

                    pbar.update(1)
                    log.info(pbar.desc)

        log.info("A股股票全市场日线数据下载完毕")

    def get_newest_bar_data(self, symbol: str, exchange: Exchange, interval: Interval) -> BarData or None:
        """"""
        for overview in self.bar_overviews:
            if exchange == overview.exchange and interval == overview.interval and symbol == overview.symbol:
                bars = database_manager.load_bar_data(symbol=symbol, exchange=exchange, interval=interval,
                                                      start=overview.end, end=overview.end)
                return bars[0] if bars is not None else None
        return None

    def update_newest(self):
        """
        使用tushare更新本地数据库中的最新数据，默认本地数据库中原最新的数据之前的数据都是完备的
        :return:
        """
        log.info("开始更新最新的A股股票全市场日线数据")
        if self.symbols is not None:
            with tqdm(total=len(self.symbols)) as pbar:
                for tscode, list_date in zip(self.symbols['ts_code'], self.symbols['list_date']):
                    symbol, exchange = to_split_ts_codes(tscode)

                    newest_local_bar = self.get_newest_bar_data(symbol=symbol,
                                                                exchange=exchange,
                                                                interval=Interval.DAILY)
                    if newest_local_bar is not None:
                        pbar.set_description_str("正在处理股票代码：" + tscode + "本地最新数据：" +
                                                 newest_local_bar.datetime.strftime(TS_DATE_FORMATE))
                        start_date = newest_local_bar.datetime + timedelta(days=1)
                    else:
                        pbar.set_description_str("正在处理股票代码：" + tscode + "无本地数据")
                        start_date = datetime.strptime(list_date, TS_DATE_FORMATE)
                    req = HistoryRequest(symbol=symbol,
                                         exchange=exchange,
                                         start=start_date,
                                         end=datetime.now(),
                                         interval=Interval.DAILY)
                    bardata = self.tushare_client.query_history(req=req)
                    if bardata:
                        try:
                            database_manager.save_bar_data(bardata)
                        except Exception as ex:
                            log.error(tscode + "数据存入数据库异常")
                            log.error(ex)
                            traceback.print_exc()

                    pbar.update(1)
                    log.info(pbar.desc)

        log.info("A股股票全市场日线数据更新完毕")

    def check_update_all(self):
        """
        这个方法太慢了，不建议调用。
        这个方法用于本地数据库已经建立，但可能有部分数据缺失时使用
        使用tushare检查更新所有的A股股票全市场日线数据
        检查哪一个交易日的数据是缺失的，补全它
        检查上市后是否每个交易日都有数据，若存在某一交易日无数据，尝试从tushare查询该日数据，若仍无，则说明当天停盘
        :return:
        """
        log.info("开始检查更新所有的A股股票全市场日线数据")

        if self.symbols is not None:
            with tqdm(total=len(self.symbols)) as pbar:
                for tscode, list_date in zip(self.symbols['ts_code'], self.symbols['list_date']):
                    pbar.set_description_str("正在检查A股日线数据，股票代码:" + tscode)

                    symbol, exchange = to_split_ts_codes(tscode)

                    local_bar = database_manager.load_bar_data(symbol=symbol,
                                                               exchange=exchange,
                                                               interval=Interval.DAILY,
                                                               start=datetime.strptime(list_date, TS_DATE_FORMATE),
                                                               end=datetime.now())
                    local_bar_dates = [bar.datetime.strftime(TS_DATE_FORMATE) for bar in local_bar]

                    index = (self.trade_cal[exchange.value][(self.trade_cal[exchange.value].cal_date == list_date)])
                    trade_cal = self.trade_cal[exchange.value].iloc[index.index[0]:]
                    for trade_date in trade_cal['cal_date']:
                        if trade_date not in local_bar_dates:
                            req = HistoryRequest(symbol=symbol,
                                                 exchange=exchange,
                                                 start=datetime.strptime(trade_date, TS_DATE_FORMATE),
                                                 end=datetime.strptime(trade_date, TS_DATE_FORMATE),
                                                 interval=Interval.DAILY)
                            bardata = self.tushare_client.query_history(req=req)
                            if bardata:
                                log.info(tscode + "本地数据库缺失：" + trade_date)
                                try:
                                    database_manager.save_bar_data(bardata)
                                except Exception as ex:
                                    log.error(tscode + "数据存入数据库异常")
                                    log.error(ex)
                                    traceback.print_exc()
                    pbar.update(1)
                    log.info(pbar.desc)

        log.info("A股股票全市场日线数据检查更新完毕")


a_share_daily_data_manager = AShareDailyDataManager()


def auto_update(start_time: time = time(18, 0)):
    """
    每日盘后自动更新最新日线数据到本地数据库
    """
    log.info("启动A股股票全市场日线数据定时更新")
    run_parent(start_time=start_time)


def run_parent(start_time: time = time(18, 0)):
    """
    运行父进程，定时启动子进程下载任务
    :return:
    """
    log.info("启动A股股票全市场日线数据定时更新父进程")

    # 每天晚上18：30从tushare更新当时K线数据
    UPDATE_TIME = start_time

    child_process = None

    while True:
        current_time = datetime.now().time()

        if current_time.hour == UPDATE_TIME.hour and current_time.minute == UPDATE_TIME.minute and child_process is None:
            log.info("启动日线数据更新子进程")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            log.info("日线数据更新子进程启动成功")

        if (not (current_time.hour == UPDATE_TIME.hour and current_time.minute == UPDATE_TIME.minute)) \
                and child_process is not None:
            child_process.join()
            child_process = None
            log.info("数据更新子进程关闭成功")
            log.info("进入A股股票全市场日线数据定时更新父进程")

        sleep(10)


def run_child():
    """
    子线程下载数据
    :return:
    """
    log.info("启动A股股票全市场日线数据定时更新子进程")

    try:
        a_share_daily_data_manager.update_newest()
    except Exception:
        log.info("子进程异常")
        traceback.print_exc()


if __name__ == '__main__':
    log.info("自动更新A股股票全市场日线数据")

    # a_share_daily_data_manager.download_all()
    # a_share_daily_data_manager.update_newest()
    # a_share_daily_data_manager.check_update_all()
    auto_update(start_time=time(21, 47))
