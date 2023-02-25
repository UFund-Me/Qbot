#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入模块
from wxpy import *

# 初始化机器人，扫码登陆
bot = Bot()

# 搜索名称含有 "游否" 的男性深圳好友
my_friend = bot.friends().search('Chamrve', sex=MALE, city="苏州")[0]


image_file=""/Users/charmve/Qbot/gui/imgs/UFund.png

# 发送文本给好友
my_friend.send('Hello WeChat!')
# 发送图片
my_friend.send_image(image_file)


# 打印来自其他好友、群聊和公众号的消息
@bot.register()
def print_others(msg):
    print(msg)

# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('你好👋，我是迈微AI研习社助理，其实也是Charmve本人 哈哈哈😂')

# 进入 Python 命令行、让程序保持运行
embed()

# 或者仅仅堵塞线程
# bot.join()
