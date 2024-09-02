#include "CustomMdSpi.h"
#include "TickToKlineHelper.h"
#include <fstream>
#include <iostream>
#include <unordered_map>

// ---- 全局参数声明 ---- //
extern CThostFtdcMdApi *g_pMdUserApi;            // 行情指针
extern char gMdFrontAddr[];                      // 模拟行情前置地址
extern TThostFtdcBrokerIDType gBrokerID;         // 模拟经纪商代码
extern TThostFtdcInvestorIDType gInvesterID;     // 投资者账户名
extern TThostFtdcPasswordType gInvesterPassword; // 投资者密码
extern char
    *g_pInstrumentID[];   // 行情合约代码列表，中、上、大、郑交易所各选一种
extern int instrumentNum; // 行情合约订阅数量
extern std::unordered_map<std::string, TickToKlineHelper>
    g_KlineHash; // k线存储表

// ---- ctp_api回调函数 ---- //
// 连接成功应答
void CustomMdSpi::OnFrontConnected() {
  std::cout << "=====建立网络连接成功=====" << std::endl;
  // 开始登录
  CThostFtdcReqUserLoginField loginReq;
  memset(&loginReq, 0, sizeof(loginReq));
  strcpy(loginReq.BrokerID, gBrokerID);
  strcpy(loginReq.UserID, gInvesterID);
  strcpy(loginReq.Password, gInvesterPassword);
  static int requestID = 0; // 请求编号
  int rt = g_pMdUserApi->ReqUserLogin(&loginReq, requestID);
  if (!rt)
    std::cout << ">>>>>>发送登录请求成功" << std::endl;
  else
    std::cerr << "--->>>发送登录请求失败" << std::endl;
}

// 断开连接通知
void CustomMdSpi::OnFrontDisconnected(int nReason) {
  std::cerr << "=====网络连接断开=====" << std::endl;
  std::cerr << "错误码： " << nReason << std::endl;
}

// 心跳超时警告
void CustomMdSpi::OnHeartBeatWarning(int nTimeLapse) {
  std::cerr << "=====网络心跳超时=====" << std::endl;
  std::cerr << "距上次连接时间： " << nTimeLapse << std::endl;
}

// 登录应答
void CustomMdSpi::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin,
                                 CThostFtdcRspInfoField *pRspInfo,
                                 int nRequestID, bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (!bResult) {
    std::cout << "=====账户登录成功=====" << std::endl;
    std::cout << "交易日： " << pRspUserLogin->TradingDay << std::endl;
    std::cout << "登录时间： " << pRspUserLogin->LoginTime << std::endl;
    std::cout << "经纪商： " << pRspUserLogin->BrokerID << std::endl;
    std::cout << "帐户名： " << pRspUserLogin->UserID << std::endl;
    // 开始订阅行情
    int rt = g_pMdUserApi->SubscribeMarketData(g_pInstrumentID, instrumentNum);
    if (!rt)
      std::cout << ">>>>>>发送订阅行情请求成功" << std::endl;
    else
      std::cerr << "--->>>发送订阅行情请求失败" << std::endl;
  } else
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 登出应答
void CustomMdSpi::OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout,
                                  CThostFtdcRspInfoField *pRspInfo,
                                  int nRequestID, bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (!bResult) {
    std::cout << "=====账户登出成功=====" << std::endl;
    std::cout << "经纪商： " << pUserLogout->BrokerID << std::endl;
    std::cout << "帐户名： " << pUserLogout->UserID << std::endl;
  } else
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 错误通知
void CustomMdSpi::OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID,
                             bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (bResult)
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 订阅行情应答
void CustomMdSpi::OnRspSubMarketData(
    CThostFtdcSpecificInstrumentField *pSpecificInstrument,
    CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (!bResult) {
    std::cout << "=====订阅行情成功=====" << std::endl;
    std::cout << "合约代码： " << pSpecificInstrument->InstrumentID
              << std::endl;
    // 如果需要存入文件或者数据库，在这里创建表头,不同的合约单独存储
    char filePath[100] = {'\0'};
    sprintf(filePath, "%s_market_data.csv", pSpecificInstrument->InstrumentID);
    std::ofstream outFile;
    outFile.open(filePath, std::ios::out); // 新开文件
    outFile << "合约代码"
            << ","
            << "更新时间"
            << ","
            << "最新价"
            << ","
            << "成交量"
            << ","
            << "买价一"
            << ","
            << "买量一"
            << ","
            << "卖价一"
            << ","
            << "卖量一"
            << ","
            << "持仓量"
            << ","
            << "换手率" << std::endl;
    outFile.close();
  } else
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 取消订阅行情应答
void CustomMdSpi::OnRspUnSubMarketData(
    CThostFtdcSpecificInstrumentField *pSpecificInstrument,
    CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (!bResult) {
    std::cout << "=====取消订阅行情成功=====" << std::endl;
    std::cout << "合约代码： " << pSpecificInstrument->InstrumentID
              << std::endl;
  } else
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 订阅询价应答
void CustomMdSpi::OnRspSubForQuoteRsp(
    CThostFtdcSpecificInstrumentField *pSpecificInstrument,
    CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (!bResult) {
    std::cout << "=====订阅询价成功=====" << std::endl;
    std::cout << "合约代码： " << pSpecificInstrument->InstrumentID
              << std::endl;
  } else
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 取消订阅询价应答
void CustomMdSpi::OnRspUnSubForQuoteRsp(
    CThostFtdcSpecificInstrumentField *pSpecificInstrument,
    CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
  bool bResult = pRspInfo && (pRspInfo->ErrorID != 0);
  if (!bResult) {
    std::cout << "=====取消订阅询价成功=====" << std::endl;
    std::cout << "合约代码： " << pSpecificInstrument->InstrumentID
              << std::endl;
  } else
    std::cerr << "返回错误--->>> ErrorID=" << pRspInfo->ErrorID
              << ", ErrorMsg=" << pRspInfo->ErrorMsg << std::endl;
}

// 行情详情通知
void CustomMdSpi::OnRtnDepthMarketData(
    CThostFtdcDepthMarketDataField *pDepthMarketData) {
  // 打印行情，字段较多，截取部分
  std::cout << "=====获得深度行情=====" << std::endl;
  std::cout << "交易日： " << pDepthMarketData->TradingDay << std::endl;
  std::cout << "交易所代码： " << pDepthMarketData->ExchangeID << std::endl;
  std::cout << "合约代码： " << pDepthMarketData->InstrumentID << std::endl;
  std::cout << "合约在交易所的代码： " << pDepthMarketData->ExchangeInstID
            << std::endl;
  std::cout << "最新价： " << pDepthMarketData->LastPrice << std::endl;
  std::cout << "数量： " << pDepthMarketData->Volume << std::endl;
  // 如果只获取某一个合约行情，可以逐tick地存入文件或数据库
  char filePath[100] = {'\0'};
  sprintf(filePath, "%s_market_data.csv", pDepthMarketData->InstrumentID);
  std::ofstream outFile;
  outFile.open(filePath, std::ios::app); // 文件追加写入
  outFile << pDepthMarketData->InstrumentID << ","
          << pDepthMarketData->UpdateTime << "."
          << pDepthMarketData->UpdateMillisec << ","
          << pDepthMarketData->LastPrice << "," << pDepthMarketData->Volume
          << "," << pDepthMarketData->BidPrice1 << ","
          << pDepthMarketData->BidVolume1 << "," << pDepthMarketData->AskPrice1
          << "," << pDepthMarketData->AskVolume1 << ","
          << pDepthMarketData->OpenInterest << "," << pDepthMarketData->Turnover
          << std::endl;
  outFile.close();

  // 计算实时k线
  std::string instrumentKey = std::string(pDepthMarketData->InstrumentID);
  if (g_KlineHash.find(instrumentKey) == g_KlineHash.end())
    g_KlineHash[instrumentKey] = TickToKlineHelper();
  g_KlineHash[instrumentKey].KLineFromRealtimeData(pDepthMarketData);

  // 取消订阅行情
  // int rt = g_pMdUserApi->UnSubscribeMarketData(g_pInstrumentID,
  // instrumentNum); if (!rt) 	std::cout << ">>>>>>发送取消订阅行情请求成功" <<
  // std::endl; else 	std::cerr << "--->>>发送取消订阅行情请求失败" <<
  // std::endl;
}

// 询价详情通知
void CustomMdSpi::OnRtnForQuoteRsp(CThostFtdcForQuoteRspField *pForQuoteRsp) {
  // 部分询价结果
  std::cout << "=====获得询价结果=====" << std::endl;
  std::cout << "交易日： " << pForQuoteRsp->TradingDay << std::endl;
  std::cout << "交易所代码： " << pForQuoteRsp->ExchangeID << std::endl;
  std::cout << "合约代码： " << pForQuoteRsp->InstrumentID << std::endl;
  std::cout << "询价编号： " << pForQuoteRsp->ForQuoteSysID << std::endl;
}