import wx

class VerticalBox(wx.BoxSizer):
    def __init__(self):
        wx.BoxSizer.__init__(self, wx.VERTICAL)

class HorizontalBox(wx.BoxSizer):
    def __init__(self):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

class Spacer(wx.Object):
    def __init__(self, parent, size, proportion=0):
        self.spacer_size = size
        self.proportion = proportion

class DialogButtons(wx.BoxSizer):
    def __init__(self, parent, style):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        dlg_found = False
        while parent and not dlg_found:
            try:
                self.Add(parent.CreateButtonSizer(style))
                dlg_found = True
            except AttributeError:
                parent = parent.GetParent()
