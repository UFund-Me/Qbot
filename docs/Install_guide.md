# Install

## Setup

1. 下载安装
```bash
wget https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh
bash Anaconda3-5.3.1-Linux-x86_64.sh
```
2. 编辑 ``~/.basrc`` 文件，在最后面加上

``export PATH=/home/aeasringnar/anaconda3/bin:$PATH``

保存退出后：``source ~/.bashrc``

3. 再次输入``conda list``测试

4. 创建conda环境：

```bash
conda create -n Qbot python=3.9
conda activate Qbot

pip install -r requirements.txt
```

## Prepare

设置环境变量聚款账号:

```bash
export USER_ID="admin"
export PASSWORD="admin1234."
```

## RUN

Auto run with ci, eg:

```
python3 pytrader/backtest.py
python3 pytrader/tradertest.py

```
