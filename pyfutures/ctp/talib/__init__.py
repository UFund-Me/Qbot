# -*- coding: utf-8 -*-

from __future__ import absolute_import as _init

__author__ = 'lovelylain'
__version__ = '0.2.0'

class TAError(Exception):
    pass

class TAFunc(object):
    __slots__ = ('inputs', 'outputs', 'params', 'lookback', 'size')
    def __call__(self, stop, start=-1):
        return 0
    @classmethod
    def C(cls, *a, **kw):
        """C(cls, *a, **kw) -> (outNBElement, outputs...)
        calculate result on all inputs and return the result
        """
        self = cls(*a, **kw)
        return (self(self.size, 0),) + self.outputs

class ACOS(TAFunc):
    """ACOS(real) -> Acos
    Acos(stop, start=-1) -> outNBElement

    Vector Trigonometric ACos (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class AD(TAFunc):
    """AD(high, low, close, volume) -> Ad
    Ad(stop, start=-1) -> outNBElement

    Chaikin A/D Line (Volume Indicators)
    Inputs: [high, low, close, volume]
    Outputs: (outReal,d)
    """
    __slots__ = ('high', 'low', 'close', 'volume', 'outReal')
    def __init__(self, high, low, close, volume):
        pass

class ADD(TAFunc):
    """ADD(real0, real1) -> Add
    Add(stop, start=-1) -> outNBElement

    Vector Arithmetic Add (Math Operators)
    Inputs: real0, real1
    Outputs: (outReal,d)
    """
    __slots__ = ('real0', 'real1', 'outReal')
    def __init__(self, real0, real1):
        pass

class ADOSC(TAFunc):
    """ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10) -> AdOsc
    AdOsc(stop, start=-1) -> outNBElement

    Chaikin A/D Oscillator (Volume Indicators)
    Inputs: [high, low, close, volume]
    Outputs: (outReal,d)
    Parameters:
      fastperiod: Fast Period (2 <= i <= 100000)
        Number of period for the fast MA
      slowperiod: Slow Period (2 <= i <= 100000)
        Number of period for the slow MA
    """
    __slots__ = ('high', 'low', 'close', 'volume', 'outReal', 'fastperiod', 'slowperiod')
    def __init__(self, high, low, close, volume, fastperiod=3, slowperiod=10):
        pass

class ADX(TAFunc):
    """ADX(high, low, close, timeperiod=14) -> Adx
    Adx(stop, start=-1) -> outNBElement

    Average Directional Movement Index (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class ADXR(TAFunc):
    """ADXR(high, low, close, timeperiod=14) -> Adxr
    Adxr(stop, start=-1) -> outNBElement

    Average Directional Movement Index Rating (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class APO(TAFunc):
    """APO(real, fastperiod=12, slowperiod=26, matype=0) -> Apo
    Apo(stop, start=-1) -> outNBElement

    Absolute Price Oscillator (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      fastperiod: Fast Period (2 <= i <= 100000)
        Number of period for the fast MA
      slowperiod: Slow Period (2 <= i <= 100000)
        Number of period for the slow MA
      matype: MA Type
        Type of Moving Average
    """
    __slots__ = ('real', 'outReal', 'fastperiod', 'slowperiod', 'matype')
    def __init__(self, real, fastperiod=12, slowperiod=26, matype=0):
        pass

class AROON(TAFunc):
    """AROON(high, low, timeperiod=14) -> Aroon
    Aroon(stop, start=-1) -> outNBElement

    Aroon (Momentum Indicators)
    Inputs: [high, low]
    Outputs: (outAroonDown,d), (outAroonUp,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'outAroonDown', 'outAroonUp', 'timeperiod')
    def __init__(self, high, low, timeperiod=14):
        pass

class AROONOSC(TAFunc):
    """AROONOSC(high, low, timeperiod=14) -> AroonOsc
    AroonOsc(stop, start=-1) -> outNBElement

    Aroon Oscillator (Momentum Indicators)
    Inputs: [high, low]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'outReal', 'timeperiod')
    def __init__(self, high, low, timeperiod=14):
        pass

class ASIN(TAFunc):
    """ASIN(real) -> Asin
    Asin(stop, start=-1) -> outNBElement

    Vector Trigonometric ASin (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class ATAN(TAFunc):
    """ATAN(real) -> Atan
    Atan(stop, start=-1) -> outNBElement

    Vector Trigonometric ATan (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class ATR(TAFunc):
    """ATR(high, low, close, timeperiod=14) -> Atr
    Atr(stop, start=-1) -> outNBElement

    Average True Range (Volatility Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class AVGPRICE(TAFunc):
    """AVGPRICE(open, high, low, close) -> AvgPrice
    AvgPrice(stop, start=-1) -> outNBElement

    Average Price (Price Transform)
    Inputs: [open, high, low, close]
    Outputs: (outReal,d)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outReal')
    def __init__(self, open, high, low, close):
        pass

class BBANDS(TAFunc):
    """BBANDS(real, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0) -> Bbands
    Bbands(stop, start=-1) -> outNBElement

    Bollinger Bands (Overlap Studies)
    Inputs: real
    Outputs: (outUpperBand,d), (outMiddleBand,d), (outLowerBand,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
      nbdevup: Deviations up (REAL_MIN <= d <= REAL_MAX)
        Deviation multiplier for upper band
      nbdevdn: Deviations down (REAL_MIN <= d <= REAL_MAX)
        Deviation multiplier for lower band
      matype: MA Type
        Type of Moving Average
    """
    __slots__ = ('real', 'outUpperBand', 'outMiddleBand', 'outLowerBand', 'timeperiod', 'nbdevup', 'nbdevdn', 'matype')
    def __init__(self, real, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0):
        pass

class BETA(TAFunc):
    """BETA(real0, real1, timeperiod=5) -> Beta
    Beta(stop, start=-1) -> outNBElement

    Beta (Statistic Functions)
    Inputs: real0, real1
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real0', 'real1', 'outReal', 'timeperiod')
    def __init__(self, real0, real1, timeperiod=5):
        pass

class BOP(TAFunc):
    """BOP(open, high, low, close) -> Bop
    Bop(stop, start=-1) -> outNBElement

    Balance Of Power (Momentum Indicators)
    Inputs: [open, high, low, close]
    Outputs: (outReal,d)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outReal')
    def __init__(self, open, high, low, close):
        pass

class CCI(TAFunc):
    """CCI(high, low, close, timeperiod=14) -> Cci
    Cci(stop, start=-1) -> outNBElement

    Commodity Channel Index (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class CDL2CROWS(TAFunc):
    """CDL2CROWS(open, high, low, close) -> Cdl2Crows
    Cdl2Crows(stop, start=-1) -> outNBElement

    Two Crows (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDL3BLACKCROWS(TAFunc):
    """CDL3BLACKCROWS(open, high, low, close) -> Cdl3BlackCrows
    Cdl3BlackCrows(stop, start=-1) -> outNBElement

    Three Black Crows (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDL3INSIDE(TAFunc):
    """CDL3INSIDE(open, high, low, close) -> Cdl3Inside
    Cdl3Inside(stop, start=-1) -> outNBElement

    Three Inside Up/Down (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDL3LINESTRIKE(TAFunc):
    """CDL3LINESTRIKE(open, high, low, close) -> Cdl3LineStrike
    Cdl3LineStrike(stop, start=-1) -> outNBElement

    Three-Line Strike  (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDL3OUTSIDE(TAFunc):
    """CDL3OUTSIDE(open, high, low, close) -> Cdl3Outside
    Cdl3Outside(stop, start=-1) -> outNBElement

    Three Outside Up/Down (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDL3STARSINSOUTH(TAFunc):
    """CDL3STARSINSOUTH(open, high, low, close) -> Cdl3StarsInSouth
    Cdl3StarsInSouth(stop, start=-1) -> outNBElement

    Three Stars In The South (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDL3WHITESOLDIERS(TAFunc):
    """CDL3WHITESOLDIERS(open, high, low, close) -> Cdl3WhiteSoldiers
    Cdl3WhiteSoldiers(stop, start=-1) -> outNBElement

    Three Advancing White Soldiers (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLABANDONEDBABY(TAFunc):
    """CDLABANDONEDBABY(open, high, low, close, penetration=0.3) -> CdlAbandonedBaby
    CdlAbandonedBaby(stop, start=-1) -> outNBElement

    Abandoned Baby (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.3):
        pass

class CDLADVANCEBLOCK(TAFunc):
    """CDLADVANCEBLOCK(open, high, low, close) -> CdlAdvanceBlock
    CdlAdvanceBlock(stop, start=-1) -> outNBElement

    Advance Block (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLBELTHOLD(TAFunc):
    """CDLBELTHOLD(open, high, low, close) -> CdlBeltHold
    CdlBeltHold(stop, start=-1) -> outNBElement

    Belt-hold (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLBREAKAWAY(TAFunc):
    """CDLBREAKAWAY(open, high, low, close) -> CdlBreakaway
    CdlBreakaway(stop, start=-1) -> outNBElement

    Breakaway (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLCLOSINGMARUBOZU(TAFunc):
    """CDLCLOSINGMARUBOZU(open, high, low, close) -> CdlClosingMarubozu
    CdlClosingMarubozu(stop, start=-1) -> outNBElement

    Closing Marubozu (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLCONCEALBABYSWALL(TAFunc):
    """CDLCONCEALBABYSWALL(open, high, low, close) -> CdlConcealBabysWall
    CdlConcealBabysWall(stop, start=-1) -> outNBElement

    Concealing Baby Swallow (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLCOUNTERATTACK(TAFunc):
    """CDLCOUNTERATTACK(open, high, low, close) -> CdlCounterAttack
    CdlCounterAttack(stop, start=-1) -> outNBElement

    Counterattack (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLDARKCLOUDCOVER(TAFunc):
    """CDLDARKCLOUDCOVER(open, high, low, close, penetration=0.5) -> CdlDarkCloudCover
    CdlDarkCloudCover(stop, start=-1) -> outNBElement

    Dark Cloud Cover (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.5):
        pass

class CDLDOJI(TAFunc):
    """CDLDOJI(open, high, low, close) -> CdlDoji
    CdlDoji(stop, start=-1) -> outNBElement

    Doji (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLDOJISTAR(TAFunc):
    """CDLDOJISTAR(open, high, low, close) -> CdlDojiStar
    CdlDojiStar(stop, start=-1) -> outNBElement

    Doji Star (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLDRAGONFLYDOJI(TAFunc):
    """CDLDRAGONFLYDOJI(open, high, low, close) -> CdlDragonflyDoji
    CdlDragonflyDoji(stop, start=-1) -> outNBElement

    Dragonfly Doji (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLENGULFING(TAFunc):
    """CDLENGULFING(open, high, low, close) -> CdlEngulfing
    CdlEngulfing(stop, start=-1) -> outNBElement

    Engulfing Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLEVENINGDOJISTAR(TAFunc):
    """CDLEVENINGDOJISTAR(open, high, low, close, penetration=0.3) -> CdlEveningDojiStar
    CdlEveningDojiStar(stop, start=-1) -> outNBElement

    Evening Doji Star (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.3):
        pass

class CDLEVENINGSTAR(TAFunc):
    """CDLEVENINGSTAR(open, high, low, close, penetration=0.3) -> CdlEveningStar
    CdlEveningStar(stop, start=-1) -> outNBElement

    Evening Star (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.3):
        pass

class CDLGAPSIDESIDEWHITE(TAFunc):
    """CDLGAPSIDESIDEWHITE(open, high, low, close) -> CdlGapSideSideWhite
    CdlGapSideSideWhite(stop, start=-1) -> outNBElement

    Up/Down-gap side-by-side white lines (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLGRAVESTONEDOJI(TAFunc):
    """CDLGRAVESTONEDOJI(open, high, low, close) -> CdlGravestoneDoji
    CdlGravestoneDoji(stop, start=-1) -> outNBElement

    Gravestone Doji (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHAMMER(TAFunc):
    """CDLHAMMER(open, high, low, close) -> CdlHammer
    CdlHammer(stop, start=-1) -> outNBElement

    Hammer (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHANGINGMAN(TAFunc):
    """CDLHANGINGMAN(open, high, low, close) -> CdlHangingMan
    CdlHangingMan(stop, start=-1) -> outNBElement

    Hanging Man (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHARAMI(TAFunc):
    """CDLHARAMI(open, high, low, close) -> CdlHarami
    CdlHarami(stop, start=-1) -> outNBElement

    Harami Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHARAMICROSS(TAFunc):
    """CDLHARAMICROSS(open, high, low, close) -> CdlHaramiCross
    CdlHaramiCross(stop, start=-1) -> outNBElement

    Harami Cross Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHIGHWAVE(TAFunc):
    """CDLHIGHWAVE(open, high, low, close) -> CdlHignWave
    CdlHignWave(stop, start=-1) -> outNBElement

    High-Wave Candle (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHIKKAKE(TAFunc):
    """CDLHIKKAKE(open, high, low, close) -> CdlHikkake
    CdlHikkake(stop, start=-1) -> outNBElement

    Hikkake Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHIKKAKEMOD(TAFunc):
    """CDLHIKKAKEMOD(open, high, low, close) -> CdlHikkakeMod
    CdlHikkakeMod(stop, start=-1) -> outNBElement

    Modified Hikkake Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLHOMINGPIGEON(TAFunc):
    """CDLHOMINGPIGEON(open, high, low, close) -> CdlHomingPigeon
    CdlHomingPigeon(stop, start=-1) -> outNBElement

    Homing Pigeon (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLIDENTICAL3CROWS(TAFunc):
    """CDLIDENTICAL3CROWS(open, high, low, close) -> CdlIdentical3Crows
    CdlIdentical3Crows(stop, start=-1) -> outNBElement

    Identical Three Crows (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLINNECK(TAFunc):
    """CDLINNECK(open, high, low, close) -> CdlInNeck
    CdlInNeck(stop, start=-1) -> outNBElement

    In-Neck Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLINVERTEDHAMMER(TAFunc):
    """CDLINVERTEDHAMMER(open, high, low, close) -> CdlInvertedHammer
    CdlInvertedHammer(stop, start=-1) -> outNBElement

    Inverted Hammer (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLKICKING(TAFunc):
    """CDLKICKING(open, high, low, close) -> CdlKicking
    CdlKicking(stop, start=-1) -> outNBElement

    Kicking (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLKICKINGBYLENGTH(TAFunc):
    """CDLKICKINGBYLENGTH(open, high, low, close) -> CdlKickingByLength
    CdlKickingByLength(stop, start=-1) -> outNBElement

    Kicking - bull/bear determined by the longer marubozu (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLLADDERBOTTOM(TAFunc):
    """CDLLADDERBOTTOM(open, high, low, close) -> CdlLadderBottom
    CdlLadderBottom(stop, start=-1) -> outNBElement

    Ladder Bottom (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLLONGLEGGEDDOJI(TAFunc):
    """CDLLONGLEGGEDDOJI(open, high, low, close) -> CdlLongLeggedDoji
    CdlLongLeggedDoji(stop, start=-1) -> outNBElement

    Long Legged Doji (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLLONGLINE(TAFunc):
    """CDLLONGLINE(open, high, low, close) -> CdlLongLine
    CdlLongLine(stop, start=-1) -> outNBElement

    Long Line Candle (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLMARUBOZU(TAFunc):
    """CDLMARUBOZU(open, high, low, close) -> CdlMarubozu
    CdlMarubozu(stop, start=-1) -> outNBElement

    Marubozu (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLMATCHINGLOW(TAFunc):
    """CDLMATCHINGLOW(open, high, low, close) -> CdlMatchingLow
    CdlMatchingLow(stop, start=-1) -> outNBElement

    Matching Low (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLMATHOLD(TAFunc):
    """CDLMATHOLD(open, high, low, close, penetration=0.5) -> CdlMatHold
    CdlMatHold(stop, start=-1) -> outNBElement

    Mat Hold (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.5):
        pass

class CDLMORNINGDOJISTAR(TAFunc):
    """CDLMORNINGDOJISTAR(open, high, low, close, penetration=0.3) -> CdlMorningDojiStar
    CdlMorningDojiStar(stop, start=-1) -> outNBElement

    Morning Doji Star (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.3):
        pass

class CDLMORNINGSTAR(TAFunc):
    """CDLMORNINGSTAR(open, high, low, close, penetration=0.3) -> CdlMorningStar
    CdlMorningStar(stop, start=-1) -> outNBElement

    Morning Star (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    Parameters:
      penetration: Penetration (0.0 <= d <= REAL_MAX)
        Percentage of penetration of a candle within another candle
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt', 'penetration')
    def __init__(self, open, high, low, close, penetration=0.3):
        pass

class CDLONNECK(TAFunc):
    """CDLONNECK(open, high, low, close) -> CdlOnNeck
    CdlOnNeck(stop, start=-1) -> outNBElement

    On-Neck Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLPIERCING(TAFunc):
    """CDLPIERCING(open, high, low, close) -> CdlPiercing
    CdlPiercing(stop, start=-1) -> outNBElement

    Piercing Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLRICKSHAWMAN(TAFunc):
    """CDLRICKSHAWMAN(open, high, low, close) -> CdlRickshawMan
    CdlRickshawMan(stop, start=-1) -> outNBElement

    Rickshaw Man (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLRISEFALL3METHODS(TAFunc):
    """CDLRISEFALL3METHODS(open, high, low, close) -> CdlRiseFall3Methods
    CdlRiseFall3Methods(stop, start=-1) -> outNBElement

    Rising/Falling Three Methods (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLSEPARATINGLINES(TAFunc):
    """CDLSEPARATINGLINES(open, high, low, close) -> CdlSeperatingLines
    CdlSeperatingLines(stop, start=-1) -> outNBElement

    Separating Lines (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLSHOOTINGSTAR(TAFunc):
    """CDLSHOOTINGSTAR(open, high, low, close) -> CdlShootingStar
    CdlShootingStar(stop, start=-1) -> outNBElement

    Shooting Star (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLSHORTLINE(TAFunc):
    """CDLSHORTLINE(open, high, low, close) -> CdlShortLine
    CdlShortLine(stop, start=-1) -> outNBElement

    Short Line Candle (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLSPINNINGTOP(TAFunc):
    """CDLSPINNINGTOP(open, high, low, close) -> CdlSpinningTop
    CdlSpinningTop(stop, start=-1) -> outNBElement

    Spinning Top (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLSTALLEDPATTERN(TAFunc):
    """CDLSTALLEDPATTERN(open, high, low, close) -> CdlStalledPattern
    CdlStalledPattern(stop, start=-1) -> outNBElement

    Stalled Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLSTICKSANDWICH(TAFunc):
    """CDLSTICKSANDWICH(open, high, low, close) -> CdlStickSandwhich
    CdlStickSandwhich(stop, start=-1) -> outNBElement

    Stick Sandwich (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLTAKURI(TAFunc):
    """CDLTAKURI(open, high, low, close) -> CdlTakuri
    CdlTakuri(stop, start=-1) -> outNBElement

    Takuri (Dragonfly Doji with very long lower shadow) (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLTASUKIGAP(TAFunc):
    """CDLTASUKIGAP(open, high, low, close) -> CdlTasukiGap
    CdlTasukiGap(stop, start=-1) -> outNBElement

    Tasuki Gap (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLTHRUSTING(TAFunc):
    """CDLTHRUSTING(open, high, low, close) -> CdlThrusting
    CdlThrusting(stop, start=-1) -> outNBElement

    Thrusting Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLTRISTAR(TAFunc):
    """CDLTRISTAR(open, high, low, close) -> CdlTristar
    CdlTristar(stop, start=-1) -> outNBElement

    Tristar Pattern (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLUNIQUE3RIVER(TAFunc):
    """CDLUNIQUE3RIVER(open, high, low, close) -> CdlUnique3River
    CdlUnique3River(stop, start=-1) -> outNBElement

    Unique 3 River (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLUPSIDEGAP2CROWS(TAFunc):
    """CDLUPSIDEGAP2CROWS(open, high, low, close) -> CdlUpsideGap2Crows
    CdlUpsideGap2Crows(stop, start=-1) -> outNBElement

    Upside Gap Two Crows (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CDLXSIDEGAP3METHODS(TAFunc):
    """CDLXSIDEGAP3METHODS(open, high, low, close) -> CdlXSideGap3Methods
    CdlXSideGap3Methods(stop, start=-1) -> outNBElement

    Upside/Downside Gap Three Methods (Pattern Recognition)
    Inputs: [open, high, low, close]
    Outputs: (outInt,i)
    """
    __slots__ = ('open', 'high', 'low', 'close', 'outInt')
    def __init__(self, open, high, low, close):
        pass

class CEIL(TAFunc):
    """CEIL(real) -> Ceil
    Ceil(stop, start=-1) -> outNBElement

    Vector Ceil (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class CMO(TAFunc):
    """CMO(real, timeperiod=14) -> Cmo
    Cmo(stop, start=-1) -> outNBElement

    Chande Momentum Oscillator (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class CORREL(TAFunc):
    """CORREL(real0, real1, timeperiod=30) -> Correl
    Correl(stop, start=-1) -> outNBElement

    Pearson's Correlation Coefficient (r) (Statistic Functions)
    Inputs: real0, real1
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real0', 'real1', 'outReal', 'timeperiod')
    def __init__(self, real0, real1, timeperiod=30):
        pass

class COS(TAFunc):
    """COS(real) -> Cos
    Cos(stop, start=-1) -> outNBElement

    Vector Trigonometric Cos (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class COSH(TAFunc):
    """COSH(real) -> Cosh
    Cosh(stop, start=-1) -> outNBElement

    Vector Trigonometric Cosh (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class DEMA(TAFunc):
    """DEMA(real, timeperiod=30) -> Dema
    Dema(stop, start=-1) -> outNBElement

    Double Exponential Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class DIV(TAFunc):
    """DIV(real0, real1) -> Div
    Div(stop, start=-1) -> outNBElement

    Vector Arithmetic Div (Math Operators)
    Inputs: real0, real1
    Outputs: (outReal,d)
    """
    __slots__ = ('real0', 'real1', 'outReal')
    def __init__(self, real0, real1):
        pass

class DX(TAFunc):
    """DX(high, low, close, timeperiod=14) -> Dx
    Dx(stop, start=-1) -> outNBElement

    Directional Movement Index (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class EMA(TAFunc):
    """EMA(real, timeperiod=30) -> Ema
    Ema(stop, start=-1) -> outNBElement

    Exponential Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class EXP(TAFunc):
    """EXP(real) -> Exp
    Exp(stop, start=-1) -> outNBElement

    Vector Arithmetic Exp (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class FLOOR(TAFunc):
    """FLOOR(real) -> Floor
    Floor(stop, start=-1) -> outNBElement

    Vector Floor (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class HT_DCPERIOD(TAFunc):
    """HT_DCPERIOD(real) -> HtDcPeriod
    HtDcPeriod(stop, start=-1) -> outNBElement

    Hilbert Transform - Dominant Cycle Period (Cycle Indicators)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class HT_DCPHASE(TAFunc):
    """HT_DCPHASE(real) -> HtDcPhase
    HtDcPhase(stop, start=-1) -> outNBElement

    Hilbert Transform - Dominant Cycle Phase (Cycle Indicators)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class HT_PHASOR(TAFunc):
    """HT_PHASOR(real) -> HtPhasor
    HtPhasor(stop, start=-1) -> outNBElement

    Hilbert Transform - Phasor Components (Cycle Indicators)
    Inputs: real
    Outputs: (outInPhase,d), (outQuadrature,d)
    """
    __slots__ = ('real', 'outInPhase', 'outQuadrature')
    def __init__(self, real):
        pass

class HT_SINE(TAFunc):
    """HT_SINE(real) -> HtSine
    HtSine(stop, start=-1) -> outNBElement

    Hilbert Transform - SineWave (Cycle Indicators)
    Inputs: real
    Outputs: (outSine,d), (outLeadSine,d)
    """
    __slots__ = ('real', 'outSine', 'outLeadSine')
    def __init__(self, real):
        pass

class HT_TRENDLINE(TAFunc):
    """HT_TRENDLINE(real) -> HtTrendline
    HtTrendline(stop, start=-1) -> outNBElement

    Hilbert Transform - Instantaneous Trendline (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class HT_TRENDMODE(TAFunc):
    """HT_TRENDMODE(real) -> HtTrendMode
    HtTrendMode(stop, start=-1) -> outNBElement

    Hilbert Transform - Trend vs Cycle Mode (Cycle Indicators)
    Inputs: real
    Outputs: (outInt,i)
    """
    __slots__ = ('real', 'outInt')
    def __init__(self, real):
        pass

class KAMA(TAFunc):
    """KAMA(real, timeperiod=30) -> Kama
    Kama(stop, start=-1) -> outNBElement

    Kaufman Adaptive Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class LINEARREG(TAFunc):
    """LINEARREG(real, timeperiod=14) -> LinearReg
    LinearReg(stop, start=-1) -> outNBElement

    Linear Regression (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class LINEARREG_ANGLE(TAFunc):
    """LINEARREG_ANGLE(real, timeperiod=14) -> LinearRegAngle
    LinearRegAngle(stop, start=-1) -> outNBElement

    Linear Regression Angle (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class LINEARREG_INTERCEPT(TAFunc):
    """LINEARREG_INTERCEPT(real, timeperiod=14) -> LinearRegIntercept
    LinearRegIntercept(stop, start=-1) -> outNBElement

    Linear Regression Intercept (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class LINEARREG_SLOPE(TAFunc):
    """LINEARREG_SLOPE(real, timeperiod=14) -> LinearRegSlope
    LinearRegSlope(stop, start=-1) -> outNBElement

    Linear Regression Slope (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class LN(TAFunc):
    """LN(real) -> Ln
    Ln(stop, start=-1) -> outNBElement

    Vector Log Natural (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class LOG10(TAFunc):
    """LOG10(real) -> Log10
    Log10(stop, start=-1) -> outNBElement

    Vector Log10 (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class MA(TAFunc):
    """MA(real, timeperiod=30, matype=0) -> ma
    ma(stop, start=-1) -> outNBElement

    Moving average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
      matype: MA Type
        Type of Moving Average
    """
    __slots__ = ('real', 'outReal', 'timeperiod', 'matype')
    def __init__(self, real, timeperiod=30, matype=0):
        pass

class MACD(TAFunc):
    """MACD(real, fastperiod=12, slowperiod=26, signalperiod=9) -> Macd
    Macd(stop, start=-1) -> outNBElement

    Moving Average Convergence/Divergence (Momentum Indicators)
    Inputs: real
    Outputs: (outMACD,d), (outMACDSignal,d), (outMACDHist,d)
    Parameters:
      fastperiod: Fast Period (2 <= i <= 100000)
        Number of period for the fast MA
      slowperiod: Slow Period (2 <= i <= 100000)
        Number of period for the slow MA
      signalperiod: Signal Period (1 <= i <= 100000)
        Smoothing for the signal line (nb of period)
    """
    __slots__ = ('real', 'outMACD', 'outMACDSignal', 'outMACDHist', 'fastperiod', 'slowperiod', 'signalperiod')
    def __init__(self, real, fastperiod=12, slowperiod=26, signalperiod=9):
        pass

class MACDEXT(TAFunc):
    """MACDEXT(real, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0) -> MacdExt
    MacdExt(stop, start=-1) -> outNBElement

    MACD with controllable MA type (Momentum Indicators)
    Inputs: real
    Outputs: (outMACD,d), (outMACDSignal,d), (outMACDHist,d)
    Parameters:
      fastperiod: Fast Period (2 <= i <= 100000)
        Number of period for the fast MA
      fastmatype: Fast MA
        Type of Moving Average for fast MA
      slowperiod: Slow Period (2 <= i <= 100000)
        Number of period for the slow MA
      slowmatype: Slow MA
        Type of Moving Average for slow MA
      signalperiod: Signal Period (1 <= i <= 100000)
        Smoothing for the signal line (nb of period)
      signalmatype: Signal MA
        Type of Moving Average for signal line
    """
    __slots__ = ('real', 'outMACD', 'outMACDSignal', 'outMACDHist', 'fastperiod', 'fastmatype', 'slowperiod', 'slowmatype', 'signalperiod', 'signalmatype')
    def __init__(self, real, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0):
        pass

class MACDFIX(TAFunc):
    """MACDFIX(real, signalperiod=9) -> MacdFix
    MacdFix(stop, start=-1) -> outNBElement

    Moving Average Convergence/Divergence Fix 12/26 (Momentum Indicators)
    Inputs: real
    Outputs: (outMACD,d), (outMACDSignal,d), (outMACDHist,d)
    Parameters:
      signalperiod: Signal Period (1 <= i <= 100000)
        Smoothing for the signal line (nb of period)
    """
    __slots__ = ('real', 'outMACD', 'outMACDSignal', 'outMACDHist', 'signalperiod')
    def __init__(self, real, signalperiod=9):
        pass

class MAMA(TAFunc):
    """MAMA(real, fastlimit=0.5, slowlimit=0.05) -> Mama
    Mama(stop, start=-1) -> outNBElement

    MESA Adaptive Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outMAMA,d), (outFAMA,d)
    Parameters:
      fastlimit: Fast Limit (0.01 <= d <= 0.99)
        Upper limit use in the adaptive algorithm
      slowlimit: Slow Limit (0.01 <= d <= 0.99)
        Lower limit use in the adaptive algorithm
    """
    __slots__ = ('real', 'outMAMA', 'outFAMA', 'fastlimit', 'slowlimit')
    def __init__(self, real, fastlimit=0.5, slowlimit=0.05):
        pass

class MAVP(TAFunc):
    """MAVP(real, periods, minperiod=2, maxperiod=30, matype=0) -> mavp
    mavp(stop, start=-1) -> outNBElement

    Moving average with variable period (Overlap Studies)
    Inputs: real, periods
    Outputs: (outReal,d)
    Parameters:
      minperiod: Minimum Period (2 <= i <= 100000)
        Value less than minimum will be changed to Minimum period
      maxperiod: Maximum Period (2 <= i <= 100000)
        Value higher than maximum will be changed to Maximum period
      matype: MA Type
        Type of Moving Average
    """
    __slots__ = ('real', 'periods', 'outReal', 'minperiod', 'maxperiod', 'matype')
    def __init__(self, real, periods, minperiod=2, maxperiod=30, matype=0):
        pass

class MAX(TAFunc):
    """MAX(real, timeperiod=30) -> Max
    Max(stop, start=-1) -> outNBElement

    Highest value over a specified period (Math Operators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class MAXINDEX(TAFunc):
    """MAXINDEX(real, timeperiod=30) -> MaxIndex
    MaxIndex(stop, start=-1) -> outNBElement

    Index of highest value over a specified period (Math Operators)
    Inputs: real
    Outputs: (outInt,i)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outInt', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class MEDPRICE(TAFunc):
    """MEDPRICE(high, low) -> MedPrice
    MedPrice(stop, start=-1) -> outNBElement

    Median Price (Price Transform)
    Inputs: [high, low]
    Outputs: (outReal,d)
    """
    __slots__ = ('high', 'low', 'outReal')
    def __init__(self, high, low):
        pass

class MFI(TAFunc):
    """MFI(high, low, close, volume, timeperiod=14) -> Mfi
    Mfi(stop, start=-1) -> outNBElement

    Money Flow Index (Momentum Indicators)
    Inputs: [high, low, close, volume]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'volume', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, volume, timeperiod=14):
        pass

class MIDPOINT(TAFunc):
    """MIDPOINT(real, timeperiod=14) -> MidPoint
    MidPoint(stop, start=-1) -> outNBElement

    MidPoint over period (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class MIDPRICE(TAFunc):
    """MIDPRICE(high, low, timeperiod=14) -> MidPrice
    MidPrice(stop, start=-1) -> outNBElement

    Midpoint Price over period (Overlap Studies)
    Inputs: [high, low]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'outReal', 'timeperiod')
    def __init__(self, high, low, timeperiod=14):
        pass

class MIN(TAFunc):
    """MIN(real, timeperiod=30) -> Min
    Min(stop, start=-1) -> outNBElement

    Lowest value over a specified period (Math Operators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class MININDEX(TAFunc):
    """MININDEX(real, timeperiod=30) -> MinIndex
    MinIndex(stop, start=-1) -> outNBElement

    Index of lowest value over a specified period (Math Operators)
    Inputs: real
    Outputs: (outInt,i)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outInt', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class MINMAX(TAFunc):
    """MINMAX(real, timeperiod=30) -> MinMax
    MinMax(stop, start=-1) -> outNBElement

    Lowest and highest values over a specified period (Math Operators)
    Inputs: real
    Outputs: (outMin,d), (outMax,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outMin', 'outMax', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class MINMAXINDEX(TAFunc):
    """MINMAXINDEX(real, timeperiod=30) -> MinMaxIndex
    MinMaxIndex(stop, start=-1) -> outNBElement

    Indexes of lowest and highest values over a specified period (Math Operators)
    Inputs: real
    Outputs: (outMinIdx,i), (outMaxIdx,i)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outMinIdx', 'outMaxIdx', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class MINUS_DI(TAFunc):
    """MINUS_DI(high, low, close, timeperiod=14) -> MinusDI
    MinusDI(stop, start=-1) -> outNBElement

    Minus Directional Indicator (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class MINUS_DM(TAFunc):
    """MINUS_DM(high, low, timeperiod=14) -> MinusDM
    MinusDM(stop, start=-1) -> outNBElement

    Minus Directional Movement (Momentum Indicators)
    Inputs: [high, low]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'outReal', 'timeperiod')
    def __init__(self, high, low, timeperiod=14):
        pass

class MOM(TAFunc):
    """MOM(real, timeperiod=10) -> Mom
    Mom(stop, start=-1) -> outNBElement

    Momentum (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=10):
        pass

class MULT(TAFunc):
    """MULT(real0, real1) -> Mult
    Mult(stop, start=-1) -> outNBElement

    Vector Arithmetic Mult (Math Operators)
    Inputs: real0, real1
    Outputs: (outReal,d)
    """
    __slots__ = ('real0', 'real1', 'outReal')
    def __init__(self, real0, real1):
        pass

class NATR(TAFunc):
    """NATR(high, low, close, timeperiod=14) -> Natr
    Natr(stop, start=-1) -> outNBElement

    Normalized Average True Range (Volatility Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class OBV(TAFunc):
    """OBV(real, volume) -> Obv
    Obv(stop, start=-1) -> outNBElement

    On Balance Volume (Volume Indicators)
    Inputs: real, [volume]
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'volume', 'outReal')
    def __init__(self, real, volume):
        pass

class PLUS_DI(TAFunc):
    """PLUS_DI(high, low, close, timeperiod=14) -> PlusDI
    PlusDI(stop, start=-1) -> outNBElement

    Plus Directional Indicator (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class PLUS_DM(TAFunc):
    """PLUS_DM(high, low, timeperiod=14) -> PlusDM
    PlusDM(stop, start=-1) -> outNBElement

    Plus Directional Movement (Momentum Indicators)
    Inputs: [high, low]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'outReal', 'timeperiod')
    def __init__(self, high, low, timeperiod=14):
        pass

class PPO(TAFunc):
    """PPO(real, fastperiod=12, slowperiod=26, matype=0) -> Ppo
    Ppo(stop, start=-1) -> outNBElement

    Percentage Price Oscillator (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      fastperiod: Fast Period (2 <= i <= 100000)
        Number of period for the fast MA
      slowperiod: Slow Period (2 <= i <= 100000)
        Number of period for the slow MA
      matype: MA Type
        Type of Moving Average
    """
    __slots__ = ('real', 'outReal', 'fastperiod', 'slowperiod', 'matype')
    def __init__(self, real, fastperiod=12, slowperiod=26, matype=0):
        pass

class ROC(TAFunc):
    """ROC(real, timeperiod=10) -> Roc
    Roc(stop, start=-1) -> outNBElement

    Rate of change : ((price/prevPrice)-1)*100 (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=10):
        pass

class ROCP(TAFunc):
    """ROCP(real, timeperiod=10) -> RocP
    RocP(stop, start=-1) -> outNBElement

    Rate of change Percentage: (price-prevPrice)/prevPrice (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=10):
        pass

class ROCR(TAFunc):
    """ROCR(real, timeperiod=10) -> RocR
    RocR(stop, start=-1) -> outNBElement

    Rate of change ratio: (price/prevPrice) (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=10):
        pass

class ROCR100(TAFunc):
    """ROCR100(real, timeperiod=10) -> RocR100
    RocR100(stop, start=-1) -> outNBElement

    Rate of change ratio 100 scale: (price/prevPrice)*100 (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=10):
        pass

class RSI(TAFunc):
    """RSI(real, timeperiod=14) -> Rsi
    Rsi(stop, start=-1) -> outNBElement

    Relative Strength Index (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class SAR(TAFunc):
    """SAR(high, low, acceleration=0.02, maximum=0.2) -> Sar
    Sar(stop, start=-1) -> outNBElement

    Parabolic SAR (Overlap Studies)
    Inputs: [high, low]
    Outputs: (outReal,d)
    Parameters:
      acceleration: Acceleration Factor (0.0 <= d <= REAL_MAX)
        Acceleration Factor used up to the Maximum value
      maximum: AF Maximum (0.0 <= d <= REAL_MAX)
        Acceleration Factor Maximum value
    """
    __slots__ = ('high', 'low', 'outReal', 'acceleration', 'maximum')
    def __init__(self, high, low, acceleration=0.02, maximum=0.2):
        pass

class SAREXT(TAFunc):
    """SAREXT(high, low, startvalue=0.0, offsetonreverse=0.0, accelerationinitlong=0.02, accelerationlong=0.02, accelerationmaxlong=0.2, accelerationinitshort=0.02, accelerationshort=0.02, accelerationmaxshort=0.2) -> SarExt
    SarExt(stop, start=-1) -> outNBElement

    Parabolic SAR - Extended (Overlap Studies)
    Inputs: [high, low]
    Outputs: (outReal,d)
    Parameters:
      startvalue: Start Value (REAL_MIN <= d <= REAL_MAX)
        Start value and direction. 0 for Auto, >0 for Long, <0 for Short
      offsetonreverse: Offset on Reverse (0.0 <= d <= REAL_MAX)
        Percent offset added/removed to initial stop on short/long reversal
      accelerationinitlong: AF Init Long (0.0 <= d <= REAL_MAX)
        Acceleration Factor initial value for the Long direction
      accelerationlong: AF Long (0.0 <= d <= REAL_MAX)
        Acceleration Factor for the Long direction
      accelerationmaxlong: AF Max Long (0.0 <= d <= REAL_MAX)
        Acceleration Factor maximum value for the Long direction
      accelerationinitshort: AF Init Short (0.0 <= d <= REAL_MAX)
        Acceleration Factor initial value for the Short direction
      accelerationshort: AF Short (0.0 <= d <= REAL_MAX)
        Acceleration Factor for the Short direction
      accelerationmaxshort: AF Max Short (0.0 <= d <= REAL_MAX)
        Acceleration Factor maximum value for the Short direction
    """
    __slots__ = ('high', 'low', 'outReal', 'startvalue', 'offsetonreverse', 'accelerationinitlong', 'accelerationlong', 'accelerationmaxlong', 'accelerationinitshort', 'accelerationshort', 'accelerationmaxshort')
    def __init__(self, high, low, startvalue=0.0, offsetonreverse=0.0, accelerationinitlong=0.02, accelerationlong=0.02, accelerationmaxlong=0.2, accelerationinitshort=0.02, accelerationshort=0.02, accelerationmaxshort=0.2):
        pass

class SIN(TAFunc):
    """SIN(real) -> Sin
    Sin(stop, start=-1) -> outNBElement

    Vector Trigonometric Sin (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class SINH(TAFunc):
    """SINH(real) -> Sinh
    Sinh(stop, start=-1) -> outNBElement

    Vector Trigonometric Sinh (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class SMA(TAFunc):
    """SMA(real, timeperiod=30) -> Sma
    Sma(stop, start=-1) -> outNBElement

    Simple Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class SQRT(TAFunc):
    """SQRT(real) -> Sqrt
    Sqrt(stop, start=-1) -> outNBElement

    Vector Square Root (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class STDDEV(TAFunc):
    """STDDEV(real, timeperiod=5, nbdev=1.0) -> StdDev
    StdDev(stop, start=-1) -> outNBElement

    Standard Deviation (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
      nbdev: Deviations (REAL_MIN <= d <= REAL_MAX)
        Nb of deviations
    """
    __slots__ = ('real', 'outReal', 'timeperiod', 'nbdev')
    def __init__(self, real, timeperiod=5, nbdev=1.0):
        pass

class STOCH(TAFunc):
    """STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0) -> Stoch
    Stoch(stop, start=-1) -> outNBElement

    Stochastic (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outSlowK,d), (outSlowD,d)
    Parameters:
      fastk_period: Fast-K Period (1 <= i <= 100000)
        Time period for building the Fast-K line
      slowk_period: Slow-K Period (1 <= i <= 100000)
        Smoothing for making the Slow-K line. Usually set to 3
      slowk_matype: Slow-K MA
        Type of Moving Average for Slow-K
      slowd_period: Slow-D Period (1 <= i <= 100000)
        Smoothing for making the Slow-D line
      slowd_matype: Slow-D MA
        Type of Moving Average for Slow-D
    """
    __slots__ = ('high', 'low', 'close', 'outSlowK', 'outSlowD', 'fastk_period', 'slowk_period', 'slowk_matype', 'slowd_period', 'slowd_matype')
    def __init__(self, high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0):
        pass

class STOCHF(TAFunc):
    """STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0) -> StochF
    StochF(stop, start=-1) -> outNBElement

    Stochastic Fast (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outFastK,d), (outFastD,d)
    Parameters:
      fastk_period: Fast-K Period (1 <= i <= 100000)
        Time period for building the Fast-K line
      fastd_period: Fast-D Period (1 <= i <= 100000)
        Smoothing for making the Fast-D line. Usually set to 3
      fastd_matype: Fast-D MA
        Type of Moving Average for Fast-D
    """
    __slots__ = ('high', 'low', 'close', 'outFastK', 'outFastD', 'fastk_period', 'fastd_period', 'fastd_matype')
    def __init__(self, high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0):
        pass

class STOCHRSI(TAFunc):
    """STOCHRSI(real, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0) -> StochRsi
    StochRsi(stop, start=-1) -> outNBElement

    Stochastic Relative Strength Index (Momentum Indicators)
    Inputs: real
    Outputs: (outFastK,d), (outFastD,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
      fastk_period: Fast-K Period (1 <= i <= 100000)
        Time period for building the Fast-K line
      fastd_period: Fast-D Period (1 <= i <= 100000)
        Smoothing for making the Fast-D line. Usually set to 3
      fastd_matype: Fast-D MA
        Type of Moving Average for Fast-D
    """
    __slots__ = ('real', 'outFastK', 'outFastD', 'timeperiod', 'fastk_period', 'fastd_period', 'fastd_matype')
    def __init__(self, real, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0):
        pass

class SUB(TAFunc):
    """SUB(real0, real1) -> Sub
    Sub(stop, start=-1) -> outNBElement

    Vector Arithmetic Substraction (Math Operators)
    Inputs: real0, real1
    Outputs: (outReal,d)
    """
    __slots__ = ('real0', 'real1', 'outReal')
    def __init__(self, real0, real1):
        pass

class SUM(TAFunc):
    """SUM(real, timeperiod=30) -> Sum
    Sum(stop, start=-1) -> outNBElement

    Summation (Math Operators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class T3(TAFunc):
    """T3(real, timeperiod=5, vfactor=0.7) -> t3
    t3(stop, start=-1) -> outNBElement

    Triple Exponential Moving Average (T3) (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
      vfactor: Volume Factor (0.0 <= d <= 1.0)
        Volume Factor
    """
    __slots__ = ('real', 'outReal', 'timeperiod', 'vfactor')
    def __init__(self, real, timeperiod=5, vfactor=0.7):
        pass

class TAN(TAFunc):
    """TAN(real) -> Tan
    Tan(stop, start=-1) -> outNBElement

    Vector Trigonometric Tan (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class TANH(TAFunc):
    """TANH(real) -> Tanh
    Tanh(stop, start=-1) -> outNBElement

    Vector Trigonometric Tanh (Math Transform)
    Inputs: real
    Outputs: (outReal,d)
    """
    __slots__ = ('real', 'outReal')
    def __init__(self, real):
        pass

class TEMA(TAFunc):
    """TEMA(real, timeperiod=30) -> Tema
    Tema(stop, start=-1) -> outNBElement

    Triple Exponential Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class TRANGE(TAFunc):
    """TRANGE(high, low, close) -> TrueRange
    TrueRange(stop, start=-1) -> outNBElement

    True Range (Volatility Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    """
    __slots__ = ('high', 'low', 'close', 'outReal')
    def __init__(self, high, low, close):
        pass

class TRIMA(TAFunc):
    """TRIMA(real, timeperiod=30) -> Trima
    Trima(stop, start=-1) -> outNBElement

    Triangular Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class TRIX(TAFunc):
    """TRIX(real, timeperiod=30) -> Trix
    Trix(stop, start=-1) -> outNBElement

    1-day Rate-Of-Change (ROC) of a Triple Smooth EMA (Momentum Indicators)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

class TSF(TAFunc):
    """TSF(real, timeperiod=14) -> Tsf
    Tsf(stop, start=-1) -> outNBElement

    Time Series Forecast (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=14):
        pass

class TYPPRICE(TAFunc):
    """TYPPRICE(high, low, close) -> TypPrice
    TypPrice(stop, start=-1) -> outNBElement

    Typical Price (Price Transform)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    """
    __slots__ = ('high', 'low', 'close', 'outReal')
    def __init__(self, high, low, close):
        pass

class ULTOSC(TAFunc):
    """ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28) -> UltOsc
    UltOsc(stop, start=-1) -> outNBElement

    Ultimate Oscillator (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod1: First Period (1 <= i <= 100000)
        Number of bars for 1st period.
      timeperiod2: Second Period (1 <= i <= 100000)
        Number of bars fro 2nd period
      timeperiod3: Third Period (1 <= i <= 100000)
        Number of bars for 3rd period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod1', 'timeperiod2', 'timeperiod3')
    def __init__(self, high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28):
        pass

class VAR(TAFunc):
    """VAR(real, timeperiod=5, nbdev=1.0) -> Variance
    Variance(stop, start=-1) -> outNBElement

    Variance (Statistic Functions)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (1 <= i <= 100000)
        Number of period
      nbdev: Deviations (REAL_MIN <= d <= REAL_MAX)
        Nb of deviations
    """
    __slots__ = ('real', 'outReal', 'timeperiod', 'nbdev')
    def __init__(self, real, timeperiod=5, nbdev=1.0):
        pass

class WCLPRICE(TAFunc):
    """WCLPRICE(high, low, close) -> WclPrice
    WclPrice(stop, start=-1) -> outNBElement

    Weighted Close Price (Price Transform)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    """
    __slots__ = ('high', 'low', 'close', 'outReal')
    def __init__(self, high, low, close):
        pass

class WILLR(TAFunc):
    """WILLR(high, low, close, timeperiod=14) -> WillR
    WillR(stop, start=-1) -> outNBElement

    Williams' %R (Momentum Indicators)
    Inputs: [high, low, close]
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('high', 'low', 'close', 'outReal', 'timeperiod')
    def __init__(self, high, low, close, timeperiod=14):
        pass

class WMA(TAFunc):
    """WMA(real, timeperiod=30) -> Wma
    Wma(stop, start=-1) -> outNBElement

    Weighted Moving Average (Overlap Studies)
    Inputs: real
    Outputs: (outReal,d)
    Parameters:
      timeperiod: Time Period (2 <= i <= 100000)
        Number of period
    """
    __slots__ = ('real', 'outReal', 'timeperiod')
    def __init__(self, real, timeperiod=30):
        pass

INT_MIN, INT_MAX, INT_DEFAULT, REAL_MIN, REAL_MAX, REAL_DEFAULT = (None,) * 6
MA_S, MA_E, MA_W, MA_DE, MA_TE, MA_TRI, MA_KA, MA_MA, MA_T3 = range(9)

def _init():
    ENV = globals(); del ENV['_init']
    from ._talib import _init; _init(ENV)
_init()
