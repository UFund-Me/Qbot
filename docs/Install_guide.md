# Install

## Setup

1. 下载安装Conda
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

申请聚宽账号，设置环境变量:

```bash
export USER_ID="admin"
export PASSWORD="admin1234."
```

## RUN

Auto run with ci, eg:

```
python ./qbot/main.py
# if run on Mac, please use 'pythonw ./qbot/main.py'

cd  pytrader
python test_backtrade.py
python test_trader.py

```
