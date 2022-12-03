# pytrader

基于 [easytrader](https://github.com/shidenggui/easytrader) 和 [easyquotation](https://github.com/shidenggui/easyquotation) 的量化交易框架

支持东方财富自动交易

## web 系统

新增web，可以设置关注的股票，显示T操作价格

![关注的股票](doc/watch_stock.png)

## 策略文件

在strategies目录，可以参考已有的编写。

策略需要继承StrategyTemplate类，实现int和onbar等函数。

init 设置关注的股票，行情引擎就会推动股票行情。
 
```python

    def init(self):
        for stock_code in self.watch_stocks:
            self.quotation_engine.watch(stock_code)


```

行情数据到来时，触发on_bar函数：

```python


def on_bar(self, context: Context, data: Dict[str, DataFrame]):
    pass

```

- Context 是一个工具类，可以获取其他bar或者计算cci、rsi等指标
- data是推动的行情字典，可以用股票代码获取DataFrame类型的行情数据


## 在线交易

参见 tradertest.py ，会加载所有策略，稍微改动下也能支持制定策略

```python

import easyquant
from easyquant import DefaultLogHandler

print('测试 DEMO')

# 东财
broker = 'eastmoney'

# 自己准备
# {
#     "user": "",
#     "password": ""# }
need_data = 'account.json'

log_type = 'file'

log_handler = DefaultLogHandler(name='测试', log_type=log_type, filepath='logs.log')

m = easyquant.MainEngine(broker,
                         need_data,
                         quotation='online',
                         # 1分钟K线
                         bar_type="1m",
                         log_handler=log_handler)
m.is_watch_strategy = True  # 策略文件出现改动时,自动重载,不建议在生产环境下使用
m.load_strategy()
m.start()

```

## 回测

参考backtest.py，设置回测的时间和策略，注意使用quotation需要为tushare或者jqdata，可以自己申请

```python
import easyquotation

import easyquant
from easyquant import  DefaultLogHandler, PushBaseEngine
from easyquant.log_handler.default_handler import MockLogHandler
from strategies.CCI import Strategy

print('backtest 回测 测试 ')

broker = 'mock'
need_data = 'account.json'

#
mock_start_dt = "2020-01-01"
mock_end_dt= "2021-11-11"


m = easyquant.MainEngine(broker, need_data,
                         quotation='tushare',
                         # quotation='jqdata',
                         bar_type="1d")

log_handler = MockLogHandler(context=m.context)

# 选择策略
strategy = Strategy(user=m.user, log_handler=log_handler, main_engine=m)

m.start_mock(mock_start_dt, mock_end_dt, strategy)

print('mock end')

print(m.user.get_balance())

for deal in m.user.get_current_deal():
    print(deal.deal_time, deal.bs_type, deal.deal_price, deal.deal_amount)
```