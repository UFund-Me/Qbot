<h1> <img src="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" width="42"/> 🤖 Qbot </h1>

[![CodeQL](https://github.com/UFund-Me/Qbot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/codeql-analysis.yml)
[![AutoTrade](https://github.com/UFund-Me/Qbot/actions/workflows/auto-trade.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/auto-trade.yml)
[![Pylint](https://github.com/UFund-Me/Qbot/actions/workflows/pylint.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/pylint.yml)
[![Coverage](https://github.com/UFund-Me/Qbot/actions/workflows/coverage.yml/badge.svg)](https://github.com/UFund-Me/Qbot/actions/workflows/coverage.yml)
<a href="https://github.com/Charmve/computer-vision-in-action/tree/main/code/"><img src="https://img.shields.io/badge/Python-%203.8|%203.9-000000.svg?logo=Python&color=blue" alt="Python version"></a>
<a href="https://ufund-me.github.io/qbot"><img src="https://readthedocs.org/projects/pyod/badge/?version=latest" alt="Documentation status"></a>

<div align="center">
  <img src="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" width="224"/>
  <div>&nbsp;</div>
  <div align="center">
    <b><font size="5">Qbot website</font></b>
    <sup>
      <a href="https://ufund-me.github.io/Qbot/">
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

  <i>喜欢这个项目吗？请考虑 ❤️赞助本项目 以帮助改进！</i>

</div>

## Installation

[Install Guide](./docs/Install_guide.md)

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

## Get Started

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

## Benchmark and Model zoo

Results and models are available in the [model zoo](docs/model_zoo.md). [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UFund-Me/Qbot/blob/main/pytrader/strategies/workflow_by_code.ipynb/HEAD)
<!------
<div align="center">
  <b>Components</b>
</div>
<table align="center">
  <tbody>
    <tr align="center" valign="bottom">
      <td>
        <b>Backbones</b>
      </td>
      <td>
        <b>Heads</b>
      </td>
      <td>
        <b>Features</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
      <ul>
        <li><a href="configs/pointnet2">PointNet (CVPR'2017)</a></li>
        <li><a href="configs/pointnet2">PointNet++ (NeurIPS'2017)</a></li>
        <li><a href="configs/regnet">RegNet (CVPR'2020)</a></li>
        <li><a href="configs/dgcnn">DGCNN (TOG'2019)</a></li>
        <li>DLA (CVPR'2018)</li>
        <li>MinkResNet (CVPR'2019)</li>
      </ul>
      </td>
      <td>
      <ul>
        <li><a href="configs/free_anchor">FreeAnchor (NeurIPS'2019)</a></li>
      </ul>
      </td>
      <td>
      <ul>
        <li><a href="configs/dynamic_voxelization">Dynamic Voxelization (CoRL'2019)</a></li>
      </ul>
      </td>
    </tr>
  </tbody>
</table>

<div align="center">
  <b>Architectures</b>
</div>
<table align="center">
  <tbody>
    <tr align="center" valign="middle">
      <td>
        <b>3D Object Detection</b>
      </td>
      <td>
        <b>Monocular 3D Object Detection</b>
      </td>
      <td>
        <b>Multi-modal 3D Object Detection</b>
      </td>
      <td>
        <b>3D Semantic Segmentation</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
        <li><b>Outdoor</b></li>
        <ul>
            <li><a href="configs/parta2">Part-A2 (TPAMI'2020)</a></li>
            <li><a href="configs/centerpoint">CenterPoint (CVPR'2021)</a></li>
        </ul>
        <li><b>Indoor</b></li>
        <ul>
            <li><a href="configs/groupfree3d">Group-Free-3D (ICCV'2021)</a></li>
            <li><a href="configs/fcaf3d">FCAF3D (ECCV'2022)</a></li>
      </ul>
      </td>
      <td>
        <li><b>Outdoor</b></li>
        <ul>
          <li><a href="configs/smoke">SMOKE (CVPRW'2020)</a></li>
          <li><a href="configs/fcos3d">FCOS3D (ICCVW'2021)</a></li>
          <li><a href="configs/pgd">PGD (CoRL'2021)</a></li>
        </ul>
        <li><b>Indoor</b></li>
        <ul>
          <li><a href="configs/imvoxelnet">ImVoxelNet (WACV'2022)</a></li>
        </ul>
      </td>
      <td>
        <li><b>Outdoor</b></li>
        <ul>
          <li><a href="configs/mvxnet">MVXNet (ICRA'2019)</a></li>
        </ul>
        <li><b>Indoor</b></li>
        <ul>
          <li><a href="configs/imvotenet">ImVoteNet (CVPR'2020)</a></li>
        </ul>
      </td>
      <td>
        <li><b>Indoor</b></li>
        <ul>
          <li><a href="configs/pointnet2">PointNet++ (NeurIPS'2017)</a></li>
          <li><a href="configs/paconv">PAConv (CVPR'2021)</a></li>
          <li><a href="configs/dgcnn">DGCNN (TOG'2019)</a></li>
        </ul>
      </ul>
      </td>
    </tr>
</td>
    </tr>
  </tbody>
</table>

--------->

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


<sup>**Note:** All the about **300+ models, methods of 40+ papers** in quant.ai supported by [Model Zoo](./docs/model_zoo.md) can be trained or used in this codebase.</sup>

## Quantstats Report

![Quantstats Report](https://user-images.githubusercontent.com/29084184/207054856-44d1815b-f92f-40a7-b82e-e4a6b3960f2f.png)

Click [HERE](quantstats#visualize-stock-performance) to more detail.

#### Some strategy backtest results:

A股回测MACD策略:
![KDJ with MACD](pytrader/doc/04.kdj_with_macd/Figure_kdj_with_macd.png)

A股回测KDJ策略:
![MACD](pytrader/doc/02.easy_macd_strategy/Figure_macd.png)
## Contributing

We appreciate all contributions to improve Qbot. Please refer to [CONTRIBUTING.md](.github/CONTRIBUTING.md) for the contributing guideline.

## Acknowledgement

基于Backtrader、vnpy、qlib、tushare、backtest、easyquant等开源项目，感谢开发者。

<br>

## 💖 Sponsors and Backers

<a href="https://github.com/sponsors/Charmve" target="_blank"><img src="https://opencollective.com/Qbot/tiers/sponsors.svg?avatarHeight=36" alt="Sponsor" width="160"></a>
<a href="https://github.com/sponsors/Charmve" target="_blank"><img src="https://opencollective.com/Qbot/tiers/backers.svg?avatarHeight=36" alt="Backer" width="900"></a>

<br><br>

感谢大家的支持与喜欢！

Code with ❤️ & ☕️ @Charmve 2022-2023
