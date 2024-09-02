#! /usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import datetime


class SysLogIf:

    error = "错误"
    warning = "警告"
    info = "信息"
    ind = "通知"

    def __init__(self, descr_obj):
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.descr_obj = descr_obj

    def re_print(self, cont):
        self.descr_obj.AppendText(self.time + ":\n" + cont + "\n")

    def clr_print(self):
        self.descr_obj.Clear()


class PatLogIf:

    def __init__(self, descr_obj):
        self.descr_obj = descr_obj

    def re_print(self, cont):
        self.descr_obj.AppendText(cont + "\n")

    def get_values(self):
        return self.descr_obj.GetValue()

    def clr_print(self):
        self.descr_obj.Clear()
