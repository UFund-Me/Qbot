<h1> <img src="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" width="42"/> 🤖 Qbot </h1>

[![CodeQL](https://github.com/UFund-Me/Qbot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/codeql-analysis.yml)
[![AutoTrade](https://github.com/UFund-Me/Qbot/actions/workflows/auto-trade.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/auto-trade.yml)
[![Pylint](https://github.com/UFund-Me/Qbot/actions/workflows/pylint.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/pylint.yml)
[![Coverage](https://github.com/UFund-Me/Qbot/actions/workflows/coverage.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/coverage.yml)
<a href="https://github.com/UFund-Me/Qbot"><img src="https://img.shields.io/badge/Python-%203.8|%203.9-000000.svg?logo=Python&color=blue" alt="Python version"></a>
<a href="https://ufund-me.github.io/Qbot/#/"><img src="https://readthedocs.org/projects/pyod/badge/?version=latest" alt="Documentation status"></a>

<div align="center">
  <a href="https://github.com/UFund-Me/Qbot" target="_blank" rel="noopener">
    <picture>
      <source media="(prefers-color-scheme: dark)" alt="Qbot" srcset="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" />
      <img alt="Qbot" width="224" src="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" />
    </picture>
  </a>
  <div>&nbsp;</div>
  <div align="center">
    <b><font size="5">Qbot website</font></b>
    <sup>
      <a href="https://ufund-me.github.io/Qbot/#/">
        <i><font size="4">HOT</font></i>
      </a>
    </sup>
    &nbsp;&nbsp;&nbsp;&nbsp;
    <b><font size="5">Qbot platform</font></b>
    <sup>
      <a href="https://ufund-me.github.io/Qbot/quantstats/docs/tearsheet.html">
        <i><font size="4">TRY IT OUT</font></i>
      </a>
    </sup>
  </div>
  <div>&nbsp;</div>
</div>

<div align="center">
  <p>AI驱动的自动化智能投研、智能投顾平台</p>
  <p>
    <b>Qbot</b> is an AI-oriented automated quantitative investment platform, which aims to realize the potential, <br>
  empower AI technologies in quantitative investment.
  </p>
</div>

```
🤖 Qbot = 智能交易策略 + 回测系统 + 自动化量化交易 (+ 可视化分析工具)
            |           |            |            |
            |           |            |             \_ quantstats (dashboard\online operate)
            |           |             \______________ Qbot - vnpy, pytrader, pyfunds
            |           \____________________________ BackTest - backtrader, easyquant
            \________________________________________ quant.ai - qlib, deep learning strategies
```

<br>

<div align="center">

  ***不建议 fork 项目，本项目会持续更新，只 fork 看不到更新，建议 Star ⭐️ ~***

  <i>喜欢这个项目吗？请考虑[ ❤️赞助](#sponsors--support) 本项目，以帮助改进！</i>

</div>

## Quick Start

```bash
cd ~ # $HOME as workspace
git clone https://github.com/UFund-Me/Qbot.git

cd Qbot
pip install -r requirements.txt

python main.py  #if run on Mac, please use 'pythonw main.py'
```

<p id="demo">
  <!-- <img width="" alt="demo" src="https://user-images.githubusercontent.com/29084184/221901048-bb1615fe-674f-40e8-b1e7-ba5db30a82a6.png"> -->
  <img width="" alt="demo" src="https://user-images.githubusercontent.com/29084184/223608757-5808e23c-86e4-4b1b-8b03-e04c8f368f5c.gif">
</p>

## Highlight

<table class="table table-striped table-bordered table-vcenter">
    <tbody class=ai-notebooks-table-content>
    <tr>
        <td colspan="3" rowspan="1" class="ai-notebooks-table-points ai-orange-link">
            <div class="features-2 mdl-grid">
                <h2 style="text-align:center">1. 多种交易方式：在线回测 + 模拟交易 + 实盘自动化交易</h2>
                <p>以策略研究为目标，提供多种交易方式验证策略和提高收益。</p>
            </div>
        </td>
    </tr>
    <tr>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" width="320" src="https://github.com/UFund-Me/Qbot/assets/29084184/222de589-a61f-4c45-bc5f-49de3fc2a72e"></img>
            </div>
        </td>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" width="320" src="https://user-images.githubusercontent.com/29084184/221901048-bb1615fe-674f-40e8-b1e7-ba5db30a82a6.png"/>
            </div>
        </td>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" width="320" src="https://github.com/UFund-Me/Qbot/assets/29084184/e96206ff-586a-4c6a-8f7a-cd578c8bdc43"/>
            </div>
        </td>
    </tr>
    </tbody>
</table>

<table class="table table-striped table-bordered table-vcenter">
    <tbody class=ai-notebooks-table-content>
    <tr>
        <td colspan="3" rowspan="1" class="ai-notebooks-table-points ai-orange-link">
            <div class="features-2 mdl-grid">
                <h2 style="text-align:center">2. 多种提示方式：邮件 + 飞书 + 弹窗 + 微信</h2>
                <p>这是qbot的消息提示模块，多种方式提示交易信息：交易买卖信息、每日交易收益结果、股票每日推荐等。</p>
            </div>
        </td>
    </tr>
    <tr>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" width="330" src="https://github.com/UFund-Me/Qbot/assets/29084184/aafff916-1945-4ae7-b836-60254ecacf76"></img>
            </div>
        </td>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" width="220" src="https://github.com/UFund-Me/Qbot/assets/29084184/a5cfadb5-8233-4307-ab79-6e0c0aca536d"/>
            </div>
        </td>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" width="330" height="150%" src="https://github.com/UFund-Me/Qbot/assets/29084184/beb5877b-e45e-45a8-afdb-1926ea2ea8a1"/>
            </div>
        </td>
    </tr>
    </tbody>
</table>

## USAGE ʕ •ᴥ•ʔ

### Installation

[Install Guide](./docs/01-新手指引/Install_guide.md) | [Online documents](https://ufund-me.github.io/Qbot/#/)

```
 ____________________________________
< Run ``./env_setup.sh`` to say hello >
 ------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
```

### Get Started

#### Local

```shell
export USER_ID="admin"                   # replace your info
export PASSWORD="admin1234."             # replace your info

pip install -r requirements.txt

cd  pytrader
python test_backtrade.py
python test_trader.py

# visualization
python main.py

# if run on Mac, please use 'pythonw main.py'

```

#### Web

- 1. 基金策略在线分析

需要 node 开发环境: `npm`、`node`，点击[查看](pyfunds/fund-strategies/README.md)详细操作文档

运行命令

```
cd pyfunds/fund-strategies

npm install
npm start
```

- 2. 选基、选股助手

运行命令

```
cd investool

./investool webserver
```

## No-code operation (TODO)

<img width="" alt="dagster" src="https://user-images.githubusercontent.com/29084184/221900050-2275a6e2-5c9b-4b81-84e5-0087e8fb58ec.png">

体验下来，dagster是很适合金融数据采集、处理，还有机器学习的场景。当然这里的场景更偏向于“批处理”，“定时任务”的处理与编排。

```
dagster-daemon run &
dagit -h 0.0.0.0 -p 3000
```
## Strategies 

部分未整理。。。

<div align="center">
  <b>经典策略</b>
</div>
<table align="center">
  <tbody>
    <tr align="center" valign="bottom">
      <td>
        <b>股票</b>
      </td>
      <td>
        <b>基金</b>
      </td>
      <td>
        <b>期货</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
      <ul>
        <li><a href="docs/02-经典策略/01-股票/布林线均值回归.md">布林线均值回归 ('2022)</a></li>
        <li><a href="docs/03-智能策略/">移动均线+KDJ</a></li>
        <li><a href="docs/02-经典策略/01-股票/多因子选股.md">多因子选股 ('2023)</a></li>
        <li><a href="docs/02-经典策略/01-股票/小市值.md">小市值 ('2021)</a></li>
        <li><a href="docs/02-经典策略/01-股票/指数增强.md">指数增强 ('2022)</a></li>
        <li><a href="docs/02-经典策略/01-股票/Alpha对冲.md">Alpha对冲 ('2022)</a></li>
        <li><a href="docs/02-经典策略/03-期货/网络交易.md">网格交易 ('2022)</a></li>
        <li><a href="docs/03-智能策略/拐点交易.md">拐点交易 ('2022)</a></li>
        <li><a href="docs/03-智能策略/">趋势交易</a></li>
        <li><a href="docs/03-智能策略/">海龟策略</a></li>
        <li><a href="docs/03-智能策略/">动态平衡策略</a></li>
        <li><a href="docs/03-智能策略/">阿隆指标策略</a></li>
      </ul>
      </td>
      <td>
      <ul>
        <li><a href="docs/02-经典策略/02-基金/4433法则.md">4433法则 ('2022)</a></li>
        <li><a href="docs/02-经典策略/02-基金/">对冲策略：指数型+债券型对冲</a></li>
        <li><a href="docs/02-经典策略/02-基金/">组合策略：多因子组合配置</a></li>
        <li><a href="docs/02-经典策略/02-基金/">组合策略：惠赢智能算法1</a></li>
        <li><a href="docs/02-经典策略/02-基金/">组合策略：择时多策略</a></li>
        <li><a href="docs/02-经典策略/02-基金/">组合策略：智赢多因子1</a></li>
      </ul>
      </td>
      <td>
      <ul>
        <li><a href="docs/02-经典策略/03-期货/双均线策略.md">双均线策略 ('2022)</a></li>
        <li><a href="docs/02-经典策略/03-期货/网络交易.md">网格交易 ('2022)</a></li>
      </ul>
      </td>
    </tr>
  </tbody>
</table>

<div align="center">
  <b>智能策略</b>
</div>
<table align="center">
  <tbody>
    <tr align="center" valign="middle">
      <td>
        <b>GBDT</b>
      </td>
      <td>
        <b>RNN</b>
      </td>
      <td>
        <b>Reinforcement Learning</b>
      </td>
      <td>
        <b>:fire: Transformer</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
        <li><b>GBDT</b></li>
        <ul>
            <li><a href="pytrader/strategies/benchmarks/XGBoost">XGBoost (KDD'2016)</a></li>
            <li><a href="pytrader/strategies/benchmarks/LightGBM">LightGBM (NIPS'2017)</a></li>
            <li><a href="">Catboost (NIPS'2018)</a></li>
        </ul>
        <li><b>BOOST</b></li>
        <ul>
            <li><a href="">DoubleEnsemble (ICDM'2020)</a></li>
            <li><a href="">TabNet (ECCV'2022)</a></li>
        </ul>
        <li><b>LR</b></li>
        <ul>
            <li><a href="pytrader/strategies/benchmarks/Linear"> Line Regression ('2020)</a></li>
        </ul>
      </td>
      <td>
        <li><b>CNN</b></li>
        <ul>
          <li><a href="pytrader/strategies/benchmarks/MLP">MLP (CVPRW'2020)</a></li>
          <li><a href="">GRU (ICCVW'2021)</a></li>
          <li><a href="">ImVoxelNet (WACV'2022)</a></li>
          <li><a href="">TabNet (AAAI'2019)</a></li>
        </ul>
        <li><b>RNN</b></li>
        <ul>
          <li><a href="pytrader/strategies/benchmarks/LSTM">LSTM (Neural Computation'2017)</a></li>
          <li><a href="">ALSTM (IJCAI'2022)</a></li>
          <li><a href="">ADARNN (KDD'2021)</a></li>
          <li><a href="">ADD (CoRL'2020)</a></li>
        </ul>
      </td>
      <td>
          <li><a href="pytrader/strategies/benchmarks/TFT">TFT (IJoF'2019)</a></li>
          <li><a href="">GATs (NIPS'2017)</a></li>
          <li><a href="">SFM (KDD'2017)</a></li>
      </td>
      <td>
          <li><a href="pytrader/strategies/benchmarks/Transformer">Transformer (NeurIPS'2017)</a></li>
          <li><a href="">TCTS (ICML'2021)</a></li>
          <li><a href="">TRA (KDD'2021)</a></li>
          <li><a href="">TCN (KDD'2018)</a></li>
          <li><a href="">IGMTF (KDD'2021)</a></li>
          <li><a href="">HIST (KDD'2018)</a></li>
          <li><a href="">Localformer ('2021)</a></li>
      </td>
    </tr>
</td>
    </tr>
  </tbody>
</table>

### Benchmark and Model zoo

Results and models are available in the [model zoo](docs/03-智能策略/model_zoo.md). AI strategies is shown at [here](./pytrader/strategies/), local run ``python pytrader/strategies/workflow_by_code.py``, also provide [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UFund-Me/Qbot/blob/main/pytrader/strategies/workflow_by_code.ipynb/HEAD)

<details><summary><em><b>点击展开查看具体AI模型benchmark结果</b></em></summary>

|                | status | benchmark |   framework  | DGCNN | RegNetX | addition |   arXiv    |
|  :-----------: | :----: | :--------:|   :----:     | :---: | :-----: | :------: | :--------: |
|     GBDT       |   ✗    |     ✗     |   XGBoost    |   ✗   |    ✗    |  Tianqi Chen, et al. KDD 2016 |     ✗      |
|     GBDT       |   ✗    |     ✗     |   LightGBM   |   ✗   |    ✓    |  Guolin Ke, et al. NIPS 2017 |     ✗      |
|     GBDT       |   ✗    |     ✗     |   Catboost   |   ✗   |    ✓    |  Liudmila Prokhorenkova, et al. NIPS 2018 |     ✗      |
|     MLP        |   ✓    |     ✓     |   pytorch    |   ✗   |    ✗    |  --      |     ✗      |
|     LSTM       |   ✓    |     ✓     |   pytorch    |   ✗   |    ✗    |  Sepp Hochreiter, et al. Neural computation 1997 |  ✗  |
|    LightGBM    |   ✓    |     ✓     |   pytorch    |   ✗   |    ✗    |  --      |     ✗      |
|     GRU        |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Kyunghyun Cho, et al. 2014 |     ✗      |
|     ALSTM      |   ✗    |     ✗     |   pytorch    |   ✗   |    ✗    |  Yao Qin, et al. IJCAI 2017 |     ✗      |
|     GATs       |   ✗    |     ✓     |   pytorch    |   ✗   |    ✗    |  Petar Velickovic, et al. 2017 |     ✗      |
|     SFM        |   ✓    |     ✓     |   pytorch    |   ✗   |    ✗    |  Liheng Zhang, et al. KDD 2017 |     ✗      |
|     TFT        |   ✓    |     ✓     |   tensorflow |   ✗   |    ✗    |  Bryan Lim, et al. International Journal of Forecasting 2019 | ✗ |
|     TabNet     |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Sercan O. Arik, et al. AAAI 2019 |     ✗      |
| DoubleEnsemble |   ✓    |     ✓     |   LightGBM   |   ✗   |    ✗    |  Chuheng Zhang, et al. ICDM 2020 |     ✗      |
|     TCTS       |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Xueqing Wu, et al. ICML 2021 |     ✗      |
|  Transformer   |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Ashish Vaswani, et al. NeurIPS 2017 |     ✗      |
|  Localformer   |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Juyong Jiang, et al. |     ✗      |
|     TRA        |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Hengxu, Dong, et al. KDD 2021 |     ✗      |
|     TCN        |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Shaojie Bai, et al. 2018 |     ✗      |
|     ADARNN     |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  YunTao Du, et al. 2021 |     ✗      |
|     ADD        |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Hongshun Tang, et al.2020 |     ✗      |
|     IGMTF      |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Wentao Xu, et al.2021 |     ✗      |
|     HIST       |   ✓    |     ✗     |   pytorch    |   ✗   |    ✗    |  Wentao Xu, et al.2021 |     ✗      |


<sup>**Note:** All the about **300+ models, methods of 40+ papers** in quant.ai supported by [Model Zoo](./docs/03-智能策略/model_zoo.md) can be trained or used in this codebase.</sup>

</details>

## 策略原理及源码分析

[在线文档](https://ufund-me.github.io/Qbot/#/) | [❓ 常见问题](https://ufund-me.github.io/Qbot/#/04-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/FQA) | [Jupyter Notebook](./pytrader/strategies/notebook)

## Quantstats Report

![Quantstats Report](https://user-images.githubusercontent.com/29084184/207054856-44d1815b-f92f-40a7-b82e-e4a6b3960f2f.png)

Click [HERE](quantstats#visualize-stock-performance) to more detail.

### Some strategy backtest results:

> 声明：别轻易用于实盘，市场有风险，投资需谨慎。

```
symbol：华正新材(603186)
Starting Portfolio Value: 10000.00
Startdate=datetime.datetime(2010, 1, 1),
Enddate=datetime.datetime(2020, 4, 21),
# 设置佣金为0.001, 除以100去掉%号
cerebro.broker.setcommission(commission=0.001)
```
    
A股回测MACD策略:

![MACD](pytrader/doc/02.easy_macd_strategy/Figure_macd.png)

![image](https://github.com/UFund-Me/Qbot/assets/29084184/dfef65ba-0d32-4f5f-b413-d6ec02fc700e)

👉 点击[查看](pytrader/doc/02.easy_macd_strategy/macd.py)源码

A股回测KDJ策略:

![KDJ](pytrader/doc/04.kdj_with_macd/Figure_kdj.png)
    
![image](https://github.com/UFund-Me/Qbot/assets/29084184/ef8e945b-59d6-4220-87e3-08ec1196cc2c)

👉 点击[查看](pytrader/doc/04.kdj_with_macd/kdj.py)源码

A股回测 KDJ+MACD 策略:

![KDJ with MACD](pytrader/doc/04.kdj_with_macd/Figure_kdj_with_macd.png)

![image](https://github.com/UFund-Me/Qbot/assets/29084184/67338ec5-a6b1-4aa7-9792-1a2c61f353da)

👉 点击[查看](pytrader/doc/04.kdj_with_macd/kdj_macd.py)源码

## TODO

- [x] 把策略回测整合在一个上位机中，包括：选基、选股策略、交易策略，模拟交易，实盘交易
- [ ] 很多策略需要做回测验证；
- [ ] 本项目由前后端支持，有上位机app支持，但目前框架还比较乱，需要做调整；
- [ ] 各种策略需要抽象设计，支持统一调用；
- [ ] 增强数据获取的实时性，每秒数据，降低延迟；
- [ ] 在线文档的完善，目前主要几个部分：新手使用指引、经典策略原理和源码、智能策略原理和源码、常见问题等；
- [ ] 新的feature开发，欢迎在[issues](https://github.com/UFund-Me/Qbot/issues/)交流；

## Contributing

We appreciate all contributions to improve Qbot. Please refer to [CONTRIBUTING.md](.github/CONTRIBUTING.md) for the contributing guideline.

## 🍮 Community
- Github <a href="https://github.com/UFund-Me/Qbot/discussions" target="_blank">discussions 💬</a> or <a href="https://github.com/UFund-Me/Qbot/issues" target="_blank">issues 💭</a>

- 微信: Yida_Zhang2
- Email: yidazhang1#gmail.com 
- 知乎：[@Charmve](https://www.zhihu.com/people/MaiweiE-com)

<br>

- 知识星球：AI量化投资 （加我微信，邀请）


## :warning: Disclaimer

交易策略和自动化工具只是提供便利，并不代表实际交易收益。该项目任何内容不构成任何投资建议。市场有风险，投资需谨慎。

## 🔥 Stargazers Over Time
	
<!-- [![Stargazers over time](https://starchart.cc/UFund-Me/Qbot.svg)](https://starchart.cc/UFund-Me/Qbot) -->

[![Star History Chart](https://api.star-history.com/svg?repos=UFund-Me/Qbot,ailabx/ailabx,jadepeng/pytrader&type=Timeline)](https://star-history.com/#UFund-Me/Qbot&ailabx/ailabx&jadepeng/pytrader&Timeline)
    
## Sponsors & support

If you like the project, you can become a sponsor at [Open Collective](https://opencollective.com/qbot) or use [GitHub Sponsors](https://github.com/sponsors/Charmve).

<b>Thank you for supporting Qbot!</b>

<a href="https://opencollective.com/qbot" target="_blank"><img src="https://opencollective.com/Qbot/tiers/sponsors.svg?avatarHeight=120" alt="Sponsor"></a>
<a href="https://opencollective.com/qbot#category-CONTRIBUTE" target="_blank"><img src="https://opencollective.com/qbot/tiers/backers.svg?avatarHeight=32"/></a>

<b>Last but not least, we're thankful to these open-source repo for sharing their services for free:</b>

基于Backtrader、vnpy、qlib、tushare、backtest、easyquant等开源项目，感谢开发者。

<br><br>

感谢大家的支持与喜欢！

Code with ❤️ & ☕️ @Charmve 2022-2023
