#pragma once
// ---- 计算k线的类 ---- //

#include <string>
#include <vector>

// k线数据结构
struct KLineDataType {
  double open_price;  // 开
  double high_price;  // 高
  double low_price;   // 低
  double close_price; // 收
  int volume;         // 量
};

class TickToKlineHelper {
public:
  // 从本地数据构建k线，并存储到本地(假定本地数据没有丢包)
  void KLineFromLocalData(const std::string &sFilePath,
                          const std::string &dFilePath);
  // 从实时数据构建k线
  void KLineFromRealtimeData(CThostFtdcDepthMarketDataField *pDepthMarketData);

public:
  std::vector<double> m_priceVec; // 存储1分钟的价格
  std::vector<int> m_volumeVec;   // 存储1分钟的成交量
  std::vector<KLineDataType> m_KLineDataArray;
};
