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
