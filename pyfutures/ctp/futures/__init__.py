# -*- coding: utf-8 -*-

from __future__ import absolute_import as _init

__author__ = 'lovelylain'
__version__ = '0.2.1'

__all__ = ['ApiStruct', 'MdApi', 'TraderApi']

if 0: from . import ApiStruct

class MdApi(object):
    def Create(self, pszFlowPath='', bIsUsingUdp=False, bIsMulticast=False):
        """创建MdApi
        @param pszFlowPath 存贮订阅信息文件的目录，默认为当前目录
        @return 创建出的UserApi
        modify for udp marketdata
        """

    def Release(self):
        """删除接口对象本身
        @remark 不再使用本接口对象时,调用该函数删除接口对象
        """

    def Init(self):
        """初始化
        @remark 初始化运行环境,只有调用后,接口才开始工作
        """

    def Join(self):
        """等待接口线程结束运行
        @return 线程退出代码
        """
        return 0

    def GetTradingDay(self):
        """获取当前交易日
        @retrun 获取到的交易日
        @remark 只有登录成功后,才能得到正确的交易日
        """
        return ''

    def RegisterFront(self, pszFrontAddress):
        """注册前置机网络地址
        @param pszFrontAddress：前置机网络地址。
        @remark 网络地址的格式为：“protocol:
        ipaddress:port”，如：”tcp:
        127.0.0.1:17001”。
        @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”17001”代表服务器端口号。
        """

    def RegisterNameServer(self, pszNsAddress):
        """注册名字服务器网络地址
        @param pszNsAddress：名字服务器网络地址。
        @remark 网络地址的格式为：“protocol:
        ipaddress:port”，如：”tcp:
        127.0.0.1:12001”。
        @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”12001”代表服务器端口号。
        @remark RegisterNameServer优先于RegisterFront
        """

    def RegisterFensUserInfo(self, pFensUserInfo):
        """注册名字服务器用户信息
        @param pFensUserInfo：用户信息。
        """

    def SubscribeMarketData(self, pInstrumentIDs):
        """订阅行情。
        @param pInstrumentIDs 合约ID列表
        @remark
        """
        return 0

    def UnSubscribeMarketData(self, pInstrumentIDs):
        """退订行情。
        @param pInstrumentIDs 合约ID列表
        @remark
        """
        return 0

    def ReqUserLogin(self, pReqUserLogin, nRequestID):
        """用户登录请求"""
        return 0

    def ReqUserLogout(self, pUserLogout, nRequestID):
        """登出请求"""
        return 0

    def OnFrontConnected(self):
        """当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。"""

    def OnFrontDisconnected(self, nReason):
        """当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
        @param nReason 错误原因
                0x1001 网络读失败
                0x1002 网络写失败
                0x2001 接收心跳超时
                0x2002 发送心跳失败
                0x2003 收到错误报文
        """

    def OnHeartBeatWarning(self, nTimeLapse):
        """心跳超时警告。当长时间未收到报文时，该方法被调用。
        @param nTimeLapse 距离上次接收报文的时间
        """

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        """登录请求响应"""

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        """登出请求响应"""

    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        """错误应答"""

    def OnRspSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        """订阅行情应答"""

    def OnRspUnSubMarketData(self, pSpecificInstrument, pRspInfo, nRequestID, bIsLast):
        """取消订阅行情应答"""

    def OnRtnDepthMarketData(self, pDepthMarketData):
        """深度行情通知"""


class TraderApi(object):
    def Create(self, pszFlowPath=''):
        """创建TraderApi
        @param pszFlowPath 存贮订阅信息文件的目录，默认为当前目录
        @return 创建出的UserApi
        """

    def Release(self):
        """删除接口对象本身
        @remark 不再使用本接口对象时,调用该函数删除接口对象
        """

    def Init(self):
        """初始化
        @remark 初始化运行环境,只有调用后,接口才开始工作
        """

    def Join(self):
        """等待接口线程结束运行
        @return 线程退出代码
        """
        return 0

    def GetTradingDay(self):
        """获取当前交易日
        @retrun 获取到的交易日
        @remark 只有登录成功后,才能得到正确的交易日
        """
        return ''

    def RegisterFront(self, pszFrontAddress):
        """注册前置机网络地址
        @param pszFrontAddress：前置机网络地址。
        @remark 网络地址的格式为：“protocol:
        ipaddress:port”，如：”tcp:
        127.0.0.1:17001”。
        @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”17001”代表服务器端口号。
        """

    def RegisterNameServer(self, pszNsAddress):
        """注册名字服务器网络地址
        @param pszNsAddress：名字服务器网络地址。
        @remark 网络地址的格式为：“protocol:
        ipaddress:port”，如：”tcp:
        127.0.0.1:12001”。
        @remark “tcp”代表传输协议，“127.0.0.1”代表服务器地址。”12001”代表服务器端口号。
        @remark RegisterNameServer优先于RegisterFront
        """

    def RegisterFensUserInfo(self, pFensUserInfo):
        """注册名字服务器用户信息
        @param pFensUserInfo：用户信息。
        """

    def SubscribePrivateTopic(self, nResumeType):
        """订阅私有流。
        @param nResumeType 私有流重传方式
                THOST_TERT_RESTART:从本交易日开始重传
                THOST_TERT_RESUME:从上次收到的续传
                THOST_TERT_QUICK:只传送登录后私有流的内容
        @remark 该方法要在Init方法前调用。若不调用则不会收到私有流的数据。
        """

    def SubscribePublicTopic(self, nResumeType):
        """订阅公共流。
        @param nResumeType 公共流重传方式
                THOST_TERT_RESTART:从本交易日开始重传
                THOST_TERT_RESUME:从上次收到的续传
                THOST_TERT_QUICK:只传送登录后公共流的内容
        @remark 该方法要在Init方法前调用。若不调用则不会收到公共流的数据。
        """

    def ReqAuthenticate(self, pReqAuthenticate, nRequestID):
        """客户端认证请求"""
        return 0

    def ReqUserLogin(self, pReqUserLogin, nRequestID):
        """用户登录请求"""
        return 0

    def ReqUserLogout(self, pUserLogout, nRequestID):
        """登出请求"""
        return 0

    def ReqUserPasswordUpdate(self, pUserPasswordUpdate, nRequestID):
        """用户口令更新请求"""
        return 0

    def ReqTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate, nRequestID):
        """资金账户口令更新请求"""
        return 0

    def ReqOrderInsert(self, pInputOrder, nRequestID):
        """报单录入请求"""
        return 0

    def ReqParkedOrderInsert(self, pParkedOrder, nRequestID):
        """预埋单录入请求"""
        return 0

    def ReqParkedOrderAction(self, pParkedOrderAction, nRequestID):
        """预埋撤单录入请求"""
        return 0

    def ReqOrderAction(self, pInputOrderAction, nRequestID):
        """报单操作请求"""
        return 0

    def ReqQueryMaxOrderVolume(self, pQueryMaxOrderVolume, nRequestID):
        """查询最大报单数量请求"""
        return 0

    def ReqSettlementInfoConfirm(self, pSettlementInfoConfirm, nRequestID):
        """投资者结算结果确认"""
        return 0

    def ReqRemoveParkedOrder(self, pRemoveParkedOrder, nRequestID):
        """请求删除预埋单"""
        return 0

    def ReqRemoveParkedOrderAction(self, pRemoveParkedOrderAction, nRequestID):
        """请求删除预埋撤单"""
        return 0

    def ReqQryOrder(self, pQryOrder, nRequestID):
        """请求查询报单"""
        return 0

    def ReqQryTrade(self, pQryTrade, nRequestID):
        """请求查询成交"""
        return 0

    def ReqQryInvestorPosition(self, pQryInvestorPosition, nRequestID):
        """请求查询投资者持仓"""
        return 0

    def ReqQryTradingAccount(self, pQryTradingAccount, nRequestID):
        """请求查询资金账户"""
        return 0

    def ReqQryInvestor(self, pQryInvestor, nRequestID):
        """请求查询投资者"""
        return 0

    def ReqQryTradingCode(self, pQryTradingCode, nRequestID):
        """请求查询交易编码"""
        return 0

    def ReqQryInstrumentMarginRate(self, pQryInstrumentMarginRate, nRequestID):
        """请求查询合约保证金率"""
        return 0

    def ReqQryInstrumentCommissionRate(self, pQryInstrumentCommissionRate, nRequestID):
        """请求查询合约手续费率"""
        return 0

    def ReqQryExchange(self, pQryExchange, nRequestID):
        """请求查询交易所"""
        return 0

    def ReqQryInstrument(self, pQryInstrument, nRequestID):
        """请求查询合约"""
        return 0

    def ReqQryDepthMarketData(self, pQryDepthMarketData, nRequestID):
        """请求查询行情"""
        return 0

    def ReqQrySettlementInfo(self, pQrySettlementInfo, nRequestID):
        """请求查询投资者结算结果"""
        return 0

    def ReqQryTransferBank(self, pQryTransferBank, nRequestID):
        """请求查询转帐银行"""
        return 0

    def ReqQryInvestorPositionDetail(self, pQryInvestorPositionDetail, nRequestID):
        """请求查询投资者持仓明细"""
        return 0

    def ReqQryNotice(self, pQryNotice, nRequestID):
        """请求查询客户通知"""
        return 0

    def ReqQrySettlementInfoConfirm(self, pQrySettlementInfoConfirm, nRequestID):
        """请求查询结算信息确认"""
        return 0

    def ReqQryInvestorPositionCombineDetail(self, pQryInvestorPositionCombineDetail, nRequestID):
        """请求查询投资者持仓明细"""
        return 0

    def ReqQryCFMMCTradingAccountKey(self, pQryCFMMCTradingAccountKey, nRequestID):
        """请求查询保证金监管系统经纪公司资金账户密钥"""
        return 0

    def ReqQryEWarrantOffset(self, pQryEWarrantOffset, nRequestID):
        """请求查询仓单折抵信息"""
        return 0

    def ReqQryTransferSerial(self, pQryTransferSerial, nRequestID):
        """请求查询转帐流水"""
        return 0

    def ReqQryAccountregister(self, pQryAccountregister, nRequestID):
        """请求查询银期签约关系"""
        return 0

    def ReqQryContractBank(self, pQryContractBank, nRequestID):
        """请求查询签约银行"""
        return 0

    def ReqQryParkedOrder(self, pQryParkedOrder, nRequestID):
        """请求查询预埋单"""
        return 0

    def ReqQryParkedOrderAction(self, pQryParkedOrderAction, nRequestID):
        """请求查询预埋撤单"""
        return 0

    def ReqQryTradingNotice(self, pQryTradingNotice, nRequestID):
        """请求查询交易通知"""
        return 0

    def ReqQryBrokerTradingParams(self, pQryBrokerTradingParams, nRequestID):
        """请求查询经纪公司交易参数"""
        return 0

    def ReqQryBrokerTradingAlgos(self, pQryBrokerTradingAlgos, nRequestID):
        """请求查询经纪公司交易算法"""
        return 0

    def ReqFromBankToFutureByFuture(self, pReqTransfer, nRequestID):
        """期货发起银行资金转期货请求"""
        return 0

    def ReqFromFutureToBankByFuture(self, pReqTransfer, nRequestID):
        """期货发起期货资金转银行请求"""
        return 0

    def ReqQueryBankAccountMoneyByFuture(self, pReqQueryAccount, nRequestID):
        """期货发起查询银行余额请求"""
        return 0

    def OnFrontConnected(self):
        """当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。"""

    def OnFrontDisconnected(self, nReason):
        """当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
        @param nReason 错误原因
                0x1001 网络读失败
                0x1002 网络写失败
                0x2001 接收心跳超时
                0x2002 发送心跳失败
                0x2003 收到错误报文
        """

    def OnHeartBeatWarning(self, nTimeLapse):
        """心跳超时警告。当长时间未收到报文时，该方法被调用。
        @param nTimeLapse 距离上次接收报文的时间
        """

    def OnRspAuthenticate(self, pRspAuthenticate, pRspInfo, nRequestID, bIsLast):
        """客户端认证响应"""

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        """登录请求响应"""

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        """登出请求响应"""

    def OnRspUserPasswordUpdate(self, pUserPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        """用户口令更新请求响应"""

    def OnRspTradingAccountPasswordUpdate(self, pTradingAccountPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        """资金账户口令更新请求响应"""

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        """报单录入请求响应"""

    def OnRspParkedOrderInsert(self, pParkedOrder, pRspInfo, nRequestID, bIsLast):
        """预埋单录入请求响应"""

    def OnRspParkedOrderAction(self, pParkedOrderAction, pRspInfo, nRequestID, bIsLast):
        """预埋撤单录入请求响应"""

    def OnRspOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
        """报单操作请求响应"""

    def OnRspQueryMaxOrderVolume(self, pQueryMaxOrderVolume, pRspInfo, nRequestID, bIsLast):
        """查询最大报单数量响应"""

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        """投资者结算结果确认响应"""

    def OnRspRemoveParkedOrder(self, pRemoveParkedOrder, pRspInfo, nRequestID, bIsLast):
        """删除预埋单响应"""

    def OnRspRemoveParkedOrderAction(self, pRemoveParkedOrderAction, pRspInfo, nRequestID, bIsLast):
        """删除预埋撤单响应"""

    def OnRspQryOrder(self, pOrder, pRspInfo, nRequestID, bIsLast):
        """请求查询报单响应"""

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        """请求查询成交响应"""

    def OnRspQryInvestorPosition(self, pInvestorPosition, pRspInfo, nRequestID, bIsLast):
        """请求查询投资者持仓响应"""

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        """请求查询资金账户响应"""

    def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
        """请求查询投资者响应"""

    def OnRspQryTradingCode(self, pTradingCode, pRspInfo, nRequestID, bIsLast):
        """请求查询交易编码响应"""

    def OnRspQryInstrumentMarginRate(self, pInstrumentMarginRate, pRspInfo, nRequestID, bIsLast):
        """请求查询合约保证金率响应"""

    def OnRspQryInstrumentCommissionRate(self, pInstrumentCommissionRate, pRspInfo, nRequestID, bIsLast):
        """请求查询合约手续费率响应"""

    def OnRspQryExchange(self, pExchange, pRspInfo, nRequestID, bIsLast):
        """请求查询交易所响应"""

    def OnRspQryInstrument(self, pInstrument, pRspInfo, nRequestID, bIsLast):
        """请求查询合约响应"""

    def OnRspQryDepthMarketData(self, pDepthMarketData, pRspInfo, nRequestID, bIsLast):
        """请求查询行情响应"""

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequestID, bIsLast):
        """请求查询投资者结算结果响应"""

    def OnRspQryTransferBank(self, pTransferBank, pRspInfo, nRequestID, bIsLast):
        """请求查询转帐银行响应"""

    def OnRspQryInvestorPositionDetail(self, pInvestorPositionDetail, pRspInfo, nRequestID, bIsLast):
        """请求查询投资者持仓明细响应"""

    def OnRspQryNotice(self, pNotice, pRspInfo, nRequestID, bIsLast):
        """请求查询客户通知响应"""

    def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        """请求查询结算信息确认响应"""

    def OnRspQryInvestorPositionCombineDetail(self, pInvestorPositionCombineDetail, pRspInfo, nRequestID, bIsLast):
        """请求查询投资者持仓明细响应"""

    def OnRspQryCFMMCTradingAccountKey(self, pCFMMCTradingAccountKey, pRspInfo, nRequestID, bIsLast):
        """查询保证金监管系统经纪公司资金账户密钥响应"""

    def OnRspQryEWarrantOffset(self, pEWarrantOffset, pRspInfo, nRequestID, bIsLast):
        """请求查询仓单折抵信息响应"""

    def OnRspQryTransferSerial(self, pTransferSerial, pRspInfo, nRequestID, bIsLast):
        """请求查询转帐流水响应"""

    def OnRspQryAccountregister(self, pAccountregister, pRspInfo, nRequestID, bIsLast):
        """请求查询银期签约关系响应"""

    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        """错误应答"""

    def OnRtnOrder(self, pOrder):
        """报单通知"""

    def OnRtnTrade(self, pTrade):
        """成交通知"""

    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        """报单录入错误回报"""

    def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
        """报单操作错误回报"""

    def OnRtnInstrumentStatus(self, pInstrumentStatus):
        """合约交易状态通知"""

    def OnRtnTradingNotice(self, pTradingNoticeInfo):
        """交易通知"""

    def OnRtnErrorConditionalOrder(self, pErrorConditionalOrder):
        """提示条件单校验错误"""

    def OnRspQryContractBank(self, pContractBank, pRspInfo, nRequestID, bIsLast):
        """请求查询签约银行响应"""

    def OnRspQryParkedOrder(self, pParkedOrder, pRspInfo, nRequestID, bIsLast):
        """请求查询预埋单响应"""

    def OnRspQryParkedOrderAction(self, pParkedOrderAction, pRspInfo, nRequestID, bIsLast):
        """请求查询预埋撤单响应"""

    def OnRspQryTradingNotice(self, pTradingNotice, pRspInfo, nRequestID, bIsLast):
        """请求查询交易通知响应"""

    def OnRspQryBrokerTradingParams(self, pBrokerTradingParams, pRspInfo, nRequestID, bIsLast):
        """请求查询经纪公司交易参数响应"""

    def OnRspQryBrokerTradingAlgos(self, pBrokerTradingAlgos, pRspInfo, nRequestID, bIsLast):
        """请求查询经纪公司交易算法响应"""

    def OnRtnFromBankToFutureByBank(self, pRspTransfer):
        """银行发起银行资金转期货通知"""

    def OnRtnFromFutureToBankByBank(self, pRspTransfer):
        """银行发起期货资金转银行通知"""

    def OnRtnRepealFromBankToFutureByBank(self, pRspRepeal):
        """银行发起冲正银行转期货通知"""

    def OnRtnRepealFromFutureToBankByBank(self, pRspRepeal):
        """银行发起冲正期货转银行通知"""

    def OnRtnFromBankToFutureByFuture(self, pRspTransfer):
        """期货发起银行资金转期货通知"""

    def OnRtnFromFutureToBankByFuture(self, pRspTransfer):
        """期货发起期货资金转银行通知"""

    def OnRtnRepealFromBankToFutureByFutureManual(self, pRspRepeal):
        """系统运行时期货端手工发起冲正银行转期货请求，银行处理完毕后报盘发回的通知"""

    def OnRtnRepealFromFutureToBankByFutureManual(self, pRspRepeal):
        """系统运行时期货端手工发起冲正期货转银行请求，银行处理完毕后报盘发回的通知"""

    def OnRtnQueryBankBalanceByFuture(self, pNotifyQueryAccount):
        """期货发起查询银行余额通知"""

    def OnErrRtnBankToFutureByFuture(self, pReqTransfer, pRspInfo):
        """期货发起银行资金转期货错误回报"""

    def OnErrRtnFutureToBankByFuture(self, pReqTransfer, pRspInfo):
        """期货发起期货资金转银行错误回报"""

    def OnErrRtnRepealBankToFutureByFutureManual(self, pReqRepeal, pRspInfo):
        """系统运行时期货端手工发起冲正银行转期货错误回报"""

    def OnErrRtnRepealFutureToBankByFutureManual(self, pReqRepeal, pRspInfo):
        """系统运行时期货端手工发起冲正期货转银行错误回报"""

    def OnErrRtnQueryBankBalanceByFuture(self, pReqQueryAccount, pRspInfo):
        """期货发起查询银行余额错误回报"""

    def OnRtnRepealFromBankToFutureByFuture(self, pRspRepeal):
        """期货发起冲正银行转期货请求，银行处理完毕后报盘发回的通知"""

    def OnRtnRepealFromFutureToBankByFuture(self, pRspRepeal):
        """期货发起冲正期货转银行请求，银行处理完毕后报盘发回的通知"""

    def OnRspFromBankToFutureByFuture(self, pReqTransfer, pRspInfo, nRequestID, bIsLast):
        """期货发起银行资金转期货应答"""

    def OnRspFromFutureToBankByFuture(self, pReqTransfer, pRspInfo, nRequestID, bIsLast):
        """期货发起期货资金转银行应答"""

    def OnRspQueryBankAccountMoneyByFuture(self, pReqQueryAccount, pRspInfo, nRequestID, bIsLast):
        """期货发起查询银行余额应答"""

    def OnRtnOpenAccountByBank(self, pOpenAccount):
        """银行发起银期开户通知"""

    def OnRtnCancelAccountByBank(self, pCancelAccount):
        """银行发起银期销户通知"""

    def OnRtnChangeAccountByBank(self, pChangeAccount):
        """银行发起变更银行账号通知"""


def _init(Module, MdSpi, TraderSpi):
    globals()['ApiStruct'] = __import__(__name__+'.ApiStruct', None, None, 'x')

    class LazyProperty(object):
        def __get__(self, obj, cls):
            if obj is None: return self
            value = self.fget()
            name = self.fget.__name__
            setattr(obj, name, value)
            delattr(cls, name)
            return value

    def lazy_property(func):
        self = LazyProperty()
        setattr(Module, func.__name__, self)
        self.fget = func
        return self

    @lazy_property
    def MdApi():
        from ._MdApi import _init, MdApi; _init(ApiStruct)
        return type('MdApi', (MdApi,), MdSpi)

    @lazy_property
    def TraderApi():
        from ._TraderApi import _init, TraderApi; _init(ApiStruct)
        return type('TraderApi', (TraderApi,), TraderSpi)


def _init(init=_init, MdSpi=MdApi, TraderSpi=TraderApi):
    import sys
    from types import ModuleType, FunctionType as F

    f = (lambda f:F(f.__code__,env)) if sys.version_info[0] >= 3 else (lambda f:F(f.func_code,env))
    mod = sys.modules[__name__]; Module = type(mod)
    if Module is ModuleType:
        class Module(ModuleType): pass
        mod = Module(__name__); env = mod.__dict__
        env.update((k,v) for k,v in globals().items() if k.startswith('__') and k.endswith('__'))
        MdSpi = dict((k,f(v)) for k,v in MdSpi.__dict__.items() if k.startswith('On'))
        TraderSpi = dict((k,f(v)) for k,v in TraderSpi.__dict__.items() if k.startswith('On'))
        sys.modules[__name__] = mod
    else:
        env = mod.__dict__
        for k in ('MdApi','TraderApi','_init'): del env[k]
        MdSpi = dict((k,v) for k,v in MdSpi.__dict__.items() if k.startswith('On'))
        TraderSpi = dict((k,v) for k,v in TraderSpi.__dict__.items() if k.startswith('On'))

    f(init)(Module, MdSpi, TraderSpi)
_init()
