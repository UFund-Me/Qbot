<h1> <img src="https://user-images.githubusercontent.com/29084184/204598632-23c473db-92ee-4e9b-9b57-d6d95c861fdf.png" width="42"/> π€ Qbot </h1>

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
    <b>Qbot</b> is an AI-oriented quantitative investment platform, which aims to realize the potential, <br>
  empower AI technologies in quantitative investment.
  </p>
</div>

```
π€ Qbot = ζΊθ½δΊ€ζη­η₯ + εζ΅η³»η» + θͺε¨εδΊ€ζ (+ ε―θ§εεζε·₯ε·)
            |           |          |            |
            |           |          |             \_ quantstats (dashboard\online operate)
            |           |           \______________ Qbot - vnpy, pytrader, pyfunds
            |           \__________________________ BackTest - backtrader, easyquant
            \______________________________________ quant.ai - qlib, deep learning strategies
```

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
```

## Benchmark and Model zoo

Results and models are available in the [model zoo](docs/model_zoo.md).
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

|                | status | benchmark |   framework  | DGCNN | RegNetX |                        addition                                |   arXiv    |
|  :-----------: | :----: | :--------:| :----:       | :---: | :-----: | :------------------------------------------------------------: | :--------: |
|     GBDT       |   β    |     β     |   XGBoost    |   β   |    β    |  Tianqi Chen, et al. KDD 2016                                  |     β      |
|     GBDT       |   β    |     β     |   LightGBM   |   β   |    β    |  Guolin Ke, et al. NIPS 2017                                   |     β      |
|     GBDT       |   β    |     β     |   Catboost   |   β   |    β    |  Liudmila Prokhorenkova, et al. NIPS 2018β                     |     β      |
|     MLP        |   β    |     β     |   pytorch    |   β   |    β    |                             --                                 |     β      |
|     LSTM       |   β    |     β     |   pytorch    |   β   |    β    |  Sepp Hochreiter, et al. Neural computation 1997               |     β      |
|     GRU        |   β    |     β     |   pytorch    |   β   |    β    |  Kyunghyun Cho, et al. 2014                                    |     β      |
|     ALSTM      |   β    |     β     |   pytorch    |   β   |    β    |  Yao Qin, et al. IJCAI 2017                                    |     β      |
|     GATs       |   β    |     β     |   pytorch    |   β   |   β     |  Petar Velickovic, et al. 2017                                 |     β      |
|     SFM        |   β    |     β     |   pytorch    |   β   |    β    |  Liheng Zhang, et al. KDD 2017                                 |     β      |
|     TFT        |   β    |     β     |   tensorflow |   β   |    β    |  Bryan Lim, et al. International Journal of Forecasting 2019   |     β      |
|     TabNet     |   β    |     β     |   pytorch    |   β   |    β    |  Sercan O. Arik, et al. AAAI 2019                              |     β      |
| DoubleEnsemble |   β    |     β     |   LightGBM   |   β   |   β     |  Chuheng Zhang, et al. ICDM 2020                               |     β      |
|     TCTS       |   β    |     β     |   pytorch    |   β   |    β    |  Xueqing Wu, et al. ICML 2021                                  |     β      |
|  Transformer   |   β    |     β     |   pytorch    |   β   |    β    |  Ashish Vaswani, et al. NeurIPS 2017                           |     β      |
|  Localformer   |   β    |     β     |   pytorch    |   β   |    β    |  Juyong Jiang, et al.                                          |     β      |
|     TRA        |   β    |     β     |   pytorch    |   β   |    β    |  Hengxu, Dong, et al. KDD 2021                                 |     β      |
|     TCN        |   β    |     β     |   pytorch    |   β   |    β    |  Shaojie Bai, et al. 2018                                      |     β      |
|     ADARNN     |   β    |     β     |   pytorch    |   β   |    β    |  YunTao Du, et al. 2021                                        |     β      |
|     ADD        |   β    |     β     |   pytorch    |   β   |    β    |  Hongshun Tang, et al.2020                                     |     β      |
|     IGMTF      |   β    |     β     |   pytorch    |   β   |    β    |  Wentao Xu, et al.2021                                         |     β      |
|     HIST       |   β    |     β     |   pytorch    |   β   |    β    |  Wentao Xu, et al.2021                                         |     β      |


<sup>**Note:** All the about **300+ models, methods of 40+ papers** in quant.ai supported by [Model Zoo](./docs/model_zoo.md) can be trained or used in this codebase.</sup>

## Quantstats Report

![Quantstats Report](https://user-images.githubusercontent.com/29084184/207054856-44d1815b-f92f-40a7-b82e-e4a6b3960f2f.png)

Click [HERE](quantstats#visualize-stock-performance) to more detail.
## Contributing

We appreciate all contributions to improve Qbot. Please refer to [CONTRIBUTING.md](.github/CONTRIBUTING.md) for the contributing guideline.


## Acknowledgement

<br><br>

ζθ°’ε€§ε?Άηζ―ζδΈεζ¬’οΌ

Code with β€οΈ & βοΈ @Charmve 2022-2023
