# coding=utf-8
#
# Copyright 2016 timercrack
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import os
import django
if sys.platform == 'darwin':
    sys.path.append('/Users/jeffchen/Documents/gitdir/dashboard')
elif sys.platform == 'win32':
    sys.path.append(r'D:\github\dashboard')
else:
    sys.path.append('/root/gitee/dashboard')
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
import redis
import logging
from logging import handlers
from trader.strategy.brother2 import TradeStrategy
from trader.utils.read_config import config_file, app_dir, config


class RedislHandler(logging.StreamHandler):
    def __init__(self, channel: str):
        super().__init__()
        self.redis_client = redis.StrictRedis(
            host=config.get('REDIS', 'host', fallback='localhost'), port=config.getint('REDIS', 'port', fallback=6379),
            db=config.getint('REDIS', 'db', fallback=0), decode_responses=True)
        self.channel = channel

    def emit(self, message: logging.LogRecord):
        content = str(message.msg)
        self.redis_client.publish(self.channel, content)


if __name__ == '__main__':
    os.path.exists(app_dir.user_log_dir) or os.makedirs(app_dir.user_log_dir)
    log_file = os.path.join(app_dir.user_log_dir, 'trader.log')
    
    file_handler = handlers.RotatingFileHandler(log_file, encoding='utf-8', maxBytes=1024*1024, backupCount=1)
    general_formatter = logging.Formatter(config.get('LOG', 'format'))
    file_handler.setFormatter(general_formatter)
    file_handler.setLevel(config.get('LOG', 'file_level', fallback='DEBUG'))
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(general_formatter)
    console_handler.setLevel('DEBUG')
    
    redis_handler = RedislHandler(config.get('MSG_CHANNEL', 'weixin_log'))
    redis_handler.setFormatter(config.get('LOG', 'weixin_format'))
    redis_handler.setLevel(config.get('LOG', 'flower_level', fallback='INFO'))
    
    logger = logging.getLogger()
    logger.setLevel('DEBUG')
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(redis_handler)
    logger = logging.getLogger("main")
    
    pid_path = os.path.join(app_dir.user_cache_dir, 'trader.pid')
    if not os.path.exists(pid_path):
        if not os.path.exists(app_dir.user_cache_dir):
            os.makedirs(app_dir.user_cache_dir)
    with open(pid_path, 'w') as pid_file:
        pid_file.write(str(os.getpid()))
    print('Big Brother is watching you!')
    print('used config file:', config_file)
    print('log stored in:', app_dir.user_log_dir)
    print('pid file:', pid_path)
    TradeStrategy(name='大哥2.2').run()
