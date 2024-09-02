#!/usr/bin/env python
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
    sys.path.append(r'D:\GitHub\dashboard')
else:
    sys.path.append('/root/dashboard')
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
import asynctest
from trader.utils import *
from datetime import datetime
from trader.utils.read_config import config


class APITest(asynctest.TestCase):
    def setUp(self):
        self.redis_client = redis.StrictRedis(
            host=config.get('REDIS', 'host', fallback='localhost'),
            db=config.getint('REDIS', 'db', fallback=1), decode_responses=True)
        self.trading_day = datetime.strptime(self.redis_client.get("LastTradingDay"), '%Y%m%d')

    def tearDown(self) -> None:
        self.redis_client.close()

    @asynctest.skipIf(True, 'no need')
    async def test_get_shfe_data(self):
        self.assertTrue(await update_from_shfe(self.trading_day))

    @asynctest.skipIf(True, 'no need')
    async def test_get_dce_data(self):
        self.assertTrue(await update_from_dce(self.trading_day))

    @asynctest.skipIf(True, 'no need')
    async def test_get_czce_data(self):
        self.assertTrue(await update_from_czce(self.trading_day))

    @asynctest.skipIf(True, 'no need')
    async def test_get_cffex_data(self):
        self.assertTrue(await update_from_cffex(self.trading_day))

    @asynctest.skipIf(True, 'no need')
    async def test_get_contracts_argument(self):
        self.assertTrue(await get_contracts_argument(self.trading_day))

    @asynctest.skipIf(True, 'no need')
    async def test_get_all(self):
        print(f'tradingday: {self.trading_day}')
        tasks = [
            update_from_shfe(self.trading_day),
            update_from_dce(self.trading_day),
            update_from_czce(self.trading_day),
            update_from_cffex(self.trading_day),
            get_contracts_argument(self.trading_day)
        ]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        self.assertEqual(result, [True, True, True, True, True])

    @asynctest.skipIf(False, 'no need')
    async def test_load_from_kt(self):
        self.assertTrue(load_kt_data(r'D:\test'))

    @asynctest.skipIf(True, 'no need')
    async def test_create_main(self):
        inst = Instrument.objects.get(product_code='eb')
        self.assertTrue(create_main(inst))

    @asynctest.skipIf(True, 'no need')
    async def test_calc_profit(self):
        for trade in Trade.objects.filter(close_time__isnull=True):
            bar = DailyBar.objects.filter(code=trade.code).order_by('-time').first()
            trade.profit = (bar.close - trade.avg_entry_price) * trade.filled_shares * trade.instrument.volume_multiple
            if trade.direction == DirectionType.values[DirectionType.SHORT]:
                trade.profit *= -1
            trade.save(update_fields=['profit'])
        self.assertTrue(True)
