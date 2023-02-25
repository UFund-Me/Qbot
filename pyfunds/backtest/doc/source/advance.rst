.. _advance:

===========
高级用法
===========

数据缓存
--------

xalpha 有两部分可以提供数据缓存和本地化。

基金交易部分数据
+++++++++++++++++++

第一部分是本地化与增量更新 info 系列的对象，比如 ``fundinfo``, ``indexinfo``, ``mfundinfo`` 等，这样就不需要每次再去爬取处理以前的净值，费率等等。
其本地化的不只是净值数据，也包括基金名称，基金费率等元信息。

其使用方法是，直接将 ``fetch=True`` （首先尝试从本地读取数据）,
``save=True`` （更新的数据存回本地）, ``form="csv"/"sql"`` （本地后端是 csv 文件还是 sql 数据库） 和
``path="path"/engine`` （对应 csv 的本地存储路径或对应 sql 的 SQLAlchemy.engine 类.
作为参数传入 ``fundinfo`` 等。
如果是基金组合，也可以直接将这些参数传入 ``mul`` 或 ``mulfix`` 类。
格式为 sql 时， path 示例：

.. code-block:: python

    import xalpha as xa
    from sqlalchemy import create_engine
    engine = create_engine('mysql://root:password@127.0.0.1/database?charset=utf8')
    io = {"save": True, "fetch": True, "form": "sql", "path": engine}
    xa.fundinfo("510018", **io)


get_daily 数据透明缓存
++++++++++++++++++++++++++++

第二部分本地化和缓存是专门针对 ``get_daily`` 界面的，用于存储对应的日期-价格表。这一部分的缓存和本地化更加透明。不需要任何设置，``get_daily`` 就自带内存缓存，
不会去爬取重复数据。如果想要把数据本地化存储，只需要 ``xa.set_backend(backend=, path=, prefix=, precached=)`` 即可。

其中 backend 同样可以是 csv 和 sql，也可以是默认的 memory。
path 与第一部分相同为 csv 存储的文件夹或 sql 的 engine 对象。prefix 是每个表单会添加的前缀，否则默认是用 code 做键值。
precached 可以不设，若设置为 %Y%m%d 的时间字符串格式，则代表第一次爬取就"预热"从 precached 到昨日的数据缓存。
注意到即使选取了数据库或文件作为后端，内存作为二级缓存依旧发挥作用，只要数据不改变，仍会直接读取内存数据，因此提升读写数据速度。

如果担忧内存中数据被"污染"，可以通过 ``xa.universal.check_cache(code, start, end)`` 来校验对应数据的准确性。也可用 ``xa.universal.reset_cache()`` 来清空现有的内存数据缓存。


最后为了可以在运行时动态改变 xalpha 函数的缓存行为，也即任何时刻 ``xa.set_backend`` 都可以生效，xalpha 强烈推荐所有函数，都以 ``xa.meth`` 的形式使用，
强烈不建议 ``from xalpha import meth`` 这种导入方式。

.. Note::

    若不设定第一部分基金交易的缓存，则 ``xa.set_backend()`` 的设定会默认决定第一部分基金元数据的缓存位置，一旦后端是 csv 或 sql，基金信息类的缓存将默认打开，
    默认 fetch=True, svae=True. 因此 ``xa.set_backend()`` 事实上成为了设置 xalpha 数据缓存的统一接口。


对于部分数据，由于程序升级的不兼容或者缓存数据损坏造成希望重新获取而刷新掉缓存的话，可以在 get_daily 添加 refresh 选项，也即 ``xa.get_daily(code, refresh=True)``，
这会重新刷新关于 code 的本地缓存。

而对于另一些数据，我们不希望去更新，只希望使用缓存的数据，即使其日期不全（可能是由于节假日造成的错觉），这时可以添加 fetchonly 选项，也即 ``xa.get_daily(code, fetchonly=True)``.

fetchonly 和 refresh 选项也可在 set_backend 设定，则全局生效。

get_daily 不指定起止时间的时候，默认采用 end=today, prev=365, 这两个的行为也可以通过 ``defaultend=`` 和 ``defaultprev=`` 在 ``xa.set_backend`` 设置。其中 defaultend
可以是日期字符串或日期对象或返回日期对象的函数。

此外，考虑到有些数据库后端，可能由于特殊符号和大小写不敏感等情况，导致表名冲突或出错。有两种解决方案，第一 ``xa.get_daily("LK", key="lk")``, 在每次使用 get_daily 时，单独指定 key，则 key 作为存储的表名。
或者一劳永逸的办法，``xa.set_backend(path=, backend=, key_func=lambda s: s.lower())``, 通过给 ``set_backend`` 指定 ``key_func`` 参数，则每个 ``get_daily`` 的数据存储，都会将原来的 key （默认为标的代码）在 ``key_func(key)`` 转化一下。


数据本地化
-------------
数据缓存部分提供的方法已经足够满足绝大多数数据本地化的要求，可以透明地将数据落地到本地文件系统或关系型数据库。

如果需要更复杂的本地化需求，考虑到 xalpha 中所有数据都是以 pandas.DataFrame 格式存在，那么只需参考 DataFrame 的 IO 功能即可 `IOTools <https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html>`_ 。
数据可以一键落地到 csv， excel， hdf5， json，html， 数据库表格等格式。


数据可视化
----------------

xalpha 提供两部分的可视化。对于基金管理部分，相关类所有以 ``v_`` 开始的方法，均是 pyecharts 支持的可视化封装。
对于 toolbox 部分，``v()`` 方法，是 matplotlib 支持的可视化。

此外，考虑到所有数据均是 DataFrame 格式，用户也可以对任何数据，轻松可视化，参考代码 ``df.plot(x="date", y=["open", "close"])``.
更多关于对 DataFrame 的可视化，请参考 Pandas 文档， `Visualization <https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html>`_ 。

xalpha 也直接 hack 了些 dataframe 的方法用来链式调用提供更丰富的可视化。最典型的，对于有 date，open，close，high，low 和 volume（可选）列的 dataframe，
可以直接 ``df.v_kline()`` 绘制出标准的 web 级上 K 线图下交易量的行情图。


数据提供商
------------

xalpha 的数据来自天天基金，英为财情，雪球，彭博，标普，新浪财经，网易财经，雅虎财经等多个源头，xalpha 的哲学是尽量利用免费的透明数据源。
但有些数据还是会依赖需要鉴权的数据 API，这些被抽象成数据提供商。

比如 xalpha 的历史估值系统，依赖聚宽的数据，那么就有两种方案。

本地调用聚宽数据
+++++++++++++++++++

第一种是本地 ``pip install jqdatasdk`` 并且申请聚宽的本地数据试用权限（免费），
之后通过 ``xa.provider.set_jq_data(user, password)`` 即可。

如果希望不需要每次使用 xalpha 都重新鉴权，也可以在 ``set_jq_data`` 添加 ``persistent=True``
的选项，这样聚宽账户密码会简单编码后存在本地（无加密保护，请自行衡量安全性），以后每次 ``import xalpha`` 聚宽的数据源都会自动激活。

云端使用 xalpha
+++++++++++++++++

第二种方案不需要聚宽本地数据，而是直接在聚宽云平台的研究环境来使用 xalpha，此时的初始化配置为::

    >>> !pip3 install xalpha --user
    >>> import sys
    >>> sys.path.insert(0, "/home/jquser/.local/lib/python3.6/site-packages")
    >>> import xalpha as xa
    >>> xa.provider.set_jq_data(debug=True)


主要模块的关系和逻辑
---------------------
:py:mod:`xalpha.cons` 模块主要提供一些基础的函数和常量， :py:mod:`xalpha.remain` 则专门提供了一些处理分时持仓表 remtable 的函数。

:py:mod:`xalpha.record` 用于统一的处理 status 记账单，同时自身实例化可以读取 csv 文件的原有账单。且可被其他具有 status 属性的类继承，作为广泛的 status 账单处理的工具箱。 而 :py:mod:`xalpha.policy` 则用于制定虚拟的 status 记账单，来进行不同策略投资的回测，其也继承了 :class:`xalpha.record.record` 中一般的记账单处理函数。

:py:mod:`xalpha.indicator` 被具有净值表或可生成净值表的类继承，提供了一揽子净值量化分析和可视化的工具箱。其被 :class:`xalpha.info.basicinfo` 和 :class:`xalpha.multiple.mulfix` 继承和使用，后者需要通过设定 benchmark 的函数来初始化净值表。

:py:mod:`xalpha.realtime` 则是围绕基金的实时净值获取，策略集成和监视提醒为主的模块，可以用于每日按照多样的策略自动提醒投资情况。

其他四个系统的核心模块，所具有的核心数据表（都是 pandas.DataFrame 的形式），以及相互之间的关系，如下图所示。

.. image:: https://user-images.githubusercontent.com/35157286/43990032-fd6f8a3a-9d87-11e8-95c4-206b13734b40.png
 

在新版本的 xalpha 中提供了更丰富的数据抓取系统：

:py:mod:`xalpha.universal` 模块维护了不同的数据抓取，并对外提供统一的接口 :func:`xalpha.universal.get_daily` 和 :func:`xalpha.universal.get_rt`。

:py:mod:`xalpha.provider` 模块维护了需要注册的数据提供方的信息及验权接口。

:py:mod:`xalpha.toolbox` 模块维护了面向对象，封装数据的一些工具箱。

:py:mod:`xalpha.backtest` 模块维护了一个轻量级但扩展性强大的简单动态低频回测框架。

:py:mod:`xalpha.misc` 模块包含一些测试功能和爬虫组件，没有文档，随时 API 变更，也不受官方主线支持，生产环境慎用！



以下对象内部封装的数据结构均基于 pandas.DataFrame

*	记账单 status
*	净值表 price
*	现金流量表 cftable
*	仓位分时表 remtable


记账单格式说明
---------------------------

如果用户想一览自己的交易分析，那么记账单总是用户需要提供的，一般可以通过读取 csv 的方式导入 xalpha， 也即 ``xa.record(path)`` 即可，对于场内交易的账单，则需要 ``xa.irecord(path)``。
记账单的具体合法格式可以参考 :func:`xalpha.record.record` 的说明。


场外账单格式
++++++++++++++++

首先记账单分为场外和场内，需要提供单独的记账单。场外记账单无需提供每次申赎时的净值，因为这些值被时间唯一确定，可以智能抓取。
那么场外基金的账单，只需要时间，基金代码和数字三要素。对于数字，正数时代表申购金额，负数代表赎回份额，这与基金的申赎逻辑相符。
场外账单的默认格式是 matrix，也即每列的列头是一个不同的六位基金代码，每行的行头是一个独立的日期 (格式 20200202， **请注意同一日期必须全部在一行记录**)，对于对应日期和基金有交易的，则在相应单元格记录数额即可 （请注意下午三点之后的申赎应算作下个交易日）。
其他单元格可为空即可。
通常可以 Excel 等软件记录，导出成 csv 格式即可。这一格式账单的例子可以参考 github repo 中的 tests/demo.csv, 和 tests/demo2.csv.

场外账单的一些进阶说明：

1. 在基金代码的下一行(也即整个表格除表头的第一行，该行位置必须如此)可以额外增加 property，用于控制基金的默认交易行为。每个代码可以填写一个0到7的数字，空默认为0。其对应的交易行为是：
基金份额确认是四舍五入0 还是舍弃尾数 1， 基金是默认现金分红 0 还是分红再投 2， 基金是赎回数目对应份额 0 还是金额 4 （只支持货币基金）， property 数字为三者之和。

2. 关于交易数字的一些特别约定，交易数字小数点一位之后的非零位有特别约定，不代表交易的部分。
小数点后第二位如果是5，且当日恰好为对应基金分红日，标志着选择了分红再投入的方式，否则默认分红拿现金。（该默认行为 property 含 2 时可翻转）比如 100.05 的意思是当日分红再投入且又申购了 500 元。
对于赎回的负数，如果是一个绝对值小于 0.005 的数，标记了赎回的份额占当时总份额的比例而非赎回的份额数目， 其中-0.005对应全部赎回，线性类推。eg. -0.001对应赎回20%。

3. 账单上自定义申购费和赎回费，小数点后第三位的 5 标记，代表了该数据费用是自定义的。注意这和 -0.005 代表全部卖出并不冲突，其原因是自定义费用，
前边肯定不全为 0。第三位 5 之后，代表了 1% 位。也即 -51.28515 意义是赎回 51.28 份，赎回费为 1.5%. 200.205 代表申购 200.2 元，申购费为0
（因为标记位 5 后没有其他非零数字）。这种自定义通常可用于定期支付型基金的强制卖出（不收赎回费）和基金公司官网申购基金时申购费全免的记录。


.. Note::

    如果不适应这种矩阵型的记账单，场外记账单也可以采用流水式的，也即每行记录一笔交易，列头分别是 fund，date，和 trade。这一格式的例子可以参考 tests/demo1.csv。
    此时的日期格式是 2020/2/2. 这种形式的账单，通过 ``xa.record(path, format="list")`` 来读取，不过这种账单不支持在账单层面设置基金的交易行为参数 property,
    但该参数仍可在基金投资组合 ``xa.mul(status=xa.record(path, formath="list"), property=Dict[fundcode, property_number])`` 的时候传入。对于这种格式的场外账单，
    不保证之后会维持和矩阵型场外账单同样的功能，因此请优先考虑矩阵型的场外账单格式。


场内账单格式
++++++++++++++++


场内账单则统一采用流水形式，每一笔需要记录交易净值和交易份额，此时由于买卖都是份额，因此数字全部代表份额，正买负卖，若有分红折算等，需自己手动维护，额外添加交易记录实现。
场内账单的例子请参考 github 库中的 tests/demo3.csv. 其列头分别是 date,code,value,share,fee。date 格式为20200202。code 对应场内代码，开头需包含 SH 或 SZ。value 是成交的净值单价。
share 代表成交的份数。fee 代表手续费，也可以不计，则默认为0，建议记录以得到交易盈利的更好全景。

场内账单的读入使用 ``ist=xa.irecord(path)``. 其既可以传入专门的场内投资组合类 ``xa.imul(status=ist)``，
也可以和场内记账单一起传入投资组合类 ``xa.mul(status=st, istatus=ist)`` 进行场内外投资结果的汇总。

场内账单的分红派息拆合送股的处理。对于分红或派息，直接计 share 栏为 0，value 栏为全部返还的现金，正数。
对于拆合送股，造成的份额改变（无任何现金流变化），直接计 value 栏为 0，share 栏表示总的份额的增量，正数为增加，负数为减少。
对于申购新债等情况，可能统计时还有代码未上市，此时处理可能造成错误，需要在代码前加``#``表示省略该行记录，不予处理。待新股上市后，去掉代码前井号即可。(这一井号开头代码自动忽略的功能，也被场内账单支持。)


.. Note::

    场内账单处理逻辑为了保持和场外一致，也只处理到截止昨天的交易，因此可能出现和现时实盘不符的情形。



QDII 净值预测
---------------------------

净值预测接口请参考 :class:`xalpha.toolbox.QDIIPredict`.

基本使用说明，在提供了 holdings.py 的前提下（置于 xalpha 源代码文件夹，开源 xalpha 暂时默认不提供该文件，则预测需手动提供相应基金的持仓信息和基金交易市场，计价货币，休市时间，期货现货对应等元信息）

 .. code-block:: python

    import xalpha as xa
    xa.set_backend(backend="csv", path="./data") # 设置合适的本地化方案，也可不设，则数据仅会缓存在内存中
    nfyy = xa.QDIIPredict("SH501018", positions=True) # 初始化南方原油的净值预测，采取浮动仓位预测
    print(nfyy.t1_type) # 未计算
    print(nfyy.get_t1()) # 返回上个交易日的净值预测
    print(nfyy.t1_type) # 已计算
    print(nfyy.get_position()) # 返回基于前天和更早净值数据判断而得出的昨日仓位估计
    print(nfyy.get_t0()) # 实时净值预测
    print(nfyy.get_t1_rate()) # 实时市价相对昨日净值预测的溢价率
    print(nfyy.get_t0_rate()) # 实时市价相对实时估值的溢价率
    nfyy.benchmark_test("2020-01-01", "2020-03-01") # 回测一段时间内的预测效果
    nfyy.analyse() # 打印出回测的定量分析


导入外部 holdings.py 数据文件
+++++++++++++++++++++++++++++++

可将 holdings.py 文件与运行脚本置于同一文件夹，或任何在 PYTHONPATH 的文件夹

.. code-block:: python

    import holdings  # 导入外部的 holdings.py
    import xalpha as xa
    xa.set_holdings(holdings) # 设置 xalpha 使用该数据文件
    # 之后的操作与之前相同


自制 holdings.py 文件
+++++++++++++++++++++++++++++++

默认的 xalpha 不提供 holdings.py ，因此 QDII 净值预测只有脚手架，没有具体的数据文件，要想预测 QDII 基金的净值和溢价率，暂时使用可以直接提供持仓字典，传入 QDIIPredict 初始化参数中。
但打算长期持续使用的话，还是建议维护自己的 holdings.py 文件。下面将具体介绍 holdings.py 文件应具有的内容和格式。文件示例

.. code-block:: python

    no_trading_days = {}  # 市场对应休市日
    no_trading_days["LU"] = [
        "2020-01-01",
        "2020-04-10",
        "2020-04-13",
        "2020-05-01",
        "2020-12-24",
        "2020-12-25",
        "2020-12-31",
    ]

    market_info = {
        "SP5475707.2": "US",
        "FT-CSGOLD:SWX:USD": "CH",
    }  # 代码对应市场

    # 收盘北京时间，用于期货基准比较
    usend = 4  # winter 5
    euend = -1
    jpend = -10

    futures_info = {
        "indices/india-50-futures": "indices/s-p-cnx-nifty",
        "commodities/crude-oil": "commodities/crude-oil",
        "commodities/brent-oil": "commodities/brent-oil",
    }  # 期货对应现货


    alt_info = {
        "FT-AUCHAH:SWX:CHF": "BB-AUCHAH:SW",
        "indices/dj-us-select-oil-exploration-prod": "SP91988493.2",
    }
    # 标的备份替换，用于生产级稳定性

    # 单个标的非假期净值缺失日
    gap_info = {}  # Fcode: list of %Y-%m-%d
    gap_info["etfs/velocityshares-3x-long-crude-oil"] = ["2020-04-03"]  # 基金清盘

    # 计价货币信息

    currency_info = {
        "BB-AUCHAH:SW": "CHF",
        "FT-RICY:IOM": "USD",
        "etfs/powershares-india-portfolio": "USD",
    }

    # 基金持仓
    holdings = {}


    # 南方原油
    holdings_501018_19s4 = {
        "etfs/etfs-brent-1mth-uk": 17.51,  # UK
        "etfs/etfs-brent-crude": 15.04,  # UK
        "etfs/etfs-crude-oil": 7.34,  # UK
        "etfs/ipath-series-b-sp-gsci-crd-oil-tr": 0.06,  # US
        "etfs/powershares-db-oil-fund": 11.6,  # US
        "etfs/ubs-cmci-oil-sf-usd": 8.68,  # CH
        "etfs/united-states-12-month-oil": 8.14,  # US
        "etfs/united-states-brent-oil-fund-lp": 15.42,  # US
        "etfs/united-states-oil-fund": 9.63,  # US
    }

    holdings["501018"] = holdings_501018_19s4
    holdings["501018rt"] = {
        "commodities/brent-oil": {"weight": 30, "time": euend},
        "commodities/crude-oil~1": {"weight": 45, "time": usend},
        "commodities/crude-oil~2": {"weight": 20, "time": jpend},
    }
    # 将对应标的 T-1 及实时预测持仓，添加到 holdings 字典


    holdings["510510"] = {"SH000905": 100}  # 国内标的实时溢价率也支持，但需要调用的是 xa.RTPredict 类



具体解释如下

``no_trading_days``: Dict[str, List[str(%Y-%m-%d)]] eg. ``no_trading_days = {"FR": ["2020-02-02"]}``, 用来记录各个地区市场的非周末休息日，注意大部分主流市场的休市日信息已经在 ``xa.cons.holiday`` 中，而不需重复记录

``market_info``: Dict[str, str]. 对应标的的市场地区，如不存在，则默认网络抓取，如对应标的不支持市场信息，则按照标的货币信息推断。

``currency_info``: Dict[str, str]. 对应标的货币信息，大部分标的可通过 ``xa.get_rt`` 获取的，不必须记录。

``holdings``: Dict[str, Dict[str, float]]. 核心字典，key 可以是基金代码用于 T-1 净值预测或普通基金的实时净值预测，基金代码 + rt 用于 QDII 基金的实时净值预测。每个 value 是一个持仓字典。
数值代表比例，100为单位。对于 rt 字典，value 也可以还是一个字典，分别用 weight time base 来精准的表示对应比例和参考的基准时间与基准标的。

其他更进阶的信息字典一般不需要设置，如果有需求或疑问，请直接参考 :class:`xalpha.toolbox.QDIIPredict` 源代码，或开 issue 联系作者。

需要注意的是，上述内容看似复杂，但多是为了生产级的稳定性和速度，实际上只定义对应基金的 holdings 字典已经可以在绝大多数情形正常使用净值预测功能。


动态回测系统
------------

:py:mod:`xalpha.backtest` 引入了一个轻量级但可扩展性强的动态回测框架，支持编程回测较复杂的需求，（``xa.policy`` 简单策略无法充分支持的）。
通过自定义 ``xa.backtest.BTE`` 的子类，作为不同策略的回测引擎。同时该模块提供一些简单常见回测策略的例子。


日志系统
---------------

xalpha 引入了 python logger 的日志系统，尤其是用来记录网络链接和爬虫等详细的 debug 信息。


Jupyter 中的使用
+++++++++++++++++++++

.. code-block:: python

    import xalpha as xa
    import logging
    logger = logging.getLogger('xalpha')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

以上配置，日志将打印在 jupyter notebook 前端


脚本程序中使用
+++++++++++++++++

.. code-block:: python

    import xalpha as xa
    import logging
    logger = logging.getLogger('xalpha')
    logger.setLevel(logging.DEBUG)
    fhandler = logging.FileHandler(filename='debug.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)

以上配置，日志将输入文件 debug.log


get 方法钩子
-----------------

有时候可能用户自己维护了一部分数据或数据库，也可能用户有其他更好的数据 API 可用。为了将这些无缝的融合进 xalpha，我们引入了 handler 来处理。

举例来说，我的数据库里有 A 股股票的日线数据，而且我觉得这个数据质量比网上爬虫要好，那么我希望 ``xa.get_daily("SH600000")`` 的时候，
xalpha 不要去雪球爬取数据，而是直接从我的数据库里来拿，这样又快又稳。这样所有基于 xa.get_daily 构建的 xalpha 的工具箱就也可以继续无缝的使用了。

为了实现这点，可以按如下示例：

.. code-block:: python

    import xalpha as xa

    def fetch_from_database(code, start, end, **kws): # **kws 是声明钩子函数所必须的，即使你用不到
        if code.startswith("SH"): # 请只过滤符合要求的代码，其他代码仍然用 get_daily 方法
            # 这里定义连接数据库和拿数据
            return df # 最终返回符合约定的 pd.DataFrame, 比如必须有 date 列，type 是 pd.Timestamp
        else:
            return None # 对于不满足的代码，返回 None 即可，程序将自动按照原来的 get_daily 处理

    xa.set_handler(method="daily", f=fetch_from_database) # 设定好钩子
    xa.get_daily("SH600000") # 此时程序将从数据库获取日线数据

同样的方法，也可以应用到 ``get_rt`` 和 ``get_bar``, 对应的 method="rt", "bar".

应用举例，有时候你可能不希望抓取实时数据那么实时，每分钟更新一次实时数据就好，那你可以通过下面的方式实现 get_rt 的"迟滞化"。

.. code-block:: python

    import xalpha as xa

    @xa.universal.lru_cache_time(ttl=60)
    def cached_get_rt(code, **kws):
        return xa.get_rt(code, handler=False)

    xa.set_handler(method="rt", f=cached_get_rt)


set 方法总结
---------------

xalpha 激进地利用了 python 的 reflection 机制，很多设定可以运行时动态改变，这些往往被抽象成一些 ``set_`` 接口。

* set_proxy: 设定代理，支持 http 和 socks 代理，set_proxy() 可以立即取消代理 :func:`xalpha.provider.set_proxy`

* set_backend: 设定数据缓存的后端和行为 :func:`xalpha.universal.set_backend`

* set_holdings: 导入外部的 holdings.py 数据文件 :func:`xalpha.toolbox.set_holdings`

* set_handler: 为 ``get_`` 数据函数设定钩子 :func:`xalpha.universal.set_handler`

* set_jq_data: 聚宽数据源鉴权 :func:`xalpha.provider.set_jq_data`

* set_display: 若参数为 "notebook"，可以设定 dataframe 按照 web 级的表格显示，支持排序，搜索和翻页 :func:`xalpha.toolbox.set_display`


爬虫与反爬虫
-------------------

xalpha 本身不维护任何数据，所有数据都来自从不同数据源的即时爬虫。但由于 xalpha 设计巧妙的本地缓存策略，大部分数据都不需要重复爬取，使用和分析因此不需要过多的时间延迟。
xalpha 维护了极其丰富的数据源，横跨十几个不同的网站，其默认设置可以顺利的爬取这些网站的数据，不需要额外的配置。但部分数据源如彭博，可能需要 ``xa.set_proxy`` 设定代理才能链接。

xalpha 设计的尽量对数据源网站友好，通过丰富而合理的本地和内存缓存策略，可以极大的减少网络连接和下载数目，从而提升反应速度和减少对数据源服务器的冲击。
xalpha 也不建议被用作高频交易的组件，不提倡任何高强度爬取数据的行为。

如果对同一数据源链接强度过大，很有可能被限制 ip 从而无法获取数据。此时唯一的 workaround 就是设置代理 ``xa.set_proxy()``，从而改变 ip。
根据个人经验，最容易封禁 ip 从而无法爬取的数据源包括人民币中间价官方网站，彭博网站。此外，ft.com 和标普网站在部分情况容易出现访问超时或访问错误等问题，原因未知，似乎不是反爬策略造成的。

set_proxy 传入字符串可以是 http 或 socks5 代理地址，注意， socks5:// 格式的输入，不会改变使用本地的 DNS，如果想 DNS 查询也通过代理服务器的话，需使用 socks5h:// ,
这一约定与 curl 和 requests 同步。


一些投资概念的理解
----------------------------

封闭组合系统和开放组合系统
++++++++++++++++++++++++++++++

参考 `issue <https://github.com/refraction-ray/xalpha/issues/29>`_

当讨论 beta，alpha 或者最大回撤这些概念时，我们需要一个每日净值数据，也就是至少整个系统得有净值的概念。那么这样一个系统就是封闭系统。封闭系统的意思是，初始资金固定 （totmoney），之后不再投入资金了，只在系统内不同仓位间轮换（比如货币基金和股票）。这个具体例子里 totmoney=14000，是因为我们选了14个基金，每个1000元，这样恰好相当于初始现金全买了基金了。当然可以选择更大的 totmoney，那么就会有一部分钱一直在货币基金里。这样系统的每日净值，实际上就是每日现有资产总值和初始资金的比例。这就是 mulfix。这种系统的净值同时反应了投资者的择时和择标的能力。

而 mul 对应的系统，是“开放的”，也就是可以随时进钱，随时出钱。比如对于工薪族每月定投这种，用开放系统就比较合适。因为并不是刚开始就有36个月的钱在货币基金里，然后每月向基金移仓的。这样的系统当然也可以定义净值，但这种净值会很奇怪，只能反应投资者的择标的能力，而反应不了其择时能力（但很多时候择时能力贡献了利润的大部分）。因此我没有给 mul 净值的属性，所以这种 “开放” 系统是进行不了那些基于净值曲线的指标分析的。但是依旧可以计算内部收益率 mul.xirrrate()。一个资金反复进出的开放系统，究竟投资效果如何，主要靠 xirrrate 定量刻画。

作为一个理解 mul 和 mulfix 本质区别的例子，考虑某个基金，年初净值1.0，你投入了1000元，年中涨到 2.0, 你又投入了1000元，年末跌回 1.0. 请问这样一个系统看成开放系统和封闭系统，其净值是怎么变化的，从中你会理解到我为什么说开放系统的净值记录是失真的和没有意义的。（答案：若考虑成封闭系统，年末净值为0.75，如考虑成开放系统，年末净值为 1.0）


内部收益率和年化收益率
++++++++++++++++++++++++++

参考 `issue <https://github.com/refraction-ray/xalpha/issues/9>`_

计算上， anunalized return 就是最后日期的总资产金额除以开始的，然后按总天数开方就好了，比较简单。但是这种计算肯定不适用于开放系统，开放系统的投入金额怎么定义，总天数又怎么定义，这都是问题。
xirr 就是内部收益率，这个可以考虑到每一笔现金投入的时间成本，计算时首先增加一笔现在的全部卖出，然后对所有的现金流计算 c_1/t_1^r+c_2/t_2^r+...=0, 这个方程的解r，就是内部收益率，它并较准确的刻画了开放系统的年化情况。
两个收益率在封闭系统理论上是一样的，但由于 xirr 需要数值解方程，肯定会有一个误差，所以才会不完全一样。（其实还有 xirr 考虑了赎回费， returns 没考虑的因素）
至于开放系统定义一定时间内的收益率，则需将之前的基金持有净值，视为这一阶段第一日的买入？因为 xirr 计算需要每一笔现金流。
总结下就是，只有封闭的系统可以计算 annualized return，只有现金流闭合的系统（买入卖出全部能对上，不能有最后没卖掉的，也不能卖不存在的），才能计算 xirr。这是理论和现实所限制的，而不是程序实现。

关于涉及有分红基金分析的一些讨论
+++++++++++++++++++++++++++++++++++

一些能够实现分红再投入，在不同情形下分析的 workaround。

参考 `issue <https://github.com/refraction-ray/xalpha/issues/34>`_

一个基本范式

.. code-block:: python

    def fundinfo_buyandhold(code, start=None):
        f = xa.fundinfo(code)
        if not start:
            start = f.price.iloc[0]["date"].strftime("%Y%m%d")
        st = xa.policy.buyandhold(f, start=start, totmoney=1000)
        sys = xa.mulfix(status=st.status, totmoney=1000)
        sys.bcmkset(xa.cashinfo(start=start))
        sys.code = code
        sys.name = f.name
        return sys
