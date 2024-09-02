#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from qbot.gui.mainframe import MainFrame

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title="AI智能量化投研平台")
    frame.Show()

    app.MainLoop()
