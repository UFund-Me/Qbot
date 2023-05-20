'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-24 01:20:21
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-24 01:20:22
FilePath: /Qbot/utils/push_local_sigal.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import os
import sys
import pync
from larkbot import LarkBot

top_path = os.path.dirname(os.path.abspath(sys.argv[0]))
sounds_file = os.path.join(top_path, "../qbot/sounds/bell.wav")

def send_signal_sounds(type="buy"):
    if type == "buy":
        # if linux
        # os.system('play ./qbot/sounds/alert-bells.wav')
        # if MacOs
        os.system(f"afplay {sounds_file}")
    elif type == "sell":
        os.system(f"afplay {sounds_file}")

def send_signal_message_screen(symbol, price, type=default):
    pync.notify(
            f'{symbol}当前价格为{price}',
            title=f'Qbot - {symbol}股票已低于设定值{49}',
            open="https://ufund-me.github.io/",
            appIcon="../gui/imgs/logo.ico",
        )