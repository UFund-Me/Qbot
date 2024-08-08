import logging

# 1.创建一个logger实例，并且logger实例的名称命名为“single info”，设定的严重级别为DEBUG
LOGGER = logging.getLogger("qbot")
LOGGER.setLevel(logging.DEBUG)

LOGGER_TXT = logging.getLogger("qbot")
LOGGER_TXT.setLevel(logging.DEBUG)

# 2.创建一个handler，这个主要用于控制台输出日志，并且设定严重级别
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 2、创建一个handler，用于写入日志文件
fh = logging.FileHandler("qbot_pro.log", encoding="utf-8", mode="a")
fh.setLevel(logging.WARNING)

# 3.创建handler的输出格式（formatter）
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d %(funcName)s: %(message)s"
)

# 4.将formatter添加到handler中
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# 5.将handler添加到logger中
LOGGER.addHandler(ch)
LOGGER_TXT.addHandler(fh)
