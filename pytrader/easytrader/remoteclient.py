# -*- coding: utf-8 -*-
import requests

from easytrader.utils.misc import file2dict


def use(broker, host, port=1430, **kwargs):
    return RemoteClient(broker, host, port)


class RemoteClient:
    def __init__(self, broker, host, port=1430, **kwargs):
        self._s = requests.session()
        self._api = "http://{}:{}".format(host, port)
        self._broker = broker

    def prepare(
        self,
        config_path=None,
        user=None,
        password=None,
        exe_path=None,
        comm_password=None,
        **kwargs
    ):
        """
        登陆客户端
        :param config_path: 登陆配置文件，跟参数登陆方式二选一
        :param user: 账号
        :param password: 明文密码
        :param exe_path: 客户端路径类似 r'C:\\htzqzyb2\\xiadan.exe',
            默认 r'C:\\htzqzyb2\\xiadan.exe'
        :param comm_password: 通讯密码
        :return:
        """
        params = locals().copy()
        params.pop("self")

        if config_path is not None:
            account = file2dict(config_path)
            params["user"] = account["user"]
            params["password"] = account["password"]

        params["broker"] = self._broker

        response = self._s.post(self._api + "/prepare", json=params)
        if response.status_code >= 300:
            raise Exception(response.json()["error"])
        return response.json()

    @property
    def balance(self):
        return self.common_get("balance")

    @property
    def position(self):
        return self.common_get("position")

    @property
    def today_entrusts(self):
        return self.common_get("today_entrusts")

    @property
    def today_trades(self):
        return self.common_get("today_trades")

    @property
    def cancel_entrusts(self):
        return self.common_get("cancel_entrusts")

    def auto_ipo(self):
        return self.common_get("auto_ipo")

    def exit(self):
        return self.common_get("exit")

    def common_get(self, endpoint):
        response = self._s.get(self._api + "/" + endpoint)
        if response.status_code >= 300:
            raise Exception(response.json()["error"])
        return response.json()

    def buy(self, security, price, amount, **kwargs):
        params = locals().copy()
        params.pop("self")

        response = self._s.post(self._api + "/buy", json=params)
        if response.status_code >= 300:
            raise Exception(response.json()["error"])
        return response.json()

    def sell(self, security, price, amount, **kwargs):
        params = locals().copy()
        params.pop("self")

        response = self._s.post(self._api + "/sell", json=params)
        if response.status_code >= 300:
            raise Exception(response.json()["error"])
        return response.json()

    def cancel_entrust(self, entrust_no):
        params = locals().copy()
        params.pop("self")

        response = self._s.post(self._api + "/cancel_entrust", json=params)
        if response.status_code >= 300:
            raise Exception(response.json()["error"])
        return response.json()
