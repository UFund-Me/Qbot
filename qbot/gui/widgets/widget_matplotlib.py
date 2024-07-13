import matplotlib
import matplotlib.pyplot as plt
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class MatplotlibPanel(wx.ScrolledWindow):
    def __init__(self, parent, id=-1):
        super(MatplotlibPanel, self).__init__(parent, id)
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.TopBoxSizer)

        self.btn_bkt = wx.Button(self, label="投资策略回测分析", pos=(100, 10))

        self.figure = matplotlib.figure.Figure(figsize=(4, 3))
        self.figure = plt.figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.TopBoxSizer.Add(
            self.canvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND
        )

    def show(self):
        plt.show()
