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

import asyncio
import re
from collections import defaultdict
import datetime
from decimal import Decimal
import logging
from django.db.models import Q, F, Sum
from django.utils import timezone
from talib import ATR
import ujson as json
import aioredis
from trader.strategy import BaseModule
from trader.utils.func_container import RegisterCallback
from trader.utils.read_config import config, ctp_errors
from trader.utils import ApiStruct, price_round, is_trading_day, update_from_shfe, update_from_dce, update_from_czce, update_from_cffex, \
    get_contracts_argument, calc_main_inst, str_to_number, get_next_id, ORDER_REF_SIGNAL_ID_START, update_from_gfex
from panel.models import *

logger = logging.getLogger('CTPApi')
HANDLER_TIME_OUT = config.getint('TRADE', 'command_timeout', fallback=10)


class TradeStrategy(BaseModule):
    def __init__(self, name: str):
        super().__init__()
        self.__market_response_format = config.get('MSG_CHANNEL', 'market_response_format')
        self.__trade_response_format = config.get('MSG_CHANNEL', 'trade_response_format')
        self.__request_format = config.get('MSG_CHANNEL', 'request_format')
        self.__ignore_inst_list = config.get('TRADE', 'ignore_inst', fallback="WH,bb,JR,RI,RS,LR,PM,im").split(',')
        self.__strategy = Strategy.objects.get(name=name)
        self.__inst_ids = self.__strategy.instruments.all().values_list('product_code', flat=True)
        self.__broker = self.__strategy.broker
        self.__fake = self.__broker.fake  # 虚拟资金
        self.__current = self.__broker.current  # 当前动态权益
        self.__pre_balance = self.__broker.pre_balance  # 静态权益
        self.__cash = self.__broker.cash  # 可用资金
        self.__shares = dict()  # { instrument : position }
        self.__cur_account = None
        self.__margin = self.__broker.margin  # 占用保证金
        self.__withdraw = 0  # 出金
        self.__deposit = 0  # 入金
        self.__activeOrders = dict()  # 未成交委托单
        self.__cur_pos = dict()  # 持有头寸
        self.__re_extract_code = re.compile(r'([a-zA-Z]*)(\d+)')  # 提合约字母部分 IF1509 -> IF
        self.__re_extract_name = re.compile('(.*?)([0-9]+)(.*?)$')  # 提取合约文字部分
        self.__trading_day = timezone.make_aware(datetime.datetime.strptime(self.raw_redis.get("TradingDay")+'08', '%Y%m%d%H'))
        self.__last_trading_day = timezone.make_aware(datetime.datetime.strptime(self.raw_redis.get("LastTradingDay")+'08', '%Y%m%d%H'))

    async def start(self):
        await self.install()
        self.raw_redis.set('HEARTBEAT:TRADER', 1, ex=61)
        today = timezone.localtime()
        now = int(today.strftime('%H%M'))
        if today.isoweekday() < 6 and (820 <= now <= 1550 or 2010 <= now <= 2359):  # 非交易时间查不到数据
            await self.refresh_account()
            order_list = await self.query('Order')
            for order in order_list:
                # 未成交订单
                if int(order['OrderStatus']) in range(1, 5) and order['OrderSubmitStatus'] == ApiStruct.OSS_Accepted:
                    direct_str = DirectionType.values[order['Direction']]
                    logger.info(f"撤销未成交订单: 合约{order['InstrumentID']} {direct_str}单 {order['VolumeTotal']}手 价格{order['LimitPrice']}")
                    await self.cancel_order(order)
                # 已成交订单
                elif order['OrderSubmitStatus'] == ApiStruct.OSS_Accepted:
                    self.save_order(order)
            await self.refresh_position()
        # today = timezone.make_aware(datetime.datetime.strptime(self.raw_redis.get('LastTradingDay'), '%Y%m%d'))
        # self.calculate(today, create_main_bar=False)
        # await self.processing_signal3()

    async def refresh_account(self):
        try:
            logger.debug('更新账户')
            account = await self.query('TradingAccount')
            account = account[0]
            self.__withdraw = Decimal(account['Withdraw'])
            self.__deposit = Decimal(account['Deposit'])
            # 虚拟=虚拟(原始)-入金+出金
            fake = self.__fake - self.__deposit + self.__withdraw
            if fake < 1:
                fake = 0
            # 静态权益=上日结算+入金金额-出金金额
            self.__pre_balance = Decimal(account['PreBalance']) + self.__deposit - self.__withdraw
            # 动态权益=静态权益+平仓盈亏+持仓盈亏-手续费
            self.__current = self.__pre_balance + Decimal(account['CloseProfit']) + Decimal(account['PositionProfit']) - Decimal(account['Commission'])
            self.__margin = Decimal(account['CurrMargin'])
            self.__cash = Decimal(account['Available'])
            self.__cur_account = account
            self.__broker.cash = self.__cash
            self.__broker.current = self.__current
            self.__broker.pre_balance = self.__pre_balance
            self.__broker.margin = self.__margin
            self.__broker.save(update_fields=['cash', 'current', 'pre_balance', 'margin'])
            logger.debug(f"更新账户,可用资金: {self.__cash:,.0f} 静态权益: {self.__pre_balance:,.0f} 动态权益: {self.__current:,.0f} "
                         f"出入金: {self.__withdraw - self.__deposit:,.0f} 虚拟: {fake:,.0f}")
        except Exception as e:
            logger.warning(f'refresh_account 发生错误: {repr(e)}', exc_info=True)

    async def refresh_position(self):
        try:
            logger.debug('更新持仓...')
            pos_list = await self.query('InvestorPositionDetail')
            self.__cur_pos.clear()
            for pos in pos_list:
                if 'empty' in pos and pos['empty'] is True:
                    continue
                if pos['Volume'] > 0:
                    old_pos = self.__cur_pos.get(pos['InstrumentID'])
                    if old_pos is None:
                        self.__cur_pos[pos['InstrumentID']] = pos
                    else:
                        old_pos['OpenPrice'] = (old_pos['OpenPrice'] * old_pos['Volume'] + pos['OpenPrice'] * pos['Volume']) / (old_pos['Volume'] + pos['Volume'])
                        old_pos['Volume'] += pos['Volume']
                        old_pos['PositionProfitByTrade'] += pos['PositionProfitByTrade']
                        old_pos['Margin'] += pos['Margin']
            Trade.objects.filter(~Q(code__in=self.__cur_pos.keys()), close_time__isnull=True).delete()  # 删除不存在的头寸
            for _, pos in self.__cur_pos.items():
                p_code = self.__re_extract_code.match(pos['InstrumentID']).group(1)
                inst = Instrument.objects.get(product_code=p_code)
                trade = Trade.objects.filter(broker=self.__broker, strategy=self.__strategy, instrument=inst, code=pos['InstrumentID'], close_time__isnull=True,
                                             direction=DirectionType.values[pos['Direction']]).first()
                bar = DailyBar.objects.filter(code=pos['InstrumentID']).order_by('-time').first()
                profit = (bar.close - Decimal(pos['OpenPrice'])) * pos['Volume'] * inst.volume_multiple
                if pos['Direction'] == DirectionType.values[DirectionType.SHORT]:
                    profit *= -1
                if trade:
                    trade.shares = (trade.closed_shares if trade.closed_shares else 0) + pos['Volume']
                    trade.filled_shares = trade.shares
                    trade.profit = profit
                    trade.save(update_fields=['shares', 'filled_shares', 'profit'])
                else:
                    Trade.objects.create(
                        broker=self.__broker, strategy=self.__strategy, instrument=inst, code=pos['InstrumentID'], profit=profit, filled_shares=pos['Volume'],
                        direction=DirectionType.values[pos['Direction']], avg_entry_price=Decimal(pos['OpenPrice']), shares=pos['Volume'],
                        open_time=timezone.make_aware(datetime.datetime.strptime(pos['OpenDate'] + '08', '%Y%m%d%H')), frozen_margin=Decimal(pos['Margin']),
                        cost=pos['Volume'] * Decimal(pos['OpenPrice']) * inst.fee_money * inst.volume_multiple + pos['Volume'] * inst.fee_volume)
            logger.debug('更新持仓完成!')
        except Exception as e:
            logger.warning(f'refresh_position 发生错误: {repr(e)}', exc_info=True)

    async def refresh_instrument(self):
        try:
            logger.debug("更新合约...")
            inst_dict = defaultdict(dict)
            inst_list = await self.query('Instrument')
            for inst in inst_list:
                if inst['empty']:
                    continue
                if inst['IsTrading'] == 1 and chr(inst['ProductClass']) == ApiStruct.PC_Futures and int(str_to_number(inst['StrikePrice'])) == 0:
                    if inst['ProductID'] in self.__ignore_inst_list or inst['LongMarginRatio'] > 1:
                        continue
                    inst_dict[inst['ProductID']][inst['InstrumentID']] = dict()
                    inst_dict[inst['ProductID']][inst['InstrumentID']]['name'] = inst['InstrumentName']
                    inst_dict[inst['ProductID']][inst['InstrumentID']]['exchange'] = inst['ExchangeID']
                    inst_dict[inst['ProductID']][inst['InstrumentID']]['multiple'] = inst['VolumeMultiple']
                    inst_dict[inst['ProductID']][inst['InstrumentID']]['price_tick'] = inst['PriceTick']
            for code in inst_dict.keys():
                all_inst = ','.join(sorted(inst_dict[code].keys()))
                inst_data = list(inst_dict[code].values())[0]
                valid_name = self.__re_extract_name.match(inst_data['name'])
                if valid_name is not None:
                    valid_name = valid_name.group(1)
                else:
                    valid_name = inst_data['name']
                if valid_name == code:
                    valid_name = ''
                inst_data['name'] = valid_name
                inst, created = Instrument.objects.update_or_create(product_code=code, exchange=inst_data['exchange'])
                print(f"inst:{inst} created:{created} main_code:{inst.main_code}")
                update_field_list = list()
                # 更新主力合约的保证金和手续费
                if inst.main_code:
                    margin_rate = await self.query('InstrumentMarginRate', InstrumentID=inst.main_code)
                    inst.margin_rate = margin_rate[0]['LongMarginRatioByMoney']
                    fee = await self.query('InstrumentCommissionRate', InstrumentID=inst.main_code)
                    inst.fee_money = Decimal(fee[0]['CloseRatioByMoney'])
                    inst.fee_volume = Decimal(fee[0]['CloseRatioByVolume'])
                    update_field_list += ['margin_rate', 'fee_money', 'fee_volume']
                if created:
                    inst.name = inst_data['name']
                    inst.volume_multiple = inst_data['multiple']
                    inst.price_tick = inst_data['price_tick']
                    update_field_list += ['name', 'volume_multiple', 'price_tick']
                elif inst.main_code:
                    inst.all_inst = all_inst
                    update_field_list.append('all_inst')
                inst.save(update_fields=update_field_list)
            logger.debug("更新合约完成!")
        except Exception as e:
            logger.warning(f'refresh_instrument 发生错误: {repr(e)}', exc_info=True)

    def getShares(self, instrument: str):
        # 这个函数只能处理持有单一方向仓位的情况，若同时持有多空的头寸，返回结果不正确
        shares = 0
        pos_price = 0
        for pos in self.__shares[instrument]:
            pos_price += pos['Volume'] * pos['OpenPrice']
            shares += pos['Volume'] * (-1 if pos['Direction'] == DirectionType.SHORT else 1)
        return shares, pos_price / abs(shares), self.__shares[instrument][0]['OpenDate']

    def getPositions(self, inst_id: int):
        # 这个函数只能处理持有单一方向仓位的情况，若同时持有多空的头寸，返回结果不正确
        return self.__shares[inst_id][0]

    def async_query(self, query_type: str, **kwargs):
        request_id = get_next_id()
        kwargs['RequestID'] = request_id
        self.raw_redis.publish(self.__request_format.format('ReqQry' + query_type), json.dumps(kwargs))

    @staticmethod
    async def query_reader(pb: aioredis.client.PubSub):
        msg_list = []
        async for msg in pb.listen():
            # print(f"query_reader msg: {msg}")
            msg_dict = json.loads(msg['data'])
            if 'empty' not in msg_dict or not msg_dict['empty']:
                msg_list.append(msg_dict)
            if 'bIsLast' not in msg_dict or msg_dict['bIsLast']:
                return msg_list

    async def query(self, query_type: str, **kwargs):
        sub_client = None
        channel_rsp_qry, channel_rsp_err = None, None
        try:
            sub_client = self.redis_client.pubsub(ignore_subscribe_messages=True)
            request_id = get_next_id()
            kwargs['RequestID'] = request_id
            channel_rsp_qry = self.__trade_response_format.format('OnRspQry' + query_type, request_id)
            channel_rsp_err = self.__trade_response_format.format('OnRspError', request_id)
            await sub_client.psubscribe(channel_rsp_qry, channel_rsp_err)
            task = asyncio.create_task(self.query_reader(sub_client))
            self.raw_redis.publish(self.__request_format.format('ReqQry' + query_type), json.dumps(kwargs))
            await asyncio.wait_for(task, HANDLER_TIME_OUT)
            await sub_client.punsubscribe()
            await sub_client.close()
            return task.result()
        except Exception as e:
            logger.warning(f'{query_type} 发生错误: {repr(e)}', exc_info=True)
            if sub_client and channel_rsp_qry:
                await sub_client.unsubscribe()
                await sub_client.close()
            return None

    async def SubscribeMarketData(self, inst_ids: list):
        sub_client = None
        channel_rsp_dat, channel_rsp_err = None, None
        try:
            sub_client = self.redis_client.pubsub(ignore_subscribe_messages=True)
            channel_rsp_dat = self.__market_response_format.format('OnRspSubMarketData', 0)
            channel_rsp_err = self.__market_response_format.format('OnRspError', 0)
            await sub_client.psubscribe(channel_rsp_dat, channel_rsp_err)
            task = asyncio.create_task(self.query_reader(sub_client))
            self.raw_redis.publish(self.__request_format.format('SubscribeMarketData'), json.dumps(inst_ids))
            await asyncio.wait_for(task, HANDLER_TIME_OUT)
            await sub_client.punsubscribe()
            await sub_client.close()
            return task.result()
        except Exception as e:
            logger.warning(f'SubscribeMarketData 发生错误: {repr(e)}', exc_info=True)
            if sub_client and sub_client.in_pubsub and channel_rsp_dat:
                await sub_client.unsubscribe()
                await sub_client.close()
            return None

    async def UnSubscribeMarketData(self, inst_ids: list):
        sub_client = None
        channel_rsp_dat, channel_rsp_err = None, None
        try:
            sub_client = self.redis_client.pubsub(ignore_subscribe_messages=True)
            channel_rsp_dat = self.__market_response_format.format('OnRspUnSubMarketData', 0)
            channel_rsp_err = self.__market_response_format.format('OnRspError', 0)
            await sub_client.psubscribe(channel_rsp_dat, channel_rsp_err)
            task = asyncio.create_task(self.query_reader(sub_client))
            self.raw_redis.publish(self.__request_format.format('UnSubscribeMarketData'), json.dumps(inst_ids))
            await asyncio.wait_for(task, HANDLER_TIME_OUT)
            await sub_client.punsubscribe()
            await sub_client.close()
            return task.result()
        except Exception as e:
            logger.warning(f'UnSubscribeMarketData 发生错误: {repr(e)}', exc_info=True)
            if sub_client and sub_client.in_pubsub and channel_rsp_dat:
                await sub_client.unsubscribe()
                await sub_client.close()
            return None

    def ReqOrderInsert(self, sig: Signal):
        try:
            request_id = get_next_id()
            autoid = Autonumber.objects.create()
            order_ref = f"{autoid.id:07}{sig.id:05}"
            param_dict = dict()
            param_dict['RequestID'] = request_id
            param_dict['OrderRef'] = order_ref
            param_dict['InstrumentID'] = sig.code
            param_dict['VolumeTotalOriginal'] = sig.volume
            param_dict['LimitPrice'] = float(sig.price)
            match sig.type:
                case SignalType.BUY | SignalType.SELL_SHORT:
                    param_dict['Direction'] = ApiStruct.D_Buy if sig.type == SignalType.BUY else ApiStruct.D_Sell
                    param_dict['CombOffsetFlag'] = ApiStruct.OF_Open
                    logger.info(f'{sig.instrument} {sig.type}{sig.volume}手 价格: {sig.price}')
                case SignalType.BUY_COVER | SignalType.SELL:
                    param_dict['Direction'] = ApiStruct.D_Buy if sig.type == SignalType.BUY_COVER else ApiStruct.D_Sell
                    param_dict['CombOffsetFlag'] = ApiStruct.OF_Close
                    pos = Trade.objects.filter(
                        broker=self.__broker, strategy=self.__strategy, code=sig.code, shares=sig.volume, close_time__isnull=True,
                        direction=DirectionType.values[DirectionType.SHORT] if sig.type == SignalType.BUY_COVER else DirectionType.values[
                            DirectionType.LONG]).first()
                    if pos.open_time.astimezone().date() == timezone.localtime().date() and pos.instrument.exchange == ExchangeType.SHFE:
                        param_dict['CombOffsetFlag'] = ApiStruct.OF_CloseToday  # 上期所区分平今和平昨
                    logger.info(f'{sig.instrument} {sig.type}{sig.volume}手 价格: {sig.price}')
                case SignalType.ROLL_CLOSE:
                    param_dict['CombOffsetFlag'] = ApiStruct.OF_Close
                    pos = Trade.objects.filter(broker=self.__broker, strategy=self.__strategy, code=sig.code, shares=sig.volume, close_time__isnull=True).first()
                    param_dict['Direction'] = ApiStruct.D_Sell if pos.direction == DirectionType.values[DirectionType.LONG] else ApiStruct.D_Buy
                    if pos.open_time.astimezone().date() == timezone.localtime().date() and pos.instrument.exchange == ExchangeType.SHFE:
                        param_dict['CombOffsetFlag'] = ApiStruct.OF_CloseToday  # 上期所区分平今和平昨
                    logger.info(f'{sig.code}->{sig.instrument.main_code} {pos.direction}头换月平旧{sig.volume}手 价格: {sig.price}')
                case SignalType.ROLL_OPEN:
                    param_dict['CombOffsetFlag'] = ApiStruct.OF_Open
                    pos = Trade.objects.filter(
                        Q(close_time__isnull=True) | Q(close_time__date__gte=timezone.localtime().now().date()),
                        broker=self.__broker, strategy=self.__strategy, code=sig.instrument.last_main, shares=sig.volume).first()
                    param_dict['Direction'] = ApiStruct.D_Buy if pos.direction == DirectionType.values[DirectionType.LONG] else ApiStruct.D_Sell
                    logger.info(f'{pos.code}->{sig.code} {pos.direction}头换月开新{sig.volume}手 价格: {sig.price}')
            self.raw_redis.publish(self.__request_format.format('ReqOrderInsert'), json.dumps(param_dict))
        except Exception as e:
            logger.warning(f'ReqOrderInsert 发生错误: {repr(e)}', exc_info=True)

    async def cancel_order(self, order: dict):
        sub_client = None
        channel_rsp_odr_act, channel_rsp_err = None, None
        try:
            sub_client = self.redis_client.pubsub(ignore_subscribe_messages=True)
            request_id = get_next_id()
            order['RequestID'] = request_id
            channel_rtn_odr = self.__trade_response_format.format('OnRtnOrder', order['OrderRef'])
            channel_rsp_odr_act = self.__trade_response_format.format('OnRspOrderAction', 0)
            channel_rsp_err = self.__trade_response_format.format('OnRspError', request_id)
            await sub_client.psubscribe(channel_rtn_odr, channel_rsp_odr_act, channel_rsp_err)
            task = asyncio.create_task(self.query_reader(sub_client))
            self.raw_redis.publish(self.__request_format.format('ReqOrderAction'), json.dumps(order))
            await asyncio.wait_for(task, HANDLER_TIME_OUT)
            await sub_client.punsubscribe()
            await sub_client.close()
            result = task.result()[0]
            if 'ErrorID' in result:
                logger.warning(f"撤销订单出错: {ctp_errors[result['ErrorID']]}")
                return False
            return True
        except Exception as e:
            logger.warning('cancel_order 发生错误: %s', repr(e), exc_info=True)
            if sub_client and sub_client.in_pubsub and channel_rsp_odr_act:
                await sub_client.unsubscribe()
                await sub_client.close()
            return False

    @RegisterCallback(channel='MSG:CTP:RSP:MARKET:OnRtnDepthMarketData:*')
    async def OnRtnDepthMarketData(self, channel, tick: dict):
        try:
            inst = channel.split(':')[-1]
            tick['UpdateTime'] = datetime.datetime.strptime(tick['UpdateTime'], "%Y%m%d %H:%M:%S:%f")
            logger.debug('inst=%s, tick: %s', inst, tick)
        except Exception as ee:
            logger.warning('OnRtnDepthMarketData 发生错误: %s', repr(ee), exc_info=True)

    @staticmethod
    def get_trade_string(trade: dict) -> str:
        if trade['OffsetFlag'] == OffsetFlag.Open:
            open_direct = DirectionType.values[trade['Direction']]
        else:
            open_direct = DirectionType.values[DirectionType.LONG] if trade['Direction'] == DirectionType.SHORT else DirectionType.values[DirectionType.SHORT]
        return f"{trade['ExchangeID']}.{trade['InstrumentID']} {OffsetFlag.values[trade['OffsetFlag']]}{open_direct}已成交{trade['Volume']}手 " \
               f"价格:{trade['Price']} 时间:{trade['TradeTime']} 订单号: {trade['OrderRef']}"

    @RegisterCallback(channel='MSG:CTP:RSP:TRADE:OnRtnTrade:*')
    async def OnRtnTrade(self, channel, trade: dict):
        try:
            signal = None
            new_trade = False
            trade_completed = False
            order_ref: str = channel.split(':')[-1]
            manual_trade = int(order_ref) < 10000
            if not manual_trade:
                signal = Signal.objects.get(id=int(order_ref[ORDER_REF_SIGNAL_ID_START:]))
            logger.info(f"成交回报: {self.get_trade_string(trade)}")
            inst = Instrument.objects.get(product_code=self.__re_extract_code.match(trade['InstrumentID']).group(1))
            order = Order.objects.filter(order_ref=order_ref, code=trade['InstrumentID']).order_by('-send_time').first()
            trade_cost = trade['Volume'] * Decimal(trade['Price']) * inst.fee_money * inst.volume_multiple + trade['Volume'] * inst.fee_volume
            trade_margin = trade['Volume'] * Decimal(trade['Price']) * inst.margin_rate
            now = timezone.localtime()
            trade_time = timezone.make_aware(datetime.datetime.strptime(trade['TradeDate'] + trade['TradeTime'], '%Y%m%d%H:%M:%S'))
            if trade_time.date() > now.date():
                trade_time.replace(year=now.year, month=now.month, day=now.day)
            if trade['OffsetFlag'] == OffsetFlag.Open:  # 开仓
                last_trade = Trade.objects.filter(
                    broker=self.__broker, strategy=self.__strategy, instrument=inst, code=trade['InstrumentID'], open_time__lte=trade_time,
                    close_time__isnull=True,
                    direction=DirectionType.values[trade['Direction']]).first() if manual_trade else Trade.objects.filter(open_order=order).first()
                # print(connection.queries[-1]['sql'])
                if last_trade is None:
                    new_trade = True
                    last_trade = Trade.objects.create(
                        broker=self.__broker, strategy=self.__strategy, instrument=inst, code=trade['InstrumentID'], open_order=order if order else None,
                        direction=DirectionType.values[trade['Direction']], open_time=trade_time, shares=order.volume if order else trade['Volume'],
                        cost=trade_cost, filled_shares=trade['Volume'], avg_entry_price=trade['Price'], frozen_margin=trade_margin)
                if order is None or order.status == OrderStatus.values[OrderStatus.AllTraded]:
                    trade_completed = True
                if (not new_trade and not manual_trade) or (trade_completed and not new_trade and manual_trade):
                    last_trade.avg_entry_price = (last_trade.avg_entry_price * last_trade.filled_shares + trade['Volume'] * Decimal(trade['Price'])) / \
                                                 (last_trade.filled_shares + trade['Volume'])
                    last_trade.filled_shares += trade['Volume']
                    if trade_completed and not new_trade and manual_trade:
                        last_trade.shares += trade['Volume']
                    last_trade.cost += trade_cost
                    last_trade.frozen_margin += trade_margin
                    last_trade.save()
            else:  # 平仓
                open_direct = DirectionType.values[DirectionType.LONG] if trade['Direction'] == DirectionType.SHORT else DirectionType.values[DirectionType.SHORT]
                last_trade = Trade.objects.filter(Q(closed_shares__isnull=True) | Q(closed_shares__lt=F('shares')), shares=F('filled_shares'),
                                                  broker=self.__broker, strategy=self.__strategy, instrument=inst, code=trade['InstrumentID'],
                                                  direction=open_direct).first()
                # print(connection.queries[-1]['sql'])
                logger.debug(f'trade={last_trade}')
                if last_trade:
                    if last_trade.closed_shares and last_trade.avg_exit_price:
                        last_trade.avg_exit_price = (last_trade.avg_exit_price * last_trade.closed_shares + trade['Volume'] * Decimal(trade['Price'])) / \
                                                    (last_trade.closed_shares + trade['Volume'])
                        last_trade.closed_shares += trade['Volume']
                    else:
                        last_trade.avg_exit_price = trade['Volume'] * Decimal(trade['Price']) / trade['Volume']
                        last_trade.closed_shares = trade['Volume']
                    last_trade.cost += trade_cost
                    last_trade.close_order = order
                    if last_trade.closed_shares == last_trade.shares:  # 全部成交
                        trade_completed = True
                        last_trade.close_time = trade_time
                        if last_trade.direction == DirectionType.values[DirectionType.LONG]:
                            profit_point = last_trade.avg_exit_price - last_trade.avg_entry_price
                        else:
                            profit_point = last_trade.avg_entry_price - last_trade.avg_exit_price
                        last_trade.profit = profit_point * last_trade.shares * inst.volume_multiple
                    last_trade.save(force_update=True)
            logger.debug(f"new_trade:{new_trade} manual_trade:{manual_trade} trade_completed:{trade_completed} "
                         f"order:{order} signal: {signal}")
            if trade_completed and not manual_trade:
                signal.processed = True
                signal.save(update_fields=['processed'])
                order.signal = signal
                order.save(update_fields=['signal'])
        except Exception as ee:
            logger.warning(f'OnRtnTrade 发生错误: {repr(ee)}', exc_info=True)

    @staticmethod
    def save_order(order: dict):
        try:
            if int(order['OrderRef']) < 10000:  # 非本程序生成订单
                return None, None
            signal = Signal.objects.get(id=int(order['OrderRef'][ORDER_REF_SIGNAL_ID_START:]))
            odr, created = Order.objects.update_or_create(
                code=order['InstrumentID'], order_ref=order['OrderRef'], defaults={
                    'broker': signal.strategy.broker, 'strategy': signal.strategy, 'instrument': signal.instrument, 'front': order['FrontID'],
                    'session': order['SessionID'], 'price': order['LimitPrice'], 'volume': order['VolumeTotalOriginal'],
                    'direction': DirectionType.values[order['Direction']], 'status': OrderStatus.values[order['OrderStatus']],
                    'offset_flag': CombOffsetFlag.values[order['CombOffsetFlag']], 'update_time': timezone.localtime(),
                    'send_time': timezone.make_aware(datetime.datetime.strptime(order['InsertDate'] + order['InsertTime'], '%Y%m%d%H:%M:%S'))})
            if order['OrderStatus'] == ApiStruct.OST_Canceled:  # 删除错误订单
                odr.delete()
                return None, None
            now = timezone.localtime().date()
            if created and odr.send_time.date() > timezone.localtime().date():  # 夜盘成交时返回的时间是下一个交易日，需要改成今天
                odr.send_time.replace(year=now.year, month=now.month, day=now.day)
                odr.save(update_fields=['send_time'])
            odr.signal = signal
            return odr, created
        except Exception as ee:
            logger.warning(f'save_order 发生错误: {repr(ee)}', exc_info=True)
            return None, None

    @staticmethod
    def get_order_string(order: dict) -> str:
        off_set_flag = CombOffsetFlag.values[order['CombOffsetFlag']] if order['CombOffsetFlag'] in CombOffsetFlag.values else \
            OffsetFlag.values[order['CombOffsetFlag']]
        order_str = f"订单号:{order['OrderRef']},{order['ExchangeID']}.{order['InstrumentID']} {off_set_flag}{DirectionType.values[order['Direction']]}" \
                    f"{order['VolumeTotalOriginal']}手 价格:{order['LimitPrice']} 报单时间:{order['InsertTime']} " \
                    f"提交状态:{OrderSubmitStatus.values[order['OrderSubmitStatus']]} "
        if order['OrderStatus'] != OrderStatus.Unknown:
            order_str += f"成交状态:{OrderStatus.values[order['OrderStatus']]} 消息:{order['StatusMsg']} "
            if order['OrderStatus'] == OrderStatus.PartTradedQueueing:
                order_str += f"成交数量:{order['VolumeTraded']} 剩余数量:{order['VolumeTotal']}"
        return order_str

    @RegisterCallback(channel='MSG:CTP:RSP:TRADE:OnRtnOrder:*')
    async def OnRtnOrder(self, _: str, order: dict):
        try:
            if order["OrderSysID"]:
                logger.debug(f"订单回报: {self.get_order_string(order)}")
            order_obj, _ = self.save_order(order)
            if not order_obj:
                return
            signal = order_obj.signal
            inst = Instrument.objects.get(product_code=self.__re_extract_code.match(order['InstrumentID']).group(1))
            # 处理由于委托价格超出交易所涨跌停板而被撤单的报单，将委托价格下调50%，重新报单
            if order['OrderStatus'] == OrderStatus.Canceled and order['OrderSubmitStatus'] == OrderSubmitStatus.InsertRejected:
                last_bar = DailyBar.objects.filter(exchange=inst.exchange, code=order['InstrumentID']).order_by('-time').first()
                volume = int(order['VolumeTotalOriginal'])
                price = Decimal(order['LimitPrice'])
                if order['CombOffsetFlag'] == CombOffsetFlag.Open:
                    if order['Direction'] == DirectionType.LONG:
                        delta = (price - last_bar.settlement) * Decimal(0.5)
                        price = price_round(last_bar.settlement + delta, inst.price_tick)
                        if delta / last_bar.settlement < 0.01:
                            logger.warning(f"{inst} 新价格: {price} 过低难以成交，放弃报单!")
                            return
                        logger.info(f"{inst} 以价格 {price} 开多{volume}手 重新报单...")
                        signal.price = price
                        self.io_loop.call_soon(self.ReqOrderInsert, signal)
                    else:
                        delta = (last_bar.settlement - price) * Decimal(0.5)
                        price = price_round(last_bar.settlement - delta, inst.price_tick)
                        if delta / last_bar.settlement < 0.01:
                            logger.warning(f"{inst} 新价格: {price} 过低难以成交，放弃报单!")
                            return
                        logger.info(f"{inst} 以价格 {price} 开空{volume}手 重新报单...")
                        signal.price = price
                        self.io_loop.call_soon(self.ReqOrderInsert, signal)
                else:
                    if order['Direction'] == DirectionType.LONG:
                        delta = (price - last_bar.settlement) * Decimal(0.5)
                        price = price_round(last_bar.settlement + delta, inst.price_tick)
                        if delta / last_bar.settlement < 0.01:
                            logger.warning(f"{inst} 新价格: {price} 过低难以成交，放弃报单!")
                            return
                        logger.info(f"{inst} 以价格 {price} 买平{volume}手 重新报单...")
                        signal.price = price
                        self.io_loop.call_soon(self.ReqOrderInsert, signal)
                    else:
                        delta = (last_bar.settlement - price) * Decimal(0.5)
                        price = price_round(last_bar.settlement - delta, inst.price_tick)
                        if delta / last_bar.settlement < 0.01:
                            logger.warning(f"{inst} 新价格: {price} 过低难以成交，放弃报单!")
                            return
                        logger.info(f"{inst} 以价格 {price} 卖平{volume}手 重新报单...")
                        signal.price = price
                        self.io_loop.call_soon(self.ReqOrderInsert, signal)
        except Exception as ee:
            logger.warning(f'OnRtnOrder 发生错误: {repr(ee)}', exc_info=True)

    @RegisterCallback(crontab='*/1 * * * *')
    async def heartbeat(self):
        self.raw_redis.set('HEARTBEAT:TRADER', 1, ex=301)

    @RegisterCallback(crontab='55 8 * * *')
    async def processing_signal1(self):
        await asyncio.sleep(5)
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if trading:
            logger.debug('查询日盘信号..')
            for sig in Signal.objects.filter(~Q(instrument__exchange=ExchangeType.CFFEX), trigger_time__gte=self.__last_trading_day, strategy=self.__strategy,
                                             instrument__night_trade=False, processed=False).order_by('-priority'):
                logger.info(f'发现日盘信号: {sig}')
                self.io_loop.call_soon(self.ReqOrderInsert, sig)
            if (self.__trading_day - self.__last_trading_day).days > 3:
                logger.info(f'假期后第一天，处理节前未成交夜盘信号.')
                self.io_loop.call_soon(asyncio.create_task, self.processing_signal3())

    @RegisterCallback(crontab='1 9 * * *')
    async def check_signal1_processed(self):
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if trading:
            logger.debug('查询遗漏的日盘信号..')
            for sig in Signal.objects.filter(~Q(instrument__exchange=ExchangeType.CFFEX), trigger_time__gte=self.__last_trading_day, strategy=self.__strategy,
                                             instrument__night_trade=False, processed=False).order_by('-priority'):
                logger.info(f'发现遗漏信号: {sig}')
                self.io_loop.call_soon(self.ReqOrderInsert, sig)

    @RegisterCallback(crontab='25 9 * * *')
    async def processing_signal2(self):
        await asyncio.sleep(5)
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if trading:
            logger.debug('查询股指和国债信号..')
            for sig in Signal.objects.filter(instrument__exchange=ExchangeType.CFFEX, trigger_time__gte=self.__last_trading_day, strategy=self.__strategy,
                                             instrument__night_trade=False, processed=False).order_by('-priority'):
                logger.info(f'发现股指和国债信号: {sig}')
                self.io_loop.call_soon(self.ReqOrderInsert, sig)

    @RegisterCallback(crontab='31 9 * * *')
    async def check_signal2_processed(self):
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if trading:
            logger.debug('查询遗漏的股指和国债信号..')
            for sig in Signal.objects.filter(instrument__exchange=ExchangeType.CFFEX, trigger_time__gte=self.__last_trading_day, strategy=self.__strategy,
                                             instrument__night_trade=False, processed=False).order_by('-priority'):
                logger.info(f'发现遗漏的股指和国债信号: {sig}')
                self.io_loop.call_soon(self.ReqOrderInsert, sig)

    @RegisterCallback(crontab='55 20 * * *')
    async def processing_signal3(self):
        await asyncio.sleep(5)
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if trading:
            logger.debug('查询夜盘信号..')
            for sig in Signal.objects.filter(
                    trigger_time__gte=self.__last_trading_day, strategy=self.__strategy, instrument__night_trade=True, processed=False).order_by('-priority'):
                logger.info(f'发现夜盘信号: {sig}')
                self.io_loop.call_soon(self.ReqOrderInsert, sig)

    @RegisterCallback(crontab='1 21 * * *')
    async def check_signal3_processed(self):
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if trading:
            logger.debug('查询遗漏的夜盘信号..')
            for sig in Signal.objects.filter(
                    trigger_time__gte=self.__last_trading_day, strategy=self.__strategy, instrument__night_trade=True, processed=False).order_by('-priority'):
                logger.info(f'发现遗漏的夜盘信号: {sig}')
                self.io_loop.call_soon(self.ReqOrderInsert, sig)

    @RegisterCallback(crontab='20 15 * * *')
    async def refresh_all(self):
        day = timezone.localtime()
        _, trading = await is_trading_day(day)
        if not trading:
            logger.info('今日是非交易日, 不更新任何数据。')
            return
        await self.refresh_account()
        await self.refresh_position()
        await self.refresh_instrument()
        logger.debug('全部更新完成!')

    @RegisterCallback(crontab='30 15 * * *')
    async def update_equity(self):
        today, trading = await is_trading_day(timezone.localtime())
        if trading:
            dividend = Performance.objects.filter(
                broker=self.__broker, day__lt=today.date()).aggregate(Sum('dividend'))['dividend__sum']
            if dividend is None:
                dividend = Decimal(0)
            dividend = dividend + self.__deposit - self.__withdraw
            # 虚拟=虚拟(原始)-入金+出金
            self.__fake = self.__fake - self.__deposit + self.__withdraw
            if self.__fake < 1:
                self.__fake = 0
            self.__broker.fake = self.__fake
            self.__broker.save(update_fields=['fake'])
            unit = dividend + self.__fake
            nav = (self.__current + self.__fake) / unit  # 单位净值
            accumulated = self.__current / (unit - self.__fake)  # 累计净值
            Performance.objects.update_or_create(broker=self.__broker, day=today.date(), defaults={
                'used_margin': self.__margin, 'dividend': self.__deposit - self.__withdraw, 'fake': self.__fake, 'capital': self.__current, 'unit_count': unit,
                'NAV': nav, 'accumulated': accumulated})
            logger.info(f"动态权益: {self.__current:,.0f}({self.__current/10000:.1f}万) "
                        f"静态权益: {self.__pre_balance:,.0f}({self.__pre_balance/10000:.1f}万) "
                        f"可用资金: {self.__cash:,.0f}({self.__cash/10000:.1f}万) "
                        f"保证金占用: {self.__margin:,.0f}({self.__margin/10000:.1f}万) "
                        f"虚拟资金: {self.__fake:,.0f}({self.__fake/10000:.1f}万) 当日入金: {self.__deposit:,.0f} "
                        f"当日出金: {self.__withdraw:,.0f} 单位净值: {nav:,.2f} 累计净值: {accumulated:,.2f}")

    @RegisterCallback(crontab='0 17 * * *')
    async def collect_quote(self, tasks=None):
        try:
            day = timezone.localtime()
            _, trading = await is_trading_day(day)
            if not trading:
                logger.info('今日是非交易日, 不计算任何数据。')
                return
            logger.debug(f'{day}盘后计算,获取交易所日线数据..')
            if tasks is None:
                tasks = [update_from_shfe, update_from_dce, update_from_czce, update_from_cffex, update_from_gfex, get_contracts_argument]
            result = await asyncio.gather(*[func(day) for func in tasks], return_exceptions=True)
            if all(result):
                self.io_loop.call_soon(self.calculate, day)
            else:
                failed_tasks = [tasks[i] for i, rst in enumerate(result) if not rst]
                self.io_loop.call_later(10*60, asyncio.create_task, self.collect_quote(failed_tasks))
        except Exception as e:
            logger.warning(f'collect_quote 发生错误: {repr(e)}', exc_info=True)
        logger.debug('盘后计算完毕!')

    def calculate(self, day, create_main_bar=True):
        try:
            p_code_set = set(self.__inst_ids)
            for code in self.__cur_pos.keys():
                p_code_set.add(self.__re_extract_code.match(code).group(1))
            all_margin = 0
            for inst in Instrument.objects.all().order_by('section', 'exchange', 'name'):
                if create_main_bar:
                    logger.debug(f'生成连续合约: {inst.name}')
                    calc_main_inst(inst, day)
                if inst.product_code in p_code_set:
                    logger.debug(f'计算交易信号: {inst.name}')
                    sig, margin = self.calc_signal(inst, day)
                    all_margin += margin
            if (all_margin + self.__margin) / self.__current > 0.8:
                logger.info(f"！！！风险提示！！！开仓保证金共计: {all_margin:.0f}({all_margin/10000:.1f}万) "
                            f"账户风险度将达到: {100 * (all_margin + self.__margin) / self.__current:.0f}% 建议追加保证金或减少开仓手数！")
        except Exception as e:
            logger.warning(f'calculate 发生错误: {repr(e)}', exc_info=True)

    def calc_signal(self, inst: Instrument, day: datetime.datetime) -> (Signal, Decimal):
        try:
            break_n = self.__strategy.param_set.get(code='BreakPeriod').int_value
            atr_n = self.__strategy.param_set.get(code='AtrPeriod').int_value
            long_n = self.__strategy.param_set.get(code='LongPeriod').int_value
            short_n = self.__strategy.param_set.get(code='ShortPeriod').int_value
            stop_n = self.__strategy.param_set.get(code='StopLoss').int_value
            risk = self.__strategy.param_set.get(code='Risk').float_value
            # 只读取最近400条记录，减少运算量
            df = to_df(MainBar.objects.filter(time__lte=day.date(), exchange=inst.exchange, product_code=inst.product_code).order_by('-time').values_list(
                'time', 'open', 'high', 'low', 'close')[:400], index_col='time', parse_dates=['time'])
            df = df.iloc[::-1]  # 日期升序排列
            df["atr"] = ATR(df.high, df.low, df.close, timeperiod=atr_n)
            df["short_trend"] = df.close
            df["long_trend"] = df.close
            for idx in range(1, df.shape[0]):  # 手动计算SMA
                df.short_trend[idx] = (df.short_trend[idx-1] * (short_n - 1) + df.close[idx]) / short_n
                df.long_trend[idx] = (df.long_trend[idx-1] * (long_n - 1) + df.close[idx]) / long_n
            df["high_line"] = df.close.rolling(window=break_n).max()
            df["low_line"] = df.close.rolling(window=break_n).min()
            idx = -1
            buy_sig = df.short_trend[idx] > df.long_trend[idx] and price_round(df.close[idx], inst.price_tick) >= price_round(df.high_line[idx - 1], inst.price_tick)
            sell_sig = df.short_trend[idx] < df.long_trend[idx] and price_round(df.close[idx], inst.price_tick) <= price_round(df.low_line[idx - 1], inst.price_tick)
            pos = Trade.objects.filter(close_time__isnull=True, broker=self.__broker, strategy=self.__strategy, instrument=inst, shares__gt=0).first()
            roll_over = False
            if pos:
                roll_over = pos.code != inst.main_code and pos.code < inst.main_code
            elif self.__strategy.force_opens.filter(id=inst.id).exists() and not buy_sig and not sell_sig:
                logger.info(f'强制开仓: {inst}')
                if df.short_trend[idx] > df.long_trend[idx]:
                    buy_sig = True
                else:
                    sell_sig = True
                self.__strategy.force_opens.remove(inst)
            signal = signal_code = price = volume = volume_ori = use_margin = None
            priority = PriorityType.LOW
            if pos:
                # 多头持仓
                if pos.direction == DirectionType.values[DirectionType.LONG]:
                    first_pos = pos
                    while hasattr(first_pos, 'open_order') and first_pos.open_order and first_pos.open_order.signal and first_pos.open_order.signal.type == \
                            SignalType.ROLL_OPEN:
                        last_pos = Trade.objects.filter(
                            close_order__signal__type=SignalType.ROLL_CLOSE, instrument=first_pos.instrument, strategy=first_pos.strategy,
                            shares=first_pos.shares, direction=first_pos.direction, close_time__date=first_pos.open_time.date()).first()
                        if last_pos is None:
                            break
                        logger.debug(f"发现换月前持仓:{last_pos} 开仓时间: {last_pos.open_time}")
                        first_pos = last_pos
                    pos_idx = df.index.get_loc(first_pos.open_time.astimezone().date().isoformat())
                    # 多头止损
                    if df.close[idx] <= df.high[pos_idx:idx].max() - df.atr[pos_idx - 1] * stop_n:
                        signal = SignalType.SELL
                        signal_code = pos.code
                        volume = pos.shares
                        last_bar = DailyBar.objects.filter(exchange=inst.exchange, code=pos.code, time=day.date()).first()
                        price = self.calc_down_limit(inst, last_bar)
                        priority = PriorityType.High
                    # 多头换月
                    elif roll_over:
                        signal = SignalType.ROLL_OPEN
                        volume = pos.shares
                        last_bar = DailyBar.objects.filter(exchange=inst.exchange, code=pos.code, time=day.date()).first()
                        new_bar = DailyBar.objects.filter(exchange=inst.exchange, code=inst.main_code, time=day.date()).first()
                        price = self.calc_up_limit(inst, new_bar)
                        priority = PriorityType.Normal
                        Signal.objects.update_or_create(
                            code=pos.code, strategy=self.__strategy, instrument=inst, type=SignalType.ROLL_CLOSE, trigger_time=day,
                            defaults={'price': self.calc_down_limit(inst, last_bar), 'volume': volume, 'priority': priority, 'processed': False})
                # 空头持仓
                else:
                    first_pos = pos
                    while hasattr(first_pos, 'open_order') and first_pos.open_order and first_pos.open_order.signal \
                            and first_pos.open_order.signal.type == SignalType.ROLL_OPEN:
                        last_pos = Trade.objects.filter(
                            close_order__signal__type=SignalType.ROLL_CLOSE, instrument=first_pos.instrument, strategy=first_pos.strategy,
                            shares=first_pos.shares, direction=first_pos.direction,close_time__date=first_pos.open_time.date()).first()
                        if last_pos is None:
                            break
                        logger.debug(f"发现换月前持仓:{last_pos} 开仓时间: {last_pos.open_time}")
                        first_pos = last_pos
                    pos_idx = df.index.get_loc(first_pos.open_time.astimezone().date().isoformat())
                    # 空头止损
                    if df.close[idx] >= df.low[pos_idx:idx].min() + df.atr[pos_idx - 1] * stop_n:
                        signal = SignalType.BUY_COVER
                        signal_code = pos.code
                        volume = pos.shares
                        last_bar = DailyBar.objects.filter(exchange=inst.exchange, code=pos.code, time=day.date()).first()
                        price = self.calc_up_limit(inst, last_bar)
                        priority = PriorityType.High
                    # 空头换月
                    elif roll_over:
                        signal = SignalType.ROLL_OPEN
                        volume = pos.shares
                        last_bar = DailyBar.objects.filter(exchange=inst.exchange, code=pos.code, time=day.date()).first()
                        new_bar = DailyBar.objects.filter(exchange=inst.exchange, code=inst.main_code, time=day.date()).first()
                        price = self.calc_down_limit(inst, new_bar)
                        priority = PriorityType.Normal
                        Signal.objects.update_or_create(
                            code=pos.code, strategy=self.__strategy, instrument=inst, type=SignalType.ROLL_CLOSE, trigger_time=day,
                            defaults={'price': self.calc_up_limit(inst, last_bar), 'volume': volume, 'priority': priority, 'processed': False})
            # 开新仓
            elif buy_sig or sell_sig:
                start_cash = Performance.objects.last().unit_count
                # 原始扎堆儿
                profit = Trade.objects.filter(strategy=self.__strategy, instrument__section=inst.section).aggregate(sum=Sum('profit'))['sum']
                profit = profit if profit else 0
                risk_each = Decimal(df.atr[idx]) * Decimal(inst.volume_multiple)
                volume_ori = (start_cash + profit) * risk / risk_each
                volume = round(volume_ori)
                print(f"{inst}: ({start_cash:,.0f} + {profit:,.0f}) / {risk_each:,.0f} = {volume_ori}")
                if volume > 0:
                    new_bar = DailyBar.objects.filter(exchange=inst.exchange, code=inst.main_code, time=day.date()).first()
                    use_margin = new_bar.settlement * inst.volume_multiple * inst.margin_rate * volume
                    price = self.calc_up_limit(inst, new_bar) if buy_sig else self.calc_down_limit(inst, new_bar)
                    signal = SignalType.BUY if buy_sig else SignalType.SELL_SHORT
                else:
                    logger.info(f"做{'多' if buy_sig else '空'}{inst},单手风险:{risk_each:.0f},超出风控额度，放弃。")
            if signal:
                use_margin = use_margin if use_margin else 0
                sig, _ = Signal.objects.update_or_create(
                    code=signal_code if signal_code else inst.main_code,strategy=self.__strategy, instrument=inst, type=signal, trigger_time=day,
                    defaults={'price': price, 'volume': volume, 'priority': priority, 'processed': False})
                volume_ori = volume_ori if volume_ori else volume
                logger.info(f"新信号: {sig}({volume_ori:.1f}手) "
                            f"预估保证金: {use_margin:.0f}({use_margin/10000:.1f}万)")
                return signal, use_margin
        except Exception as e:
            logger.warning(f'calc_signal 发生错误: {repr(e)}', exc_info=True)
        return None, 0

    def calc_up_limit(self, inst: Instrument, bar: DailyBar):
        settlement = bar.settlement
        limit_ratio = str_to_number(self.raw_redis.get(f"LIMITRATIO:{inst.exchange}:{inst.product_code}:{bar.code}"))
        price_tick = inst.price_tick
        price = price_round(settlement * (Decimal(1) + Decimal(limit_ratio)), price_tick)
        return price - price_tick

    def calc_down_limit(self, inst: Instrument, bar: DailyBar):
        settlement = bar.settlement
        limit_ratio = str_to_number(self.raw_redis.get(f"LIMITRATIO:{inst.exchange}:{inst.product_code}:{bar.code}"))
        price_tick = inst.price_tick
        price = price_round(settlement * (Decimal(1) - Decimal(limit_ratio)), price_tick)
        return price + price_tick
