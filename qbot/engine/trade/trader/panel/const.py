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
from djchoices import DjangoChoices, C


class ContractType(DjangoChoices):
    STOCK = C(label='股票')
    FUTURE = C(label='期货')
    OPTION = C(label='期权')


class ExchangeType(DjangoChoices):
    SHFE = C(value='SHFE', label='上期所')
    DCE = C(value='DCE', label='大商所')
    CZCE = C(value='CZCE', label='郑商所')
    CFFEX = C(value='CFFEX', label='中金所')
    INE = C(value='INE', label='上期能源')
    GFEX = C(value='GFEX', label='广交所')


class SectionType(DjangoChoices):
    Stock = C(label='股票')
    Bond = C(label='债券')
    Metal = C(label='基本金属')
    Agricultural = C(label='农产品')
    EnergyChemical = C(label='能源化工')
    BlackMaterial = C(label='黑色建材')


class SortType(DjangoChoices):
    Stock = C(label='股票')
    Bond = C(label='债券')
    Rare = C(label='贵金属')
    Metal = C(label='基本金属')
    EdibleOil = C(label='食用油')
    Feed = C(label='动物饲料')
    Cotton = C(label='棉')
    EnergyChemical = C(label='能源化工')
    BlackMaterial = C(label='黑色建材')


class AddressType(DjangoChoices):
    TRADE = C(label='交易')
    MARKET = C(label='行情')


class OperatorType(DjangoChoices):
    TELECOM = C(label='电信')
    UNICOM = C(label='联通')


class DirectionType(DjangoChoices):
    LONG = C(label='多', value=b'0'[0])
    SHORT = C(label='空', value=b'1'[0])


class CombOffsetFlag(DjangoChoices):  # 订单开平标志
    Open = C(label='开', value='0')
    Close = C(label='平', value='1')
    ForceClose = C(label='强平', value='2')
    CloseToday = C(label='平', value='3')
    CloseYesterday = C(label='平昨', value='4')
    ForceOff = C(label='强减', value='5')
    LocalForceClose = C(label='本地强平', value='6')


class OffsetFlag(DjangoChoices):  # 开平标志
    Open = C(label='开', value=b'0'[0])
    Close = C(label='平', value=b'1'[0])
    ForceClose = C(label='强平', value=b'2'[0])
    CloseToday = C(label='平今', value=b'3'[0])
    CloseYesterday = C(label='平昨', value=b'4'[0])
    ForceOff = C(label='强减', value=b'5'[0])
    LocalForceClose = C(label='本地强平', value=b'6'[0])


class OrderStatus(DjangoChoices):  # 报单状态
    AllTraded = C(value=b'0'[0], label='全部成交')
    PartTradedQueueing = C(value=b'1'[0], label='部分成交还在队列中')
    PartTradedNotQueueing = C(value=b'2'[0], label='部分成交不在队列中')
    NoTradeQueueing = C(value=b'3'[0], label='未成交还在队列中')
    NoTradeNotQueueing = C(value=b'4'[0], label='未成交不在队列中')
    Canceled = C(value=b'5'[0], label='撤单')
    Unknown = C(value=b'a'[0], label='未知')
    NotTouched = C(value=b'b'[0], label='尚未触发')
    Touched = C(value=b'c'[0], label='已触发')


class OrderSubmitStatus(DjangoChoices):  # 报单提交状态
    InsertSubmitted = C(value=b'0'[0], label='已经提交')
    CancelSubmitted = C(value=b'1'[0], label='撤单已经提交')
    ModifySubmitted = C(value=b'2'[0], label='修改已经提交')
    Accepted = C(value=b'3'[0], label='已经接受')
    InsertRejected = C(value=b'4'[0], label='报单已经被拒绝')
    CancelRejected = C(value=b'5'[0], label='撤单已经被拒绝')
    ModifyRejected = C(value=b'6'[0], label='改单已经被拒绝')


DCE_NAME_CODE = {
    '豆一': 'a',
    '豆二': 'b',
    '胶合板': 'bb',
    '玉米': 'c',
    '玉米淀粉': 'cs',
    '纤维板': 'fb',
    '铁矿石': 'i',
    '焦炭': 'j',
    '鸡蛋': 'jd',
    '焦煤': 'jm',
    '聚乙烯': 'l',
    '豆粕': 'm',
    '棕榈油': 'p',
    '聚丙烯': 'pp',
    '聚氯乙烯': 'v',
    '苯乙烯': 'eb',
    '乙二醇': 'eg',
    '液化石油气': 'pg',
    '生猪': 'lh',
    '粳米': 'rr',
    '豆油': 'y',
}

MONTH_CODE = {
    1: "F",
    2: "G",
    3: "H",
    4: "J",
    5: "K",
    6: "M",
    7: "N",
    8: "Q",
    9: "U",
    10: "V",
    11: "X",
    12: "Z"
}


KT_MARKET = {
    'DL': 'DCE',
    'DY': 'DCE',
    'SQ': 'SHFE',
    'SY': 'SHFE',
    'ZJ': 'CFFEX',
    'ZZ': 'CZCE',
    'ZY': 'CZCE',
}


class SignalType(DjangoChoices):
    ROLL_CLOSE = C(label='换月平旧')
    ROLL_OPEN = C(label='换月开新')
    BUY = C(label='买开')
    SELL_SHORT = C(label='卖开')
    SELL = C(label='卖平')
    BUY_COVER = C(label='买平')


class PriorityType(DjangoChoices):
    LOW = C(label='低', value=0)
    Normal = C(label='普通', value=1)
    High = C(label='高', value=2)
