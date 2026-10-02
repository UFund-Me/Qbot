## Waking-Up

> 大多数人都高估了他们一天能做的事情，但低估了他们一年能做的事情。

> NOTE
> - [tutorials code](./tutorials_code)


<br>

<h2> <img src="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" width="42"/> 🤖 Qbot </h2>

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
      <a href="https://ufund-me.github.io/Qbot/quantstats/tearsheet.html">
        <i><font size="4">TRY IT OUT</font></i>
      </a>
    </sup>
  </div>
  <div>&nbsp;</div>
</div>

<div align="center">
  <p>AI智能量化投研平台</p>
</div>

>  <b>Qbot</b> is an AI-oriented automated quantitative investment platform, which aims to realize the potential, empower AI technologies in quantitative investment. Qbot supports diverse machine learning modeling paradigms. including supervised learning, market dynamics modeling, and RL.

<p id="demo">
  <!-- <img width="" alt="demo" src="https://user-images.githubusercontent.com/29084184/221901048-bb1615fe-674f-40e8-b1e7-ba5db30a82a6.png"> -->
  <img width="" alt="demo" src="https://user-images.githubusercontent.com/29084184/223608757-5808e23c-86e4-4b1b-8b03-e04c8f368f5c.gif">
</p>

```
🤖 Qbot = 智能交易策略 + 回测系统 + 自动化量化交易 (+ 可视化分析工具)
            |           |            |            |
            |           |            |             \_ quantstats (dashboard\online operation)
            |           |             \______________ Qbot - vnpy, pytrader, pyfunds
            |           \____________________________ BackTest - backtrader, easyquant
            \________________________________________ quant.ai - qlib, deep learning strategies
```

<br>

<div align="center">
  
  🎺 <b>号外</b>：Qbot微信小程序开发招募 [UFund-miniprogram](https://github.com/UFund-Me/UFund-miniprogram)

  <b>不建议 fork 项目，本项目会持续更新，只 fork 看不到更新，建议 Star ⭐️ ~</b>

  <i>喜欢这个项目吗？请考虑[ ❤️赞助](#sponsors--support) 本项目，以帮助改进！</i>

</div>

## Quick Start

Qbot是一个免费的量化投研平台，提供从数据获取、交易策略开发、策略回测、模拟交易到最终实盘交易的全闭环流程。在实盘接入前，有股票、基金评测和策略回测，在模拟环境下做交易验证，近乎实盘的时延、滑点仿真。故，本平台提供GUI前端/客户端（部分功能也支持网页），后端做数据处理、交易调度，实现事件驱动的交易流程。对于策略研究部分，尤其强调机器学习、强化学习的AI策略，结合多因子模型提高收益比。

但本项目可能需要一点点python基础知识，有一点点交易经验，会更容易体会作者的初衷，解决当下产品空缺和广大散户朋友的交易痛点，现在直接免费开源出来！

```bash
cd ~ # $HOME as workspace
git clone https://github.com/UFund-Me/Qbot --depth 1

cd Qbot
pip install -r requirements.txt

export PYTHONPATH=${PYTHONPATH}:$(pwd)
python main.py  #if run on Mac, please use 'pythonw main.py'

```

详细文档 https://github.com/UFund-Me/Qbot/blob/main/quick_start.md

> [!NOTE]
> - wxPython、Ta-Lib 需要手动安装，pip wheel 在 dev/ 路径下。https://github.com/UFund-Me/Qbot/issues/76
> - <details><summary>Mac系统在安装之前需要手动安装tables库的依赖hdf5，以及pythonw https://github.com/UFund-Me/Qbot/issues/11 </summary>
> <code>
>   brew install hdf5
>   brew install c-blosc
>   export HDF5_DIR=/opt/homebrew/opt/hdf5 
>   export BLOSC_DIR=/opt/homebrew/opt/c-blosc
> </code>
> </details>

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/UFund-Me/Qbot)

<!-- ![Gitpod-Ready](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod) -->

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
                <img class="illustration_img" src="https://github.com/UFund-Me/Qbot/assets/29084184/aafff916-1945-4ae7-b836-60254ecacf76"></img>
            </div>
        </td>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" src="https://github.com/UFund-Me/Qbot/assets/29084184/a5cfadb5-8233-4307-ab79-6e0c0aca536d"/>
            </div>
        </td>
        <td>
            <div class="mdl-cell mdl-cell--4-col">
                <img class="illustration_img" src="https://github.com/UFund-Me/Qbot/assets/29084184/beb5877b-e45e-45a8-afdb-1926ea2ea8a1"/>
            </div>
        </td>
    </tr>
    </tbody>
</table>

## USAGE ʕ •ᴥ•ʔ

### Installation

[Install Guide](https://github.com/UFund-Me/Qbot/blob/main/docs/01-新手指引/Install_guide) | [Online documents](https://ufund-me.github.io/Qbot/#/)

### Get Started

本项目分为前端（客户端）和后端两部分，前端由wxPython编写的轻量化GUI客户端，后端分为策略开发、策略回测 ``qbot/strategies``、股票基金评测、模拟交易、在线回测几个部分，对应于客户端从左到右的三个菜单。

➕ 请注意：本项目建议使用python 3.8、3.9版本，推荐使用conda搭建环境，参考 [Install Guide](https://github.com/UFund-Me/Qbot/blob/main/docs/01-新手指引/Install_guide)。

<sub>* 如果是 Win 系统使用``set``命令.</sub>

```shell
git clone https://github.com/UFund-Me/Qbot --depth 1
cd Qbot
pip install -r requirements.txt

# if run on Mac, please use 'pythonw main.py'
python main.py
```

> [!NOTE]
> wxPython、Ta-Lib 需要手动安装，pip wheel 在 dev/ 路径下。https://github.com/UFund-Me/Qbot/issues/76

主要包含四个窗口，如果启动界面未显示或有问题可以参考下图中对应的启动方式。👉 点击[这里](https://github.com/UFund-Me/Qbot/blob/main/gui/mainframe.py#L122-L141)查看源码，下文也有文字介绍。

![image](https://github.com/UFund-Me/Qbot/assets/29084184/9f1dcc07-ca76-4600-a02c-76104fb28c51)

## Strategy pool

通过Qbot 可以积木式完成策略编写、多因子挖掘，实现数据开发、因子开发、组合优化、交易执行的[量化交易全流程](01-新手指引/量化策略的分类和原理.md#1量化选股策略)。

<b>如果说策略是量化的核心 ，那么因子就是策略的核心。</b>通过Qbot量化投研平台研究员可实现自动化因子挖掘，提取出具备预测能力的单因子，利用历史数据进行回测，如果回测结果显示该因子的预测能力达标，就提交到因子库。然后，对因子库里的因子进行有机组合，以形成预测模型，预测模型是整个量化策略的目标。

以下即为，<u>数据指标单因子或组合因子</u>和<u>通过深度学习、机器学习、强化学习挖掘到的交易因子</u>，然后通过组合优化算法实现趋势交易、风险策略、alpha策略、动量轮动等等交易策略。

策略库源代码路径：[qbot/strategies](../qbot/strategies)、[pytrader/strategies](../pytrader/strategies)


<div align="center">
  <b>经典策略</b>
</div>
<table align="center">
  <tbody>
    <tr align="center" valign="bottom">
      <td>
        <b>交易对象</b>
      </td>
      <td>
        <b>选股</b>
      </td>
      <td>
        <b>择时</b>
      </td>
      <td>
        <b>风险控制 (组合、仓位管理)</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
        <b>股票/期货/虚拟货币</b>
      </td>
      <td>
        <ul>
          <li><a href="02-经典策略/01-股票/布林线均值回归.md">布林线均值回归 ('2022)</a></li>
          <li><a href="tutorials_code/05.kdj_macd_in_A_market">移动均线+KDJ</a></li>
          <li><a href="../qbot/strategies/bigger_than_ema_bt.py">简单移动均线</a></li>
          <li><a href="../qbot/strategies/arbr_strategy.py">情绪指标ARBR</a></li>
          <li><a href="../pytrader/strategies/aroon_strategy.py">阿隆指标(趋势交易)</a></li>
          <li><a href="../pytrader/strategies/lgb_strategy.py">LightGBM 预测</a></li>
          <li><a href="../pytrader/strategies/svm_strategy.py">SVM 预测</a></li>
          <li><a href="../qbot/strategies/lstm_strategy_bt.py">LSTM时序预测</a></li>
          <li><a href="../qbot/strategies/rl_strategy_bt.py">强化学习预测</a></li>
          <li><a href="../pytrader/strategies/q-learning.py">Q-Leaning预测</a></li>
          <li><a href="tutorials_code/11_RandomForest">随机森林预测</a></li>
          <li><a href="../pytrader/strategies/rsi_departure_strategy.py">RSI背离策略</a></li>
          <li><a href="../qbot/strategies/ssa_strategy_bt.py">麻雀优化算法SSA</a></li>
          <li><a href="../pytrader/strategies/StochRSI.py">随机相对强弱指数 StochRSI</a></li>
          <li><a href="02-经典策略/01-股票/小市值.md">小市值 ('2021)</a></li>
          <li><a href="../qbot/strategies/undervalued_stock_picking_strategy.py">市场低估值策略</a></li>
          <li><a href="02-经典策略/01-股票/量化策略-RSRS择时.md">RSRS择时</a></li>
          <li><a href="02-经典策略/01-股票/量化三-配对交易.md">配对交易</a></li>
        </ul>
      </td>
      <td>
        <li><b>传统指标（对应下方Qbot支持的指标 <a href="#交易指标因子">这里</a>）</b></li>
        <ul>
          <li><a href="02-经典策略/01-股票/布林线均值回归.md">布林线均值回归 ('2022)</a></li>
          <li><a href="tutorials_code/05.kdj_macd_in_A_market">移动均线+KDJ</a></li>
          <li><a href="../qbot/strategies/bigger_than_ema_bt.py">简单移动均线</a></li>
          <li><a href="../qbot/strategies/klines_bt.py">双均线策略 ('2022)</a></li>
          <li><a href="../qbot/strategies/arbr_strategy.py">情绪指标ARBR</a></li>
          <li><a href="../pytrader/strategies/aroon_strategy.py">阿隆指标(趋势交易)</a></li>
          <li><a href="../pytrader/strategies/lgb_strategy.py">LightGBM 预测</a></li>
          <li><a href="../pytrader/strategies/svm_strategy.py">SVM 预测</a></li>
          <li><a href="../qbot/strategies/lstm_strategy_bt.py">LSTM时序预测</a></li>
          <li><a href="../qbot/strategies/rl_strategy_bt.py">强化学习预测</a></li>
          <li><a href="../pytrader/strategies/q-learning.py">Q-Leaning预测</a></li>
          <li><a href="tutorials_code/11_RandomForest">随机森林预测</a></li>
          <li><a href="../pytrader/strategies/rsi_departure_strategy.py">RSI背离策略</a></li>
          <li><a href="../qbot/strategies/ssa_strategy_bt.py">麻雀优化算法SSA</a></li>
          <li><a href="../pytrader/strategies/StochRSI.py">随机相对强弱指数 StochRSI</a></li>
        </ul>
        <li><b>因子组合</b></li>
        <ul>
          <li><a href="../pytrader/strategies/CCI.py">RSI和CCI组合</a></li>
          <li><a href="../qbot/strategies/adx_strategy.py">MACD和ADX指标</a></li>
          <li><a href="tutorials_code/05.kdj_macd_in_A_market">MACD和KDJ指标</a></li>
          <li><a href="../qbot/strategies/multi_strategy_bt.py">多因子交易</a></li>
          <li><a href="tutorials_code/13.alphalens_factor_backtest">alphalens多因子交易</a></li>
          <li><a href="tutorials_code/08.harami_in_A_market">多策略整合</a></li>
          <li><a href="notebook/Kurtosis Portfolio.ipynb">组合策略</a></li>
          <li><a href="02-经典策略/01-股票/指数增强.md">指数增强 ('2022)</a></li>
        </ul>
        <li><b>经典策略</b></li>
        <ul>
          <li><a href="02-经典策略/01-股票/多因子选股.md">多因子选股 ('2023)</a></li>
          <li><a href="02-经典策略/01-股票/指数增强.md">指数增强 ('2022)</a></li>
          <li><a href="02-经典策略/01-股票/Alpha对冲.md">Alpha对冲 ('2022)</a></li>
          <li><a href="02-经典策略/03-期货/网络交易.md">网格交易</a></li>
          <li><a href="02-经典策略/03-期货/双均线策略.md">双均线策略 ('2022)</a></li>
          <li><a href="03-智能策略/拐点交易.md">拐点交易 ('2022)</a></li>
          <li><a href="03-智能策略/">趋势交易</a></li>
          <li><a href="03-智能策略/">海龟策略</a></li>
          <li><a href="03-智能策略/">动态平衡策略</a></li>
        </ul>
      </td>
      <td>
        <ul>
          <li><a href="notebook/Kurtosis Portfolio.ipynb">Kurtosis Portfolio组合策略 ('2023)</a></li>
          <li><a href="02-经典策略/01-股票/指数增强.md">指数增强 ('2022)</a></li>
          <li><a href="02-经典策略/01-股票/Alpha对冲.md">Alpha对冲 ('2022)</a></li>
          <li><a href="03-智能策略/">动态平衡策略</a></li>
          <li><a href="../pytrader/strategies/multi_factor_strategy.py">多因子自动组合策略</a></li>
        </ul>
      </td>
      <tr valign="top">
        <td>
          <b>基金</b>
        </td>
        <td>
          <ul>
            <li><a href="02-经典策略/02-基金/4433法则.md">4433法则 ('2022)</a></li>
          </ul>
        </td>
        <td>
          <ul>
            <li><a href="02-经典策略/02-基金/">对冲策略：指数型+债券型对冲</a></li>
            <li><a href="02-经典策略/02-基金/">组合策略：多因子组合配置</a></li>
            <li><a href="02-经典策略/02-基金/">组合策略：惠赢智能算法1</a></li>
            <li><a href="02-经典策略/02-基金/">组合策略：择时多策略</a></li>
            <li><a href="02-经典策略/02-基金/">组合策略：智赢多因子1</a></li>
          </ul>
        </td>
        <td>
          <b>同上</b>
        </td>
      </tr>
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
      <td>
        <b>:fire: LLM</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
        <li><b>GBDT</b></li>
        <ul>
            <li><a href="../pytrader/strategies/benchmarks/XGBoost">XGBoost (KDD'2016)</a></li>
            <li><a href="../pytrader/strategies/benchmarks/LightGBM">LightGBM (NIPS'2017)</a></li>
            <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/CatBoost">Catboost (NIPS'2018)</a> <sup>qlib</sup></li>
        </ul>
        <li><b>BOOST</b></li>
        <ul>
            <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/DoubleEnsemble">DoubleEnsemble (ICDM'2020)</a> <sup>qlib</sup></li>
            <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TabNet">TabNet (ECCV'2022)</a> <sup>qlib</sup></li>
        </ul>
        <li><b>LR</b></li>
        <ul>
            <li><a href="../pytrader/strategies/benchmarks/Linear"> Line Regression ('2020)</a></li>
        </ul>
      </td>
      <td>
        <li><b>CNN</b></li>
        <ul>
          <li><a href="../pytrader/strategies/benchmarks/MLP">MLP (CVPRW'2020)</a></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/GRU">GRU (ICCVW'2021)</a> <sup>qlib</sup></li>
          <li>ImVoxelNet (WACV'2022) <sup>未包含</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TabNet">TabNet (AAAI'2019)</a> <sup>qlib</sup></li>
        </ul>
        <li><b>RNN</b></li>
        <ul>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/LSTM">LSTM (Neural Computation'2017)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/ALSTM">ALSTM (IJCAI'2022)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/ADARNN">ADARNN (KDD'2021)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/ADD">ADD (CoRL'2020)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/KRNN">KRNN ()</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/Sandwich">Sandwich ()</a> <sup>qlib</sup></li>
        </ul>
      </td>
      <td>
          <li><a href="../pytrader/strategies/benchmarks/TFT">TFT (IJoF'2019)</a></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/GATs">GATs (NIPS'2017)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/SFM">SFM (KDD'2017)</a> <sup>qlib</sup></li>
      </td>
      <td>
          <li><a href="../pytrader/strategies/benchmarks/Transformer">Transformer (NeurIPS'2017)</a></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TCTS">TCTS (ICML'2021)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TRA">TRA (KDD'2021)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TCN">TCN (KDD'2018)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/IGMTF">IGMTF (KDD'2021)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/HIST">HIST (KDD'2018)</a> <sup>qlib</sup></li>
          <li><a href="https://github.com/microsoft/qlib/tree/main/examples/benchmarks/Localformer">Localformer ('2021)</a> <sup>qlib</sup></li>
      </td>
      <td>
          <li><a href="https://chat-gpt-next-web-five-puce-64.vercel.app/">ChatGPT</a></li>
          <li><a href="https://github.com/UFund-Me/FinGPT">FinGPT</a></li>
      </td>
    </tr>
</td>
    </tr>
  </tbody>
</table>

> 注：标有 <sup>qlib</sup> 的模型未包含在本仓库中，链接指向 [microsoft/qlib](https://github.com/microsoft/qlib/tree/main/examples/benchmarks) 上游 benchmark；标有 <sup>未包含</sup> 的模型暂无实现。本仓库自带的模型位于 [pytrader/strategies/benchmarks](../pytrader/strategies/benchmarks)。

### Benchmark and Model zoo

Results and models are available in the [model zoo](03-智能策略/model_zoo.md). AI strategies is shown at [here](../pytrader/strategies/), local run ``python pytrader/strategies/workflow_by_code.py``, also provide [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UFund-Me/Qbot/HEAD?labpath=pytrader%2Fstrategies%2Fworkflow_by_code.ipynb)

<details><summary><em><b>👉 点击展开查看具体AI模型benchmark结果</b></em></summary>

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


<sup>**Note:** All the about **300+ models, methods of 40+ papers** in quant.ai supported by [Model Zoo](./03-智能策略/model_zoo.md) can be trained or used in this codebase.</sup>

</details>

<br>

### 交易指标/因子

包含但不限于alpha-101、alpha-191，以及基于deap实现的因子自动生成算法。
```
EMA(简单移动均线)
MACD(指数平滑异同平均线)
KDJ(随机指标)
RSRS(阻力支撑相对强度)
RSI(相对强弱指标)
StochRSI(随机相对强弱指数)
BIAS(乖离率)
BOLL(布林线指标)
OBV(能量潮)
SAR(抛物转向)
VOL(成交量)
PSY(心理线)
ARBR(人气和意愿指标)
CR(带状能力线)
BBI(多空指标)
EMV(简易波动指标)
TRIX(三重指数平滑移动平均指标)
DMA(平均线差)
DMI(趋向指标)
CCI(顺势指标)
ROC(变动速率指标, 威廉指标)
ENE(轨道线)  # 轨道线（ENE）由上轨线(UPPER)和下轨线(LOWER)及中轨线(ENE)组成，
            # 轨道线的优势在于其不仅具有趋势轨道的研判分析作用，也可以敏锐的觉察股价运行过程中方向的改变
SKDJ(慢速随机指标)
LWR(慢速威廉指标)  # 趋势判断指标
市盈率
市净率
主力意愿(收费)
买卖差(收费)
散户线(收费)
分时博弈(收费)
买卖力道(收费)
行情趋势(收费)
MTM(动量轮动指标)(收费)
MACD智能参数(收费)
KDJ智能参数(收费)
RSI智能参数(收费)
WR智能参数(收费)
Qbot智能预测(收费)
Qbot买卖强弱指标(收费)
```

<br>

## 支持的实盘交易接口
### 实盘交易接口()
> 欢迎更多交易所、柜台开放交易api

- 期货
  - CTP
  - CTPMini
  - 飞马Femas
  - 艾克朗科（仅组播行情）
  - 易达
- 期权
  - CTPOpt
  - 金证期权maOpt
  - QWIN二开
- 股票
  - 中泰XTP
  - 中泰XTPXAlgo
  - 华鑫奇点
  - 华锐ATP
  - 宽睿OES
  - 同花顺
  - 东方财富
  - 华泰证券
  - 国泰君安
  - 中汇亿达
  - 恒生UFT
  - 掘金
  - 顶点飞创
  - 华鑫奇点
  - 通达信
- 虚拟货币/数字货币
  - 欧易OKEX
  - 币安Bianace
  - 火币Huobi

### 仿真交易接口/平台

| API  |  交易类型  |  操作系统   |
| ---- |    ---    |       --- |
| qbot_pro | 股票、期货、基金、虚拟货币 | Win、Linux、Mac|
| [掘金仿真](https://sim.myquant.cn/sim/help/#%E4%B8%8B%E8%BD%BD%E4%BA%A4%E6%98%93sdk)  | 股票、基金、期货 | Win、Linux、Mac |
| 极星量化  | 期货 | Win、Mac |
| WonderTrader | 股票、期货 | Win、Linux |
| TradingView | 虚拟货币 | Win、Linux、Mac|
| 欧易OKEX、币安 Binance 、火币huobi | 虚拟货币 | Win、Linux、Mac|

## 虚拟货币交易所注册推荐码

- OKEX 交易所注册推荐码, 手续费返佣 **20%**
  - https://www.cnouyi.social/join/57246734

- 币安交易所注册推荐码, 手续费返佣 **10%**
  - https://accounts.binance.com/register?ref=130173909

- 火币交易所注册推荐码, 手续费返佣 **15%** (推荐)
  - https://www.htx.com/invite/zh-cn/1f?invite_code=wr938223


<br>

## 开源共创、社区共建

首先，感谢自今年5月份开源以来收到广大用户的关注！我们在基础版本中开放了很多传统量化策略、深度学习、强化学习等人工智能策略和多因子库，为此，我们发起《Qbot人工智能量化交易社区共建计划》。采取以下两种方式共建共赢：

1. 内容共建：

- 在我们免费提供的<b>人工智能交易策略</b>基础上，提高SOTA指标，然后以个人所有权提交Qbot量化交易社区，作为一种策略服务提供给更多人，获取收益；
- 在我们免费提供的<b>上千个交易因子</b>基础上，应用交易因子完成策略回测、模拟交易，对交易结果好的可作为一种交易策略服务提供给更多人，获取收益；

2. 代码贡献：

- 参与本代码仓库程序设计与实现，多提交PR合并后可免费加入知识星球；
- 贡献榜单前10名可获得一年免费使用权，前3名可获得qbot进阶版终身免费使用权；

## 策略原理及源码分析

本项目编写了详细的策略原理说明和平台搭建到使用的详细文档，尤其适合量化小白。欢迎加群交流！

[在线文档](https://ufund-me.github.io/Qbot/#/) | [❓ 常见问题](https://ufund-me.github.io/Qbot/#/04-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/FQA) | [Jupyter Notebook](../pytrader/strategies/notebook)

## Quantstats Report

![Quantstats Report](https://user-images.githubusercontent.com/29084184/207054856-44d1815b-f92f-40a7-b82e-e4a6b3960f2f.png)

Click [HERE](https://github.com/UFund-Me/Qbot/blob/main/quantstats#visualize-stock-performance) to more detail.

#### Some strategy backtest results:

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

![MACD](https://raw.githubusercontent.com/UFund-Me/Qbot/main/pytrader/doc/02.easy_macd_strategy/Figure_macd.png)

![image](https://github.com/UFund-Me/Qbot/assets/29084184/dfef65ba-0d32-4f5f-b413-d6ec02fc700e)

👉 点击[查看](https://github.com/UFund-Me/Qbot/blob/main/pytrader/doc/02.easy_macd_strategy/macd.py)源码

A股回测KDJ策略:

![KDJ](https://raw.githubusercontent.com/UFund-Me/Qbot/main/pytrader/doc/04.kdj_with_macd/Figure_kdj.png)
    
![image](https://github.com/UFund-Me/Qbot/assets/29084184/ef8e945b-59d6-4220-87e3-08ec1196cc2c)

👉 点击[查看](https://github.com/UFund-Me/Qbot/blob/main/pytrader/doc/04.kdj_with_macd/kdj.py)源码

A股回测 KDJ+MACD 策略:

![KDJ with MACD](https://raw.githubusercontent.com/UFund-Me/Qbot/main/pytrader/doc/04.kdj_with_macd/Figure_kdj_with_macd.png)

![image](https://github.com/UFund-Me/Qbot/assets/29084184/67338ec5-a6b1-4aa7-9792-1a2c61f353da)

👉 点击[查看](https://github.com/UFund-Me/Qbot/blob/main/pytrader/doc/04.kdj_with_macd/kdj_macd.py)源码

## TODO

- [x] 把策略回测整合在一个上位机中，包括：选基、选股策略、交易策略，模拟交易，实盘交易
- [ ] 很多策略需要做回测验证；
- [ ] 本项目由前后端支持，有上位机app支持，但目前框架还比较乱，需要做调整；
- [ ] 各种策略需要抽象设计，支持统一调用；
- [ ] 增强数据获取的实时性，每秒数据，降低延迟；
- [ ] 在线文档的完善，目前主要几个部分：新手使用指引、经典策略原理和源码、智能策略原理和源码、常见问题等；
- [ ] 新的feature开发，欢迎在[issues](https://github.com/UFund-Me/Qbot/issues/)交流；

## No-code operation (TODO)

<img width="" alt="dagster" src="https://user-images.githubusercontent.com/29084184/221900050-2275a6e2-5c9b-4b81-84e5-0087e8fb58ec.png">

体验下来，dagster是很适合金融数据采集、处理，还有机器学习的场景。当然这里的场景更偏向于“批处理”，“定时任务”的处理与编排。

```
cd plugins/dagster
dagster-daemon run &
dagit -h 0.0.0.0 -p 3000
```

## Contributing

We appreciate all contributions to improve Qbot. Please refer to [CONTRIBUTING](../.github/CONTRIBUTING.md) for the contributing guideline.

## 🍮 Community
- Github <a href="https://github.com/UFund-Me/Qbot/discussions" target="_blank">discussions 💬</a> or <a href="https://github.com/UFund-Me/Qbot/issues" target="_blank">issues 💭</a>

- 微信: Yida_Zhang2
- Email: yidazhang1#gmail.com 
- 知乎：[@Charmve](https://www.zhihu.com/people/MaiweiE-com)

<br>

- 知识星球：AI量化投资 （加我微信，邀请）

<br>

<table class="table table-striped table-bordered table-vcenter">
    <tbody class=ai-notebooks-table-content>
    <tr>
        <td width=33%>
            <div class="mdl-cell mdl-cell--4-col">
                <a href="https://github.com/UFund-Me/.github/assets/29084184/c8782e38-be7d-4839-bad0-6736bfb9ab9e"><img class="illustration_img" width="320" alt="添加个人微信" src="https://raw.githubusercontent.com/UFund-Me/Qbot/main/gui/imgs/wechat.png"></img></a> <br>个人微信
            </div>
        </td>
        <td width=33%>
            <div class="mdl-cell mdl-cell--4-col">
                <a href="https://github.com/UFund-Me/.github/assets/29084184/712a460f-a264-4f16-a7b8-c990106ec624"><img class="illustration_img" width="318" alt="加入微信交流群" src="https://github.com/UFund-Me/Qbot/assets/29084184/c81a0983-b5c4-43b5-acb5-3bd98010f7e3"/></a> <br>Qbot用户微信交流群
            </div>
        </td>
        <td width=33%>
            <div class="mdl-cell mdl-cell--4-col">
                <a href="https://github.com/UFund-Me/.github/assets/29084184/9d3983ff-ece8-4f99-8579-94234987dcf2"><img class="illustration_img" height="320" alt="加入知识星球（付费）" src="https://raw.githubusercontent.com/UFund-Me/Qbot/main/gui/imgs/zsxq.png"/></a> <br> <sup>AI量化交易策略分享、实盘交易教程、实时数据接口</sup> <br>知识星球（付费）
            </div>
        </td>
    </tr>
    </tbody>
</table>

若二维码因 Github 网络无法打开，请点击[二维码](https://charmve.github.io/img/contact-card.png)直接打开图片。

<br>

<table align="center"><tbody>
  <tr>
    <td colspan="2" rowspan="1">
      <p>🎉 本项目刚上线就收到了两次GitHub官方趋势榜Top5、Top1好成绩! <br>现对于转发本项目到朋友圈或100人以上微信群等，可获得<b>知识星球价值20元的优惠券一张</b>, 限时10张。</p>
    </td>
  </tr>
  <tr>
    <td colspan="1" rowspan="5" class="ai-notebooks-table-points ai-orange-link">
        <div align="center">
            <a href="https://github.com/UFund-Me/Qbot" target="_blank"><img src="https://img.shields.io/badge/-💮 %20Qbot-red.svg" alt="Qbot" title="Qbot"></a>&nbsp;
            <a class="https://github.com/UFund-Me/Qbot">
              <img class="ai-header-badge-img" src="https://img.shields.io/github/stars/UFund-Me/Qbot.svg?style=social&label=Star">
            </a>&nbsp;
            <a href="https://raw.githubusercontent.com/UFund-Me/Qbot/main/gui/imgs/wechat.png" target="_blank"><img src="https://img.shields.io/badge/-WeChat-lightgreen.svg?logo=WeChat"></a>
            <p>🔥Among the <a href="https://github.com/topics/quant-trade" target="_blank">top 10</a> Quant &amp; Trade repos on GitHub</p>
        </div>
        <ul> 主要包含两部分：在本项目的基础下，
            <li>增加更多策略研究，包含回测源码（请先学会有本项目中的策略库）；</li>
            <li>增加实盘接入方式的源代码；</li>
            <li>策略交流，AI投研实验室MeetUp线上/线下活动（对于基础薄弱的同学，欢迎进微信群答疑）</li>
            <li>最近较为受欢迎的一个福利点：AI选股推荐列表邮件订阅，这有个样例 https://github.com/UFund-Me/Qbot/issues/37</li>
        </ul>
      </td>
      <td>
        <img align="center" src="https://github.com/UFund-Me/Qbot/assets/29084184/bb5ec619-887a-4ba7-a9d7-9e8b083bbb1a" height="320" alt="知识星球优惠券">
      </td>
</tr></tbody></table>

<br>

## :warning: Disclaimer

交易策略和自动化工具只是提供便利，并不代表实际交易收益。该项目任何内容不构成任何投资建议。市场有风险，投资需谨慎。
    
## 🔥 Stargazers Over Time
	
<!-- [![Stargazers over time](https://starchart.cc/UFund-Me/Qbot.svg)](https://starchart.cc/UFund-Me/Qbot) -->

[![Star History Chart](https://api.star-history.com/svg?repos=UFund-Me/Qbot,ailabx/ailabx,jadepeng/pytrader&type=Timeline)](https://star-history.com/#UFund-Me/Qbot&ailabx/ailabx&jadepeng/pytrader&Timeline)

## Sponsors & support

If you like the project, you can become a sponsor at [Open Collective](https://opencollective.com/qbot) or use [GitHub Sponsors](https://github.com/sponsors/Charmve).

<b>Thank you for supporting Qbot!</b>

<a href="https://opencollective.com/qbot" target="_blank"><img src="https://opencollective.com/Qbot/tiers/sponsors.svg?avatarHeight=120" alt="Sponsor"></a>
<a href="https://opencollective.com/qbot#category-CONTRIBUTE" target="_blank"><img src="https://opencollective.com/qbot/tiers/backers.svg?avatarHeight=100"/></a>

## LICENSE

<img src="../qbot/asserts/statics/imgs/license_by-nc-sa_4.0.png">

署名-非商业性使用-相同方式共享 4.0 国际

<a href=""><img align="left" alt="Go for it!" src="https://raw.githubusercontent.com/Charmve/computer-vision-in-action/main/res/ui/frontpage/2020-sponsors.svg" height="68" title="Do what you like, and do it best!"/></a>

## ♥️ Acknowledgements

<b>Last but not least, we're thankful to these open-source repo for sharing their services for free:</b>

基于 backtrader、[vnpy](https://github.com/vnpy/vnpy)、[qlib](https://github.com/microsoft/qlib)、tushare、easyquant、[fund-strategies](https://github.com/SunshowerC/fund-strategy)、[investool](https://github.com/axiaoxin-com/investool) 等开源项目，感谢开发者。

<br><br>

感谢大家的支持与喜欢！

Code with ❤️ & ☕️     @Charmve 2022-2023
