## 一、引入

```python
import easytrader
```

## 二、设置交易客户端类型

**海通客户端**

```python
user = easytrader.use('htzq_client')
```

**华泰客户端**

```python
user = easytrader.use('ht_client')
```

**国金客户端**

```python
user = easytrader.use('gj_client') 
```

**通用同花顺客户端**

```python
user = easytrader.use('universal_client') 
```

注: 通用同花顺客户端是指同花顺官网提供的客户端软件内的下单程序，内含对多个券商的交易支持，适用于券商不直接提供同花顺客户端时的后备方案。

**其他券商专用同花顺客户端**

```python
user = easytrader.use('ths')
```

注: 其他券商专用同花顺客户端是指对应券商官网提供的基于同花顺修改的软件版本，类似银河的双子星(同花顺版本)，国金证券网上交易独立下单程序（核新PC版）等。



**雪球**

```python
user = easytrader.use('xq')
```


## 三、启动并连接客户端

### （一）其他券商专用同花顺客户端

其他券商专用同花顺客户端不支持自动登录，需要先手动登录。

请手动打开并登录客户端后，运用connect函数连接客户端。

```python
user.connect(r'客户端xiadan.exe路径') # 类似 r'C:\htzqzyb2\xiadan.exe'
```

### （二）通用同花顺客户端

需要先手动登录一次：添加券商，填入账户号、密码、验证码，勾选“保存密码”

第一次登录后，上述信息被缓存，可以调用prepare函数自动登录（仅需账户号、客户端路径，密码随意输入）。

### （三）其它

非同花顺的客户端，可以调用prepare函数自动登录。

调用prepare时所需的参数，可以通过`函数参数` 或 `配置文件` 赋予。

**1. 函数参数(推荐)**

```
user.prepare(user='用户名', password='雪球、银河客户端为明文密码', comm_password='华泰通讯密码，其他券商不用')
```

注: 雪球比较特殊，见下列配置文件格式

**2. 配置文件**

```python
user.prepare('/path/to/your/yh_client.json')  # 配置文件路径
```

注: 配置文件需自己用编辑器编辑生成, **请勿使用记事本**, 推荐使用 [notepad++](https://notepad-plus-plus.org/zh/) 或者 [sublime text](http://www.sublimetext.com/) 。

**配置文件格式如下：**

银河/国金客户端

```
{
  "user": "用户名",
  "password": "明文密码"
}

```

华泰客户端

```
{
  "user": "华泰用户名",
  "password": "华泰明文密码",
  "comm_password": "华泰通讯密码"
}

```

雪球

```
{
  "cookies": "雪球 cookies，登陆后获取，获取方式见 https://smalltool.github.io/2016/08/02/cookie/",
  "portfolio_code": "组合代码(例:ZH818559)",
  "portfolio_market": "交易市场(例:us 或者 cn 或者 hk)"
}
```

## 四、交易相关

### 1. 获取资金状况

```python
user.balance
```

**return**
```python
[{'参考市值': 21642.0,
  '可用资金': 28494.21,
  '币种': '0',
  '总资产': 50136.21,
  '股份参考盈亏': -90.21,
  '资金余额': 28494.21,
  '资金帐号': 'xxx'}]
```

### 2. 获取持仓

```python
user.position
```

**return**
```python
[{'买入冻结': 0,
  '交易市场': '沪A',
  '卖出冻结': '0',
  '参考市价': 4.71,
  '参考市值': 10362.0,
  '参考成本价': 4.672,
  '参考盈亏': 82.79,
  '当前持仓': 2200,
  '盈亏比例(%)': '0.81%',
  '股东代码': 'xxx',
  '股份余额': 2200,
  '股份可用': 2200,
  '证券代码': '601398',
  '证券名称': '工商银行'}]
```

### 3. 买入

```python
user.buy('162411', price=0.55, amount=100)
```

**return**

```python
{'entrust_no': 'xxxxxxxx'}
```

注: 系统可以配置是否返回成交回报。如果没配的话默认返回 `{"message": "success"}`

### 4. 卖出

```python
user.sell('162411', price=0.55, amount=100)
```

**return**

```python
{'entrust_no': 'xxxxxxxx'}
```

### 5. 一键打新

```python
user.auto_ipo()
```

### 6. 撤单

```python
user.cancel_entrust('buy/sell 获取的 entrust_no')
```

**return**

```
{'message': '撤单申报成功'}
```


### 7. 查询当日成交

```python
user.today_trades
```

**return**

```
[{'买卖标志': '买入',
  '交易市场': '深A',
  '委托序号': '12345',
  '成交价格': 0.626,
  '成交数量': 100,
  '成交日期': '20170313',
  '成交时间': '09:50:30',
  '成交金额': 62.60,
  '股东代码': 'xxx',
  '证券代码': '162411',
  '证券名称': '华宝油气'}]
```

### 8. 查询当日委托

```python
user.today_entrusts
```

**return**

```
[{'买卖标志': '买入',
  '交易市场': '深A',
  '委托价格': 0.627,
  '委托序号': '111111',
  '委托数量': 100,
  '委托日期': '20170313',
  '委托时间': '09:50:30',
  '成交数量': 100,
  '撤单数量': 0,
  '状态说明': '已成',
  '股东代码': 'xxxxx',
  '证券代码': '162411',
  '证券名称': '华宝油气'},
 {'买卖标志': '买入',
  '交易市场': '深A',
  '委托价格': 0.6,
  '委托序号': '1111',
  '委托数量': 100,
  '委托日期': '20170313',
  '委托时间': '09:40:30',
  '成交数量': 0,
  '撤单数量': 100,
  '状态说明': '已撤',
  '股东代码': 'xxx',
  '证券代码': '162411',
  '证券名称': '华宝油气'}]
```


### 9. 查询今日可申购新股

```python
from easytrader.utils.stock import get_today_ipo_data
ipo_data = get_today_ipo_data()
print(ipo_data)
```

**return**

```python
[{'stock_code': '股票代码',
  'stock_name': '股票名称',
  'price': 发行价,
  'apply_code': '申购代码'}]
```

### 10. 刷新数据

```
user.refresh()
```

### 11. 雪球组合比例调仓 ###

```python
user.adjust_weight('股票代码', 目标比例)
```

例如，`user.adjust_weight('000001', 10)`是将平安银行在组合中的持仓比例调整到10%。

## 五、退出客户端软件

```python
user.exit()
```

## 六、远端服务器模式

远端服务器模式是交易服务端和量化策略端分离的模式。

**交易服务端**通常是有固定`IP`地址的云服务器，该服务器上运行着`easytrader`交易服务。而**量化策略端**可能是`JoinQuant、RiceQuant、Vn.Py`，物理上与交易服务端不在同一台电脑上。交易服务端被动或主动获取交易信号，并驱动**交易软件**（交易软件包括运行在同一服务器上的下单软件，比如同花顺`xiadan.exe`，或者运行在另一台服务器上的雪球`xq`）。

远端模式下，`easytrader`交易服务通过以下两种方式获得交易信号并驱动交易软件：

### (一) 被动接收远端量化策略发送的交易相关指令

#### 交易服务端——启动服务

```python
from easytrader import server

server.run(port=1430) # 默认端口为 1430
```

#### 量化策略端——调用服务

```python
from easytrader import remoteclient

user = remoteclient.use('使用客户端类型，可选 yh_client, ht_client, ths, xq等', host='服务器ip', port='服务器端口，默认为1430')

user.buy(......)

user.sell(......)

# 交易函数用法同上，见“四、交易相关”
```

### (二) 主动监控远端量化策略的成交记录或仓位变化 


#### 1. 跟踪 `joinquant` / `ricequant`  的模拟交易

##### 1) 初始化跟踪的 trader

这里以雪球为例, 也可以使用银河之类 `easytrader` 支持的券商

```
xq_user = easytrader.use('xq')
xq_user.prepare('xueqiu.json')
```

##### 2) 初始化跟踪 `joinquant` / `ricequant` 的 follower

```
target = 'jq'  # joinquant
target = 'rq'  # ricequant
follower = easytrader.follower(target)
follower.login(user='rq/jq用户名', password='rq/jq密码')
```

##### 3) 连接 follower 和 trader

##### joinquant
```
follower.follow(xq_user, 'jq的模拟交易url')
```

注: jq的模拟交易url指的是对应模拟交易对应的可以查看持仓, 交易记录的页面, 类似 `https://www.joinquant.com/algorithm/live/index?backtestId=xxx`

正常会输出

![enjoy it](https://raw.githubusercontent.com/shidenggui/assets/master/easytrader/joinquant.jpg)

注: 启动后发现跟踪策略无输出，那是因为今天模拟交易没有调仓或者接收到的调仓信号过期了，默认只处理120s内的信号，想要测试的可以用下面的命令：

```python
jq_follower.follow(user, '模拟交易url',
          trade_cmd_expire_seconds=100000000000, cmd_cache=False)
```

- trade_cmd_expire_seconds 默认处理多少秒内的信号

- cmd_cache 是否读取已经执行过的命令缓存，以防止重复执行

目录下产生的 cmd_cache.pk，是用来存储历史执行过的交易指令，防止在重启程序时重复执行交易过的指令，可以通过 `follower.follow(xxx, cmd_cache=False)` 来关闭。

##### ricequant

```
follower.follow(xq_user, run_id)
```
注：ricequant的run_id即PT列表中的ID。


#### 2. 跟踪雪球的组合

##### 1) 初始化跟踪的 trader

同上

##### 2) 初始化跟踪 雪球组合 的 follower

```
xq_follower = easytrader.follower('xq')
xq_follower.login(cookies='雪球 cookies，登陆后获取，获取方式见 https://smalltool.github.io/2016/08/02/cookie/')
```

##### 3) 连接 follower 和 trader

```
xq_follower.follow(xq_user, 'xq组合ID，类似ZH123456', total_assets=100000)
```


注: 雪球组合是以百分比调仓的， 所以需要额外设置组合对应的资金额度

* 这里可以设置 total_assets, 为当前组合的净值对应的总资金额度, 具体可以参考参数说明
* 或者设置 initial_assets, 这时候总资金额度为 initial_assets * 组合净值

* 雪球额外支持 adjust_sell 参数，决定是否根据用户的实际持仓数调整卖出股票数量，解决雪球根据百分比调仓时计算出的股数有偏差的问题。当卖出股票数大于实际持仓数时，调整为实际持仓数。目前仅在银河客户端测试通过。 当 users 为多个时，根据第一个 user 的持仓数决定


#### 3. 多用户跟踪多策略

```
follower.follow(users=[xq_user, yh_user], strategies=['组合1', '组合2'], total_assets=[10000, 10000])
```

#### 4. 其它与跟踪有关的问题

使用市价单跟踪模式，目前仅支持银河

```
follower.follow(***, entrust_prop='market')
```

调整下单间隔, 默认为0s。调大可防止卖出买入时卖出单没有及时成交导致的买入金额不足

```
follower.follow(***, send_interval=30) # 设置下单间隔为 30 s
```
设置买卖时的滑点

```
follower.follow(***, slippage=0.05) # 设置滑点为 5%
```

## 七、命令行模式

#### 登录

```
 python cli.py --use yh --prepare gf.json
```

注: 此时会生成 `account.session` 文件保存生成的 `user` 对象

#### 获取余额 / 持仓 / 以及其他变量

```
 python cli.py --get balance
```

#### 买卖 / 撤单

```
 python cli.py --do buy 162411 0.450 100
```
#### 查看帮助

```
 python cli.py --help
```


