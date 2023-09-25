#!/bin/bash

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# shellcheck disable=SC1090,SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

pip install -r requirements.txt

if pip show PyInstaller &> /dev/null; then
    echo "PyInstaller 已经安装"
else
    echo "PyInstaller 没有安装"
    pip install PyInstaller

    if pip show numpy &> /dev/null; then
        echo "PyInstaller 安装成功"
    else
        echo "PyInstaller 安装失败"
        exit 1
    fi
fi


cd ~/Qbot
# 3、MAC打包
pyinstaller -w --clean -p gui/bkt_result/bkt_result.html -p pytrader/strategies/workflow_by_code.ipynb main.py
# 3、win打包
# pyinstaller -F -p 依赖包路径 main.py

# pip install PyInstaller
# pyi-makespec --onefile --windowed main.py
pyinstaller main.spec