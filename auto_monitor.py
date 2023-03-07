import os
import time
import tushare as ts
import pandas as pd
from utils.larkbot import LarkBot

def check_strategy():
	
	return True

def check(code, low, high):
	df = ts.get_realtime_quotes(code)
	e = df[['code','name','price','time']]
	p = df[u'price']
	print (e) 
	if float(p[0]) > low and float(p[0]) < high:
		return True
	else :
		return False
	
while True:
    WEBHOOK_SECRET = "wNMVU3ewSm2F0G2TwTX4Fd"
    bot = LarkBot(secret=WEBHOOK_SECRET)
    if check('sh', 3200, 10000) or check('601318', 0, 49):
        bot.send(content="[Signal💡] 中国平安 低于 ¥49")
		# if linux
        # os.system('play ./sounds/alert-bells.wav')
        # if MacOs
        os.system('afplay ./sounds/bell.wav')
        exit()
    time.sleep(5)