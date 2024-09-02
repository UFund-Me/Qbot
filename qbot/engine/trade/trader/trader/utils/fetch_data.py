import sys
import os
import datetime
import asyncio
import pytz

from tqdm import tqdm
import django

if sys.platform == 'darwin':
    sys.path.append('/Users/jeffchen/Documents/gitdir/dashboard')
elif sys.platform == 'win32':
    sys.path.append(r'D:\UserData\Documents\GitHub\dashboard')
else:
    sys.path.append('/home/cyh/bigbrother/dashboard')
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from trader.utils import is_trading_day, update_from_shfe, update_from_dce, update_from_czce, update_from_cffex, \
    create_main_all, fetch_from_quandl_all, clean_daily_bar, load_kt_data, calc_his_all, check_trading_day
from django.utils import timezone


async def fetch_bar():
    day_end = timezone.localtime()
    day_start = day_end - datetime.timedelta(days=365)
    tasks = []
    while day_start <= day_end:
        tasks.append(check_trading_day(day_start))
        day_start += datetime.timedelta(days=1)
    trading_days = []
    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        rst = await f
        trading_days.append(rst)
    tasks.clear()
    for day, trading in trading_days:
        if trading:
            tasks += [
                asyncio.ensure_future(update_from_shfe(day)),
                asyncio.ensure_future(update_from_dce(day)),
                asyncio.ensure_future(update_from_czce(day)),
                asyncio.ensure_future(update_from_cffex(day)),
            ]
    print('task len=', len(tasks))
    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await f


async def fetch_bar2():
    day_end = timezone.localtime()
    day_start = day_end - datetime.timedelta(days=365)
    while day_start <= day_end:
        day, trading = await check_trading_day(day_start)
        if trading:
            print('process ', day)
            tasks = [
                asyncio.ensure_future(update_from_shfe(day)),
                asyncio.ensure_future(update_from_dce(day)),
                asyncio.ensure_future(update_from_czce(day)),
                asyncio.ensure_future(update_from_cffex(day)),
            ]
            await asyncio.wait(tasks)
        day_start += datetime.timedelta(days=1)
    print('all done!')


# asyncio.get_event_loop().run_until_complete(fetch_bar2())
create_main_all()
# fetch_from_quandl_all()
# clean_dailybar()
# load_kt_data()
# calc_his_all(timezone.localtime()-datetime.timedelta(days=1))
