# -*- coding: utf-8 -*-
"""
a sample to show how to utilize the realtime watching function
"""

import xalpha as xa
import pandas as pd

# first introduce some aim you want to watch
# you must use rfundinfo instead of standard fundinfo class to get the realtime netvalue
cm = xa.rfundinfo("164818")
gf = xa.rfundinfo("001469")

# secondly setup some policies you want to run and watch
st1 = xa.policy.buyandhold(gf, start="2018-08-10", end="2019-01-01")
st2 = xa.policy.scheduled(
    cm, totmoney=1000, times=pd.date_range("2018-01-01", "2019-01-01", freq="W-MON")
)
st3 = xa.policy.scheduled(
    gf, totmoney=500, times=pd.date_range("2018-01-01", "2019-01-01", freq="W-WED")
)
st4 = xa.policy.scheduled_tune(
    cm,
    totmoney=1000,
    times=pd.date_range("2018-01-01", "2019-01-01", freq="W-TUE"),
    piece=[(0.95, 2), (1, 1)],
)

# thirdly put all your favorite policies into a review class and name these policies correspondingly
check = xa.review([st1, st2, st3, st4], ["一把梭", "赌一赌", "摩托车", "变路虎"])

# fourthly, setup the email configuration dict
conf = {
    "sender": "aaa@bb.com",
    "sender_name": "name",
    "receiver": ["aaa@bb.com", "ccc@dd.com"],
    "password": "123456",
    "server": "smtp.bb.com",
    "port": 123,
    "receiver_name": ["me", "guest"],
}

# finally send the notification
check.notification(conf)

# you are all done

"""
关于如何将该脚本定时运行，就不是 xalpha 所关心的问题了，您可以选取系统依赖的定时方案。比如 *nix 中的 crontab 等，将
｀python3 notification.py｀ 加入系统定时任务即可，建议每个工作日15:00前运行。需要提前预留出程序运行，邮件发送与接受，基金购买的时间。
一旦超过 15:00 则成为下一交易日的申购赎回。
"""
