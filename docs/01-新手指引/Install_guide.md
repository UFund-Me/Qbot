# Install

## Quick Start

```bash
 ____________________________________
< Run ``./env_setup.sh`` to say hello >
 ------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
```


## Setup

支持三种不同的环境搭建方式：

### 第一种：Conda (推荐方式)

1. 下载安装Conda

```bash
wget https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh
bash Anaconda3-5.3.1-Linux-x86_64.sh
```
2. 编辑 ``~/.bashrc`` 文件，在最后面加上

``export PATH=/home/aeasringnar/anaconda3/bin:$PATH``

保存退出后：``source ~/.bashrc``

3. 再次输入``conda list``测试

4. 创建conda环境：

```bash
conda create -n Qbot python=3.9
conda activate Qbot

pip install -r requirements.txt
```

### 第二种：本地环境（支持MacOS、Ubuntu18、Win10）

```
bash ./env_setup.sh
```

### 第三种：Docker

还在做。。。

```
cd ~/Qbot
docker build -t ufune-me:qbot-1.0.0 . 
docker images 
docker start <image-id>
docker exec -it <container-id> bash
```

## Prepare

申请聚宽账号、掘金仿真账号，设置环境变量:

```bash
export USER_ID="admin"                   # replace your info
export PASSWORD="admin1234."             # replace your info
export MAIL_LICENSE="wafasqtakgywoobach" # replace your own 163.com / qq.com license

```

## RUN

Auto run with ci 'auto-trade.yml' workflows, eg:

```
python main.py
# if run on Mac, please use 'pythonw main.py'

cd  pytrader
python test_backtrade.py
python test_trader.py

```
