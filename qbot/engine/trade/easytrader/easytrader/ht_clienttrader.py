# -*- coding: utf-8 -*-

import pywinauto
import pywinauto.clipboard

from easytrader import grid_strategies
from . import clienttrader


class HTClientTrader(clienttrader.BaseLoginClientTrader):
    grid_strategy = grid_strategies.Xls

    @property
    def broker_type(self):
        return "ht"

    def login(self, user, password, exe_path, comm_password=None, **kwargs):
        """
        :param user: 用户名
        :param password: 密码
        :param exe_path: 客户端路径, 类似
        :param comm_password:
        :param kwargs:
        :return:
        """
        self._editor_need_type_keys = False
        if comm_password is None:
            raise ValueError("华泰必须设置通讯密码")

        try:
            self._app = pywinauto.Application().connect(
                path=self._run_exe_path(exe_path), timeout=1
            )
        # pylint: disable=broad-except
        except Exception:
            self._app = pywinauto.Application().start(exe_path)

            # wait login window ready
            while True:
                try:
                    self._app.top_window().Edit1.wait("ready")
                    break
                except RuntimeError:
                    pass
            self._app.top_window().Edit1.set_focus()
            self._app.top_window().Edit1.type_keys(user)
            self._app.top_window().Edit2.type_keys(password)

            self._app.top_window().Edit3.set_edit_text(comm_password)

            self._app.top_window().button0.click()

            self._app = pywinauto.Application().connect(
                path=self._run_exe_path(exe_path), timeout=10
            )
        self._main = self._app.window(title="网上股票交易系统5.0")
        self._main.wait ( "exists enabled visible ready" , timeout=100 )
        self._close_prompt_windows ( )

    @property
    def balance(self):
        self._switch_left_menus(self._config.BALANCE_MENU_PATH)

        return self._get_balance_from_statics()

    def _get_balance_from_statics(self):
        result = {}
        for key, control_id in self._config.BALANCE_CONTROL_ID_GROUP.items():
            result[key] = float(
                self._main.child_window(
                    control_id=control_id, class_name="Static"
                ).window_text()
            )
        return result


