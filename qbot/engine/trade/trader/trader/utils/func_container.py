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

from abc import ABCMeta
from functools import wraps


def RegisterCallback(**out_kwargs):
    def _callback_handler(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, *kwargs)

        for key, value in out_kwargs.items():
            setattr(wrapper, f'arg_{key}', value)
        setattr(wrapper, 'is_callback_function', True)
        return wrapper

    return _callback_handler


class CallbackFunctionContainer(object, metaclass=ABCMeta):
    def __init__(self):
        self.callback_fun_args = dict()
        self._collect_all()

    def _collect_all(self):
        for fun_name in dir(self):
            fun = getattr(self, fun_name)
            if hasattr(fun, 'is_callback_function'):
                params = dict()
                for arg in dir(fun):
                    if arg.startswith('arg_'):
                        params[arg[4:]] = getattr(fun, arg)
                self.callback_fun_args[fun_name] = params
