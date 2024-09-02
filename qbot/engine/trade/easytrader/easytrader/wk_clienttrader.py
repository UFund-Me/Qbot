# -*- coding: utf-8 -*-
import pywinauto

from easytrader.ht_clienttrader import HTClientTrader


class WKClientTrader(HTClientTrader):
    @property
    def broker_type(self):
        return "wk"

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
            raise ValueError("五矿必须设置通讯密码")

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
            self._app.top_window().Edit1.set_edit_text(user)
            self._app.top_window().Edit2.set_edit_text(password)

            self._app.top_window().Edit3.set_edit_text(comm_password)

            self._app.top_window().Button1.click()

            # detect login is success or not
            self._app.top_window().wait_not("exists", 100)

            self._app = pywinauto.Application().connect(
                path=self._run_exe_path(exe_path), timeout=10
            )
        self._close_prompt_windows()
        self._main = self._app.window(title="网上股票交易系统5.0")