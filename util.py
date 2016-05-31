import wx

def bold_font(point_size, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL):
    return wx.Font(point_size, family, style, wx.FONTWEIGHT_BOLD)
