# -*- coding: utf-8 -*-
import abc
import io
import tempfile
from io import StringIO
from typing import TYPE_CHECKING, Dict, List, Optional

import pandas as pd
import pywinauto.keyboard
import pywinauto
import pywinauto.clipboard

from easytrader.log import logger
from easytrader.utils.captcha import captcha_recognize
from easytrader.utils.win_gui import SetForegroundWindow, ShowWindow, win32defines

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from easytrader import clienttrader


class IRefreshStrategy(abc.ABC):
    _trader: "clienttrader.ClientTrader"

    @abc.abstractmethod
    def refresh(self):
        """
        刷新数据
        """
        pass

    def set_trader(self, trader: "clienttrader.ClientTrader"):
        self._trader = trader


# noinspection PyProtectedMember
class Switch(IRefreshStrategy):
    """通过切换菜单栏刷新"""

    def __init__(self, sleep: float = 0.1):
        self.sleep = sleep

    def refresh(self):
        self._trader._switch_left_menus_by_shortcut("{F5}", sleep=self.sleep)


# noinspection PyProtectedMember
class Toolbar(IRefreshStrategy):
    """通过点击工具栏刷新按钮刷新"""

    def __init__(self, refresh_btn_index: int = 4):
        """
        :param refresh_btn_index:
            交易客户端工具栏中“刷新”排序，默认为第4个，请根据自己实际调整
        """
        self.refresh_btn_index = refresh_btn_index

    def refresh(self):
        self._trader._toolbar.button(self.refresh_btn_index - 1).click()
