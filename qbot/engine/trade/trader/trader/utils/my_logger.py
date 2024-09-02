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

import logging
from trader.utils.read_config import *


def get_my_logger(logger_name='main'):
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger
    log_file = os.path.join(app_dir.user_log_dir, '{}.log'.format(logger_name))
    if not os.path.exists(app_dir.user_log_dir):
        os.makedirs(app_dir.user_log_dir)
    formatter = logging.Formatter(config.get('LOG', 'format',
                                             fallback="%(asctime)s %(name)s [%(levelname)s] %(message)s"))
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.setLevel(config.get('LOG', 'level', fallback='ERROR'))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
