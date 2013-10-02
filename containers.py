import wx

class VerticalBox(wx.BoxSizer):
    def __init__(self):
        wx.BoxSizer.__init__(self, wx.VERTICAL)

class HorizontalBox(wx.BoxSizer):
    def __init__(self):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
