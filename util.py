import wx
from wx.lib.mixins.listctrl import TextEditMixin

def bold_font(point_size,
              family=wx.FONTFAMILY_DEFAULT,
              style=wx.FONTSTYLE_NORMAL,
              underline=False,
              face=''):
    return font(point_size, family, style, wx.FONTWEIGHT_BOLD, underline, face)

def font(point_size,
         family=wx.FONTFAMILY_DEFAULT,
         style=wx.FONTSTYLE_NORMAL,
         weight=wx.FONTWEIGHT_NORMAL,
         underline=False,
         face=''):
    return wx.Font(point_size, family, style, weight, underline, face)

class EditableListCtrl(wx.ListCtrl, TextEditMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        TextEditMixin.__init__(self)

class HtmlListBox(wx.HtmlListBox):
    def __init__(self, *args, **kwargs):
        self._render_item = kwargs.pop('render_item')
        self.data = kwargs.pop('data', {})
        wx.HtmlListBox.__init__(self, *args, **kwargs)

    def OnGetItem(self, n):
        return self._render_item(n, self.data)
