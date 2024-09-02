# coding=utf-8
import datetime


class TickBar(object):
    def __init__(self, day, data, last_volume):
        """
        pData的格式转换和整理, 交易数据都转换为整数，tick的后四个字段在模拟行情中经常出错
        :param data: ApiStruct.DepthMarketData
        :return:
        """
        self.instrument = data.InstrumentID
        self.bid_price = data.BidPrice1
        self.bid_volume = data.BidVolume1
        self.ask_price = data.AskPrice1
        self.ask_volume = data.AskVolume1
        self.holding = data.OpenInterest
        self.up_limit_price = data.UpperLimitPrice
        self.down_limit_price = data.LowerLimitPrice
        self.volume = data.Volume - last_volume
        self.price = data.LastPrice
        self.day_high = data.HighestPrice
        self.day_low = data.LowestPrice
        self.open = data.OpenPrice
        self.pre_close = data.PreClosePrice
        self.dateTime = datetime.datetime.strptime(day+data.UpdateTime, "%Y%m%d%H:%M:%S")
        self.dateTime = self.dateTime + datetime.timedelta(microseconds=datetime.datetime.now().microsecond)
