#-*- coding=utf-8 -*-
"This is the main demo file"
from ctp.futures import ApiStruct, MdApi
import time
import traceback

class MyMdApi(MdApi):
    def __init__(self, instruments, broker_id,
                 investor_id, passwd, *args,**kwargs):
        self.requestid=0
        self.instruments = instruments
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd

    def OnRspError(self, info, RequestId, IsLast):
        print " Error"
        self.isErrorRspInfo(info)

    def isErrorRspInfo(self, info):
        if info.ErrorID !=0:
            print "ErrorID=", info.ErrorID, ", ErrorMsg=", info.ErrorMsg
        return info.ErrorID !=0

    def OnFrontDisConnected(self, reason):
        print "onFrontDisConnected:", reason

    def OnHeartBeatWarning(self, time):
        print "onHeartBeatWarning", time

    def OnFrontConnected(self):
        print "OnFrontConnected:"
        self.user_login(self.broker_id, self.investor_id, self.passwd)

    def user_login(self, broker_id, investor_id, passwd):
        req = ApiStruct.ReqUserLogin(BrokerID=broker_id, UserID=investor_id, Password=passwd)

        self.requestid+=1
        r=self.ReqUserLogin(req, self.requestid)

    def OnRspUserLogin(self, userlogin, info, rid, is_last):
        print "OnRspUserLogin", is_last, info
        if is_last and not self.isErrorRspInfo(info):
            print "get today's trading day:", repr(self.GetTradingDay())
            self.subscribe_market_data(self.instruments)

    def subscribe_market_data(self, instruments):
        self.SubscribeMarketData(instruments)

    #def OnRspSubMarketData(self, spec_instrument, info, requestid, islast):
    #    print "OnRspSubMarketData"

    #def OnRspUnSubMarketData(self, spec_instrument, info, requestid, islast):
    #    print "OnRspUnSubMarketData"

    def OnRtnDepthMarketData(self, depth_market_data):
        print "OnRtnDepthMarketData"
        print depth_market_data.BidPrice1,depth_market_data.BidVolume1,depth_market_data.AskPrice1,depth_market_data.AskVolume1,depth_market_data.LastPrice,depth_market_data.Volume,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec,depth_market_data.InstrumentID

#inst=[u'al1008', u'al1009', u'al1010', u'al1011', u'al1012', u'al1101', u'al1102', u'al1103', u'al1104', u'al1105', u'al1106', u'al1107', u'au1008', u'au1009', u'au1010', u'au1011', u'au1012', u'au1101', u'au1102', u'au1103', u'au1104', u'au1105', u'au1106', u'au1107', u'cu1008', u'cu1009', u'cu1010', u'cu1011', u'cu1012', u'cu1101', u'cu1102', u'cu1103', u'cu1104', u'cu1105', u'cu1106', u'cu1107', u'fu1009', u'fu1010', u'fu1011', u'fu1012', u'fu1101', u'fu1103', u'fu1104', u'fu1105', u'fu1106', u'fu1107', u'fu1108', u'rb1008', u'rb1009', u'rb1010', u'rb1011', u'rb1012', u'rb1101', u'rb1102', u'rb1103', u'rb1104', u'rb1105', u'rb1106', u'rb1107', u'ru1008', u'ru1009', u'ru1010', u'ru1011', u'ru1101', u'ru1103', u'ru1104', u'ru1105', u'ru1106', u'ru1107', u'wr1008', u'wr1009', u'wr1010', u'wr1011', u'wr1012', u'wr1101', u'wr1102', u'wr1103', u'wr1104', u'wr1105', u'wr1106', u'wr1107', u'zn1008', u'zn1009', u'zn1010', u'zn1011', u'zn1012', u'zn1101', u'zn1102', u'zn1103', u'zn1104', u'zn1105', u'zn1106']
inst = [u'AU0']
def main():
    user = MyMdApi(instruments=inst, 
                             broker_id="000",
                             investor_id="000",
                             passwd="000")
    user.Create("data")
    user.RegisterFront("tcp://asp-sim1-front1.financial-trading-platform.com:41213")
    user.Init()

    while True:
        time.sleep(1)

if __name__=="__main__": main()
