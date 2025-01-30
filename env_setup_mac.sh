#!/bin/bash

set -euo pipefail
# shellcheck disable=all

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck disable=SC1091
source "${TOP_DIR}/scripts/qbot_base.sh"

# 检测操作系统类型
OS_TYPE="$(uname)"
IS_MINGW=false

# 改进的操作系统检测
case "$OS_TYPE" in
    "Darwin")
        info "Running on macOS"
        ;;
    "Linux")
        info "Running on Linux"
        ;;
    MINGW*)
        IS_MINGW=true
        info "Running on Windows/MinGW"
        ;;
    MSYS*)
        IS_MINGW=true
        info "Running on Windows/MSYS"
        ;;
    *)
        info "Unknown operating system: $OS_TYPE"
        ;;
esac

# 检查 conda 是否已安装
if ! command -v conda &> /dev/null; then
    if [ "$OS_TYPE" = "Darwin" ]; then
        info "在 macOS 上未检测到 conda，请使用 homebrew 安装："
        info "brew install --cask anaconda"
        exit 1
    else
        info "下载并安装 Anaconda..."
        wget https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh
        bash Anaconda3-5.3.1-Linux-x86_64.sh
        rm Anaconda3-5.3.1-Linux-x86_64.sh
    fi
fi

# 根据不同操作系统设置 conda 路径
if [ "$OS_TYPE" = "Darwin" ]; then
    # 检查多个可能的 conda 安装路径
    POSSIBLE_PATHS=(
        "/usr/local/anaconda3"
        "$HOME/anaconda3"
        "/opt/anaconda3"
        "/opt/homebrew/anaconda3"
        "$HOME/opt/anaconda3"
    )
    
    CONDA_PATH=""
    for path in "${POSSIBLE_PATHS[@]}"; do
        if [ -d "$path" ]; then
            CONDA_PATH="$path"
            break
        fi
    done
    
    if [ -z "$CONDA_PATH" ]; then
        error "无法找到 Anaconda 安装路径。请确保 Anaconda 已正确安装。"
        info "您可以使用以下命令安装 Anaconda："
        info "brew install --cask anaconda"
        exit 1
    fi
else
    CONDA_PATH="$HOME/anaconda3"
fi

# 确保 conda 命令可用并初始化
info "初始化 conda..."
if [ -f "${CONDA_PATH}/etc/profile.d/conda.sh" ]; then
    . "${CONDA_PATH}/etc/profile.d/conda.sh"
elif [ -f "${CONDA_PATH}/bin/conda" ]; then
    export PATH="${CONDA_PATH}/bin:$PATH"
else
    error "找不到 conda 命令。请确保 Anaconda 已正确安装。"
    exit 1
fi

# 验证 conda 是否可用
if ! command -v conda >/dev/null 2>&1; then
    error "conda 命令不可用，请检查 Anaconda 安装。"
    exit 1
fi

# 初始化 conda（如果尚未初始化）
if ! conda info --envs >/dev/null 2>&1; then
    info "首次初始化 conda..."
    # 保存当前 PATH
    OLD_PATH="$PATH"
    
    conda init "$(basename "$SHELL")"
    
    # 重新加载 shell 配置
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    elif [ -f ~/.zshrc ]; then
        . ~/.zshrc
    fi
    
    # 恢复 PATH，避免重复
    export PATH="$OLD_PATH"
fi

# 确保基础环境正常
info "验证 conda 基础环境..."
if ! conda activate base >/dev/null 2>&1; then
    error "无法激活 base 环境，请检查 Anaconda 安装。"
    exit 1
fi

# 更新 conda（添加错误处理）
info "更新 conda..."
if ! conda update -n base -c defaults conda -y; then
    warning "conda 更新失败，继续执行..."
fi

# 删除已存在的 qbot 环境（如果存在）
if conda env list | grep -q "qbot"; then
    info "删除已存在的 qbot 环境..."
    conda deactivate 2>/dev/null || true
    conda env remove -n qbot -y
fi

# 创建新环境（添加错误处理）
info "创建 Python 环境..."
if ! conda create -n qbot python=3.9 -y; then
    error "创建 qbot 环境失败"
    exit 1
fi

# 激活环境（使用完整路径并添加错误处理）
info "激活 qbot 环境..."
CONDA_BASE=$("$CONDA_PATH/bin/conda" info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

# 尝试多种方式激活环境
if ! conda activate qbot 2>/dev/null; then
    info "尝试替代激活方法..."
    if ! source activate qbot 2>/dev/null; then
        if ! . activate qbot 2>/dev/null; then
            error "无法激活 qbot 环境，尝试以下手动步骤："
            info "1. 关闭当前终端"
            info "2. 打开新终端"
            info "3. 运行: conda activate qbot"
            exit 1
        fi
    fi
fi

# 验证环境激活（添加更多详细信息）
CURRENT_ENV=$(conda info --envs | grep '*' | awk '{print $1}')
if [ "$CURRENT_ENV" != "qbot" ]; then
    error "qbot 环境未正确激活"
    info "当前环境: $CURRENT_ENV"
    info "请尝试手动运行: conda activate qbot"
    exit 1
fi

# 验证 Python 版本
PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$PYTHON_VERSION" != "3.9"* ]]; then
    error "Python 版本不正确: $PYTHON_VERSION (需要 3.9)"
    exit 1
fi

# 使用 conda 安装主要依赖
info "使用 conda 安装主要依赖..."
conda install -y -c conda-forge \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    matplotlib \
    seaborn \
    statsmodels \
    ta-lib \
    jupyter \
    ipython \
    requests \
    tqdm \
    pytz

# 更新 pip
conda install -y pip
pip install --upgrade pip

# 安装 backtrader
info "安装 backtrader..."
pip install backtrader

# 安装其他依赖
info "安装其他依赖包..."
if [ -f "requirements.txt" ]; then
    # 创建临时文件来存储过滤后的 requirements
    TMP_REQ=$(mktemp)
    # 过滤掉已经通过 conda 安装的包
    grep -v -E "numpy|pandas|scipy|scikit-learn|matplotlib|seaborn|statsmodels|ta-lib|jupyter|ipython|requests|tqdm|pytz|backtrader" requirements.txt > "$TMP_REQ" || true
    if [ -s "$TMP_REQ" ]; then
        pip install -r "$TMP_REQ"
    fi
    rm "$TMP_REQ"
else
    warning "requirements.txt 文件不存在，跳过安装依赖"
fi

# 安装额外需要的包
info "安装额外依赖..."
pip install -U wxpy logbook

# 安装 easyquant 相关依赖
info "安装 easyquant 相关依赖..."
pip install logbook easyutils pytesseract arrow bs4 lxml jqdatasdk redis ddddocr easytrader

# 创建软链接以修复导入路径
info "修复导入路径..."
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
EASYTRADER_PATH="$SITE_PACKAGES/easytrader"
if [ -d "$EASYTRADER_PATH" ]; then
    if [ -d "pytrader/easyquant/easytrader" ]; then
        rm -rf "pytrader/easyquant/easytrader"
    fi
    ln -sf "$EASYTRADER_PATH" "pytrader/easyquant/easytrader"
    info "已创建 easytrader 软链接"
else
    error "找不到 easytrader 包，请检查安装"
    exit 1
fi

# 安装其他数据源相关依赖
info "安装数据源相关依赖..."
pip install \
    jqdatasdk \
    tushare \
    baostock \
    akshare \
    pandas_datareader \
    yfinance \
    redis \
    redis-py-cluster \
    hiredis

# 安装数据库相关依赖
info "安装数据库相关依赖..."
pip install \
    pymongo \
    pymysql \
    sqlalchemy \
    redis

# 安装验证码识别相关依赖
info "安装验证码识别相关依赖..."
pip install \
    ddddocr \
    opencv-python \
    Pillow \
    pytesseract

# 设置环境变量
if [ "$IS_MINGW" = true ]; then
    set USER_ID="admin"                      # replace your info
    set PASSWORD="admin1234."                # replace your info
    set MAIL_LICENSE="wafasqtakgywoobach"    # replace your own 163.com / qq.com license
else                                         # Darwin or Linux
    # 添加到 shell 配置文件以持久化环境变量
    SHELL_RC="$HOME/.$(basename "$SHELL")rc"
    if [ -f "$SHELL_RC" ]; then
        # 移除旧的设置（如果存在）
        sed -i.bak '/^export USER_ID=/d' "$SHELL_RC"
        sed -i.bak '/^export PASSWORD=/d' "$SHELL_RC"
        sed -i.bak '/^export MAIL_LICENSE=/d' "$SHELL_RC"
        
        # 添加新的环境变量
        echo 'export USER_ID="admin"' >> "$SHELL_RC"
        echo 'export PASSWORD="admin1234."' >> "$SHELL_RC"
        echo 'export MAIL_LICENSE="wafasqtakgywoobach"' >> "$SHELL_RC"
        
        # 立即设置当前会话的环境变量
        export USER_ID="admin"
        export PASSWORD="admin1234."
        export MAIL_LICENSE="wafasqtakgywoobach"
        
        info "环境变量已添加到 $SHELL_RC"
    else
        warning "找不到 shell 配置文件，仅设置当前会话的环境变量"
        export USER_ID="admin"
        export PASSWORD="admin1234."
        export MAIL_LICENSE="wafasqtakgywoobach"
    fi
fi

info "请注意："
info "1. 使用 jqdatasdk 需要注册聚宽账号：https://www.joinquant.com"
info "2. 获取账号后，需要在代码中设置账号信息："
info "   from jqdatasdk import auth"
info "   auth('your_username', 'your_password')"
info "3. 使用 Redis 需要安装 Redis 服务器："
info "   在 macOS 上可以使用以下命令安装："
info "   brew install redis"
info "   启动 Redis 服务："
info "   brew services start redis"
info "4. 使用 pytesseract 需要安装 tesseract-ocr："
info "   在 macOS 上可以使用以下命令安装："
info "   brew install tesseract"

info "Successful - Environment is set up!"

info "Enjoy, Qboter!"

echo -e "\e]8;;http://github.com/Charmve\aThis is Charmve's blog\e]8;;\a"
echo -e "\e[40;38;5;82m Alpha \e[30;48;5;82m Qbot \e[0m"

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

info "Run example backtest"
cd pytrader
python test_backtrade.py # run backtest
# python test_trader.py # run real trader test

# 根据操作系统运行主程序
if [ "$OS_TYPE" = "Darwin" ]; then
    info "在 macOS 上运行..."
    # 检查是否安装了 pythonw
    if command -v pythonw &> /dev/null; then
        pythonw main.py
    else
        python main.py
    fi
elif [ "$IS_MINGW" = true ]; then
    warning "not support on WinOS."
else
    info "在 Linux 上运行..."
    python main.py
fi

# 修复导入语句
info "修复导入语句..."
cat > fix_imports.patch << 'EOF'
diff --git a/pytrader/easyquant/strategy/strategyTemplate.py b/pytrader/easyquant/strategy/strategyTemplate.py
index xxxx..xxxx 100644
--- a/pytrader/easyquant/strategy/strategyTemplate.py
+++ b/pytrader/easyquant/strategy/strategyTemplate.py
@@ -7,7 +7,7 @@ import time
 from threading import Thread
 
 from ..event_engine import Event
-from ..easytrader.webtrader import WebTrader
+from easytrader.webtrader import WebTrader
 from .quotation_engine_thread import QuotationEngineThread
 
 class StrategyTemplate:
EOF

# 应用补丁
if [ -f "fix_imports.patch" ]; then
    if patch -p1 < fix_imports.patch; then
        info "已修复导入语句"
        rm fix_imports.patch
    else
        error "应用补丁失败"
        exit 1
    fi
fi

# 检查项目结构
if [ ! -d "pytrader" ]; then
    error "找不到 pytrader 目录，请确保在正确的目录中运行脚本"
    exit 1
fi

exit 0
