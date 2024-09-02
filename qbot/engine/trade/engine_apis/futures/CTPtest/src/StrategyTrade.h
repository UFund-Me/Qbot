#pragma once
// ---- 简单策略交易的类 ---- //

#include "CTP_API/ThostFtdcUserApiStruct.h"
#include "CustomTradeSpi.h"
#include "TickToKlineHelper.h"
#include <functional>

typedef void (*reqOrderInsertFun)(TThostFtdcInstrumentIDType instrumentID,
                                  TThostFtdcPriceType price,
                                  TThostFtdcVolumeType volume,
                                  TThostFtdcDirectionType direction);

using ReqOrderInsertFunctionType = std::function<void(
    TThostFtdcInstrumentIDType instrumentID, TThostFtdcPriceType price,
    TThostFtdcVolumeType volume, TThostFtdcDirectionType direction)>;

void StrategyCheckAndTrade(TThostFtdcInstrumentIDType instrumentID,
                           CustomTradeSpi *customTradeSpi);
