#!/bin/bash
set -euo pipefail

wget https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh
bash Anaconda3-5.3.1-Linux-x86_64.sh

echo "export PATH=/home/$USER/anaconda3/bin:$PATH" | sudo tee -a ~/.bashrc
# shellcheck disable=SC1090
source ~/.bashrc

conda info --env
conda create -n Qbot python=3.9
conda activate Qbot
conda info --env

pip install -r requirements.txt

export USER_ID="admin"       # replace your info
export PASSWORD="admin1234." # replace your info

echo "Successful - Environment is set up!"

echo "Enjoy, Quanter!"

cat << EOF

             ██████╗ ██████╗  ██████╗ ████████╗
            ██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝
            ██║   ██║██████╔╝██║   ██║   ██║   
            ██║▄▄ ██║██╔══██╗██║   ██║   ██║   
            ╚██████╔╝██████╔╝╚██████╔╝   ██║   
             ╚══▀▀═╝ ╚═════╝  ╚═════╝    ╚═╝   
                
                        Alpha Qbot
          ++++=================================++++
                 auth: Charmve   --V.0.1   

   🤖 Qbot = 智能交易策略 + 回测系统 + 自动化交易 (+ 可视化分析工具)
                |           |          |            |
                |           |          |             \_ quantstats (dashboard\online operate)
                |           |           \______________ Qbot - vnpy, pytrader, pyfunds
                |           \__________________________ BackTest - backtrader, easyquant
                \______________________________________ quant.ai - qlib, deep learning strategies                                   
EOF

echo "Run example backtest"
cd pytrader
python test_backtrade.py
# python test_trader.py
