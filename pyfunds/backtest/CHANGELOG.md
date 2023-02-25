# Changelog

## Unreleased

## v0.11.7 - 2022.12.20

### updated

- 更新 2023 交易日历

### fixed

- 二进制表示十进制造成的分位误差

- 修复 `v_tradecost` 显示分红再投为交易点的 bug

## v0.11.6 - 2022.03.01

### fixed

- 网易数据源 encoding 修复

- 回测 cashobj 起始日期修复

## v0.11.5 - 2021.12.10

### added

- 更新 2022 A 股交易日历

### fixed

- 修复货币基金实时数据中的估值抓取处理报错

- 增加了场内账单默认净值的支持

- 可转债赎回价接口解析调整

## v0.11.4 - 2021.06.12

### added

- get_daily 增加富途数据源，包括了港股和美股的日线数据

- 增加 xa.cons.avail_dates 函数，用来将日期列表转变为最近的A股交易日列表

### fixed

- 实现 rget 状态码非 200 的自动重连

- 修复了波动率计算的乘数 typo

- 修复了 backtest 休市日期操作无法顺延的 bug

- 调整了 backtest 动态平衡类的赎回逻辑

- 修复了指数历史估值计算的除 0 bug

- 修复了 mul 类 tot 日期未传入的 bug

## v0.11.3 - 2021.01.31

### added

- 场内账单增加忽略基金的 # 前缀支持

- 增加了日历检查提醒

- 更新了主流国际市场 2021 休市日

- 增加了可转债工具箱对 B 评级可转债的支持

### fixed

- 进一步修改申购费自定义的小数点错误：第一笔申购情形

- 修复了 _float 中遇到百分数的 bug

- 转2修正为可转债类型

## v0.11.2 - 2021.01.01

### added

- 修复了 `get_rt` 获取基金实时净值

- `fundinfo` 增加 `set_price` 方法用来临时改正基金的价格和分红等信息

### fixed

- 修复了申购费自定义的小数点位置错误处理

- 修复了日期检查 2020->2021

## v0.11.1 - 2020.12.12

### added

- k 线图可视化支持颜色和边框颜色自定义

- k 线图支持显示多个技术指标曲线

- vinfo 增加不归一选项

- 增添可转债计算器的属性信息

- 增加 2021 A 股交易日历数据

### fixed

- 修复了 k 线图可视化图标最高价和最低价标记顺序的错误

- 修复工银传媒基金转型后，申购费率数据差异造成的测试失败

- 修复投资组合类 `mul` 同时 fundtradobj 和账单共存时的 bug

## v0.11.0 - 2020.10.11

### added

- `get_rt` 现在支持中港互认基金元数据

- `get_daily` 支持中港互认基金日线数据

- `fundinfo` 支持中港互认基金交易 （高阶功能可能暂时不可用）

### fixed

- 修复记账单.005 表记 0 申购费可能出现的 bug

## v0.10.3 - 2020.09.17

### added

- 增加动态平衡回测类

### fixed

- 修改 fundreport 类兼容新版本网站源

## v0.10.2 - 2020.08.20

### added

- 添加了 a 股股票行业判断 API, 由此支持查看基金持仓的各行业占比， `fundinfo.get_industry_holdings()`
- 在 get_daily 之外，添加了 `fundinfo.get_portfolio_holdings()` API，查看底层股债占比的逻辑更自然
- 增加基金基于持仓的行业自动判定（实验性支持）： `fundinfo.which_industry()`
- 增加 `mul.get_industry` 支持组合的行业透视

## v0.10.1 - 2020.08.10

### added

- 场外账单支持日期乱序记录（但每天仍必须严格一行）

### fixed

- 兼容天天基金 API 增量更新出现的累计净值空白
- 修复当日开仓的重计 bug
- 修复标普数据源表格包含 nan 行的 bug

## v0.10.0 - 2020.07.06

### fixed

- 修复 info 类兼容 set_backend 指定数据库后端的 bug

### added

- 增加全新的动态回测引擎模块 xa.backtest
- 为了兼容动态回测，trade 支持增量更新账单的交易处理

## v0.9.4 - 2020.07.02

### added

- record 可以直接处理内存中的 DataFrame 账单。
- ioconf 增加自定义 key_func, 兼容缓存层对 key 支持不够的情况 （大小写不敏感，特殊字符等）

### fixed

- evaluate 类的可视化函数补充 rendered 选项
- 修正了 tradevolume 周数和 pandas 给出的 iso 周数不一定对应的问题
- 修复了超高价转债债券收益率求解的 runtimeerror，直接返回 None

## v0.9.3 - 2020.06.20

### added

- get_rt 字典增加 time_ext 盘外数据时间
- 账单代码自动补全 6 位，前边智能补零

## v0.9.2 - 2020.06.08

### added

- 账单上自定义单项交易的申购赎回费用
- mulfix 添加了 v_tradecost(), 可视化显示买卖点

### fixed

- pyecharts 再次引入 breaking API，这样的上游显得有些不负责任，跟进过于麻烦，若无其他情况，将永久将 pyecharts 版本 pin 到 1.7.1，其他版本 pyecharts 不再支持

## v0.9.1 - 2020.05.31

### added

- get_daily 增加国债和企业债利率历史数据

### fixed

- 修复 value_label=1 时，-0.005 代表的全部赎回逻辑
- 修复了当日新开仓基金，当日 trade 出现的报错
- 优化了 v_tradevolume 柱形图的显示效果

## v0.9.0 - 2020.05.17

### added

- get_rt 增加货币基金元信息支持
- mul 增加资产分类扇形图， mul.v_category_positions()
- 基金组合分析增加了股票透视功能，mul.get_stock_holdings(2020, 1) 直接看穿底层持仓股票及比例
- 基金组合分析增加了股债比例穿透 mul.get_portfolio()
- 可转债价值全能计算器移入 toolbox，公开 API 进入主线支持

### fixed

- 完成了可转债定价工具的全面基准测试，并完善了几个数据细节

## v0.8.11 - 2020.05.15

### fixed

- xirrrate 支持调整时间起点，并修改内部 bug
- 允许账单的 date 不出现在第一列
- 修复了 trade 不支持按周计价净值基金的 bug

## v0.8.10 - 2020.05.01

### added

- 增加场内账单分红派息合拆送股的处理，支持特定行跳过
- 为 trade.v_tradecost() 增加买卖点标记（类似蚂蚁财富显示效果）
- 场内交易类也支持 tradecost 和 totvalue 可视化
- 指标类增加 pct_chg 方法，可以比较每年度的涨幅
- 股票日线数据除默认的前复权外，增加了后复权和不复权数据
- get_bar 支持 wsj 数据源（不保证连续的官方支持）
- 增加 mul 类 trade 覆盖逻辑，可同时提供部分 trade obj 和账单了

### fixed

- 继续完善 QDII 原油展期实时估值处理逻辑
- 优化 mul 的扇形图和 trade 折线图的显示效果
- 修正 get_bar 中的错误

## v0.8.9 - 2020.04.26

### fixed

- 中证数据源 dataframe close 列保证是 float
- 增加了原油期货交割日带来的 QDII 实时预测困难解决

### added

- 增加国证指数数据源
- 增加易盛商品指数系列数据源
- 增加基金大类资产持仓比例，通过 xa.get_daily("pt-F100032") 调取
- 增加 default_end, 用户可选择改变默认的 end 行为（今天，通常可改为昨天）
- 增加 ycharts 数据源

## v0.8.8 - 2020.04.16

### added

- get_rt 新浪源，A 股标的增加买卖前 5 手数据，可通过添加选项 \_from="sina" 调用
- 增加根据持仓的基金历史估值分析，同时使 PEBHistory 可以 dispatch 到指数，申万行业，个股和基金估值系统
- 工具箱增加 TEBHistory 可以估算拟合指数的资产和利润增速并可视化
- get_daily 增加中证指数源
- 增加 Overpriced 类工具，可以观察基金历史折溢价情况并分析

### fixed

- 修复 get_peb 的分流
- 继续完善 QDII 净值预测的跨市场逻辑处理

## v0.8.7 - 2020.04.10

### added

- 增加了基金详细股票和债券持仓的信息，可以通过 `fundinfo.get_holdings(year, season)` 调用

### fixed

- 修复了基金信息爬取的大量 corner cases, 包括 .5 年的记法，定开和封闭基金赎回费率的特殊写法，已终止基金的赎回费率处理，净值为空基金的报错，js 页面有大量换行的正则兼容

## v0.8.6 - 2020.04.09

### added

- mulfix 增加 istatus 账单读入
- get_rt 针对基金扩充更多元数据

### fixed

- 修复雪球实时 HK 开始的可能 bug
- 今日交易记录的 trade bug

## v0.8.5 - 2020.04.08

### added

- get_bar 增加聚宽源
- get_daily 支持基金累计净值
- get_rt 返回增加时间属性
- 日线增加成交量数据（注意缓存兼容性）
- 直接将绘制 k 线图 hack 到 df 上，df.v_kline()
- 支持 dataframe web 级的显示，可用 set_display 开关
- 增加 StockPEBHistory 类可以查看个股估值历史
- 对 get_daily 增加 fetchonly 更精细的控制缓存

### fixed

- 进一步完善跨市场休市日不同时的净值预测逻辑

## v0.8.4 - 2020.04.06

### added

- 增加 vinfo 类，使得任何 get_daily 可以拿到的标的都可以进行交易。
- 增加主流市场节假日信息
- 为 get 函数增加 handler 选项，方便钩子函数嵌套
- 增加非 QDII 的溢价实时预测类 RTPredict

### changed

- xa.set_backend 也可影响 fundinfo 的缓存设定

### fixed

- 进一步完善缓存刷新掉最后一天和节假日的处理逻辑

## v0.8.3 - 2020.04.04

### added

- get_bar 增加雪球源
- 增加 set_handler
- 增加更多 FT 数据
- 增加 lru_cache_time，带 ttl 的缓存更好的防止重复爬取

### fixed

- 防止 precached 之前的日线数据无法抓取
- 为 imul 增加 istatus 关键字参数作为冗余防止误输入
- predict 对于跨市场休市更完善的考虑

## v0.8.2 - 2020.04.02

### added

- 增加聚宽宏观数据到 get_daily
- QDIIPredict 实时预测支持不同时间片混合涨幅计算
- 增加 get_bar
- 英为实时增加 app 源
- 增加日志系统，可以打印网络爬虫的详细信息

### fixed

- 增加 daily_increment 的过去选项，防止假期阻止严格检查。
- get_daily 同时兼容双向人民币中间价

## v0.8.1 - 2020.04.01

### added

- 日线增加英为 app 源备份
- 增加 QDII 预测的日期返回, 增加溢价率估计，增加 t1 计算状态
- `set_proxy()` 空时添加取消代理功能，和 socks5 代理支持
- `set_holdings()` 允许外部导入数据 py
- 增加标的对应 id 的缓存

### fixed

- 改进为实时的新浪港股 API，之前 API 存在 15 分延时
- read excel 和网络下载部分解耦，增加稳定性和模块化

## v0.8.0 - 2020.03.30

### added

- 添加 ft 日线数据源和实时数据
- 将净值预测的基础设施迁移重构进 xalpha，并封装成面向对象

### fixed

- 天天基金总量 API 中，累计净值里可能存在 null
- 港股新浪实时数据现价抓取错位

## v0.7.1 - 2020.03.29

### added

- 申万行业指数历史估值情况
- cachedio 缓存器增加周末校验，周末区间自动不爬取数据
- 为 Compare 增加 col 选项，支持 close 之外的列的比较
- `get_daily` 新增指数总利润和净资产查看，用于更准确的刻画宏观经济
- 增加雅虎财经日线数据获取

## v0.7.0 - 2020.03.27

### changed

- 将面向对象封装的工具箱从 universal 模块移到单独的 toolbox 模块。

### added

- 增加内存缓存作为 IO 缓存的双重缓存层，提高数据读写速度。
- `get_daily` 增加彭博的日线数据获取。
- `mul` 增加 istatus 选项，可以场内外账单同时统计。
- `get_rt` 增加新浪实时数据源，同时增加 double_check 选项确保实时数据稳定无误。

### fixed

- 完善聚宽云平台使用的导入。

## v0.6.2 - 2020.03.25

### added

- `set_backend` 增加 `precached` 预热选项，可以一次性缓存数据备用。
- 增加 `Compare` 类进行不同日线的比较。

## v0.6.1 - 2020.03.25

### added

- `get_daily` 增加聚宽数据源的场内基金每日份额数据
- `get_daily` 增加标普官网数据源的各种小众标普指数历史数据

## v0.6.0 - 2020.03.24

### added

- 增加了持久化的透明缓存装饰器，用于保存平时的数据 `cachedio`，同时支持 csv，数据库或内存缓存。
- 增加了数据源提供商抽象层，并加入 jqdata 支持。
- 提供了基于 jqdata 的指数历史估值系统，和估值总结类 `PEBHistory`。

## v0.5.0 - 2020.03.21

### added

- 增加了场内数据记账单和交易的分析处理
- 增加了查看基金报告的类 FundReport

### fixed

- 爬取人民币中间价增加 UA，因为不加还是偶尔会被反爬

## v0.4.0 - 2020.03.12

### fixed

- 雪球数据获取，设定 end 之后的问题造成起点偏移，已解决。

### added

- 全新的基金特性设定接口，包括四舍五入机制，按金额赎回记录，和分红默认行为切换，均可以通过记账单第一行或 mul 类传入 property 字典来设定，且完全向后兼容。

## v0.3.2 - 2020.03.11

### fixed

- 通过 get_daily 获取的基金和雪球数据日线，不包括 end 和 start 两天，已修正为包括。

### changed

- 增加 rget 和 rpost 容错，使得 universal 部分的下载更稳定。

## v0.3.1 - 2020.03.09

### added

- 增加了 `get_daily` 的缓存装饰器，可以轻松无缝的缓存所有日线数据，防止反复下载

## v0.3.0 - 2020.03.08

### added

- 重磅增加几乎万能的日线数据获取器 `get_daily`
- 增加几乎万能的实时数据获取器 `get_rt`

### fixed

- pandas 1.0+ 的 `pandas.Timestamp` API 要求更严，bs 的 NavigableString 不被接受，需要先用 `str` 转回 python str
- day gap when incremental update: if today's data is published, add logic to avoid this

### changed

- `fundinfo` 解析网页逻辑重构，直接按字符串解析，不再引入 js parser，更加简洁, 依赖更少。

## v0.2.0 - 2020.02.19

### fixed

- 调整到支持 pyecharts 1.0+ 的可视化 API，部分可视化效果有待进一步调整
- 调整 v_tradevolume 语句顺序，避免无卖出时可视化空白的问题
- 暂时限制 pandas 为 0.x 版本，1.x 版本暂时存在时间戳转化的不兼容问题待解决
- 基金增量更新调整，防止更新区间过长时，更新数据不全的问题
- 解决 list 格式账单一天单个基金多次购买的计算 bug
- 将工作日 csv 本地化，从而绕过 tushare PRO API 需要 token 的缺点（普通 API 尚未支持 2020 年交易日数据）

## v0.1.2 - 2019.05.29

### added

- 增加了 fundinfo 和 mfundinfo 的自动选择逻辑
- 增加了新格式交易单的读取接口
- 增加了统一的异常接口

### fixed

- 暂时固定 pyecharts 为老版本（将在下一次发布时修改为支持 pyecharts 1.0+）
- fundinfo 增量更新，指定为货币基金代码的时候，可以妥善地报异常

## v0.1.1 - 2018.12.29

### changed

- 更简洁的底层逻辑，用来处理多个基金日期不完全相同的情形

### fixed

- 对于基金类增量更新的 API 中注释栏的处理进行了完善

## v0.1.0 - 2018.08.20

### added

- record 类增加 save_csv 函数，将账单一键保存
- info 各个类增加了增量更新的逻辑，可以将数据本地化到 csv 文件，大幅提升了速度
- info 类的增量更新亦可选择任意 sqlalchemy 支持连接的数据库，将数据本地化

### fixed

- 进一步校正 trade 类 dailyreport 在未发生过交易时的展示逻辑

## v0.0.7 - 2018.08.17

### added

- indicator 模块增加了大量技术面指标的计算工具，并针对性的设计了新的可视化函数
- 增加了基于不同技术指标交叉或点位触发的交易策略

### fixed

- 将时间常量修改为函数
- 注意到 QDII 基金可能在美国节假日无净值，从而造成和国内基金净值天数不同的问题，修复了在 evaluate 模块这部分的处理逻辑
- 解决部分可视化函数字典参数传入不到位问题

## v0.0.6 - 2018.08.14

### added

- 新增真实的货币基金类 mfundinfo，与虚拟货币基金类 cashinfo 互为补充
- 新增了 realtime 模块，可以根据存储制定的策略，提供实时的投资建议，并自动发送邮件通知

### fixed

- info 类赎回逻辑的进一步完善，未来赎回则视为最后一个有记录的净值日赎回
- info 类故意屏蔽掉今天的净值，即使净值已更新，防止出现各种逻辑错误
- 完善 policy 的各个子类，使其对未来测试兼容

## v0.0.5 - 2018.08.12

### added

- mul 类增加返回 evaluate 对象的函数
- 增加了新的模块 evaluate 类，可以作为多净值系统的比较分析工具，现在提供净值可视化与相关系数分析的功能

### fixed

- 基金组合总收益率展示改为以百分之一为单位
- 交易类的成本曲线可视化改为自有交易记录开始
- 对于 fundinfo 的处理逻辑更加完善，进一步扩大了对各种情形处理的考量
- 完善 trade 类中各量计算时，早于基金成立日的处理逻辑

## v0.0.4 - 2018.08.09

### added

- policy 模块增加网格交易类，以进行波段网格交易的回测分析和指导
- 更直接的一键虚拟清仓功能添加到 record 类，并将具有 status 的类都视为有 record 的 MixIn
- v_tradevolume() 这一基于现金表的可视化函数，增加了 freq ＝ 的关键字参数，可选 D，W，M，从而直接展示不同时间为单位的交易总量柱形图

### changed

- 修改了基金收益率的计算逻辑，大幅重构了 dailyreport 的内容和计算，并引入了简单的换手率指标估算

### deprecated

- 鉴于 mul 类中 combsummary 函数展示数据的完整度很高，tot 函数不再推荐使用

## v0.0.3 - 2018.08.06

### added

- 增加基于现金流量表的成交量柱形图可视化
- 增加 mul 类的 combsummary 展示总结函数
- policy 增加了可以定期不定额投资的 scheduled_tune 类

### fixed

- 可视化函数绘图关键词传入的修正
- policy 类生成投资 status 时遍历所有时间而非只交易日
- 注意了 fundinfo 类中时间戳读取的时区问题，使得程序可以在不同系统时间得到正确结果

## v0.0.2 - 2018.08.03

### added

- 配置 setup.py，使得通过 pip 安装可以自动安装依赖，注意 ply 库采用了老版本 3.4，这是为了防止调用 slimit 库时不必要的报 warning
