import wx
import inspect

class WxQuickBase(object):
    @property
    def wx_class(self):
        wxquick_base = type(self)
        for base in inspect.getmro(wxquick_base):
            if issubclass(base, wx.Object) and base != wxquick_base:
                return base

        raise NotImplementedError('No wx class specified.')

    def pack(self, parent=None):
        '''Default packing method'''
        self.wx_class.__init__(self, parent, **self._kwargs)
        for child in self.children:
            child.pack(self)
        
class WxQuickContainer(WxQuickBase):
    def __init__(self, *args, **kw):
        '''Base class for wx container controls'''
        self.children = list(args)
        self.proportion = kw.pop('sizer_proportion', 0)
        self.flag = kw.pop('sizer_flag', 0)
        self.border = kw.pop('sizer_border', 0)
        self.item_gap = kw.pop('item_gap', 0)
        self.center_children = kw.pop('center_children', False)
        self._kwargs = kw

    def add_child(self, child):
        self.children.append(child)
        return self

class WxQuickWidget(WxQuickBase):
    def __init__(self, *args, **kw):
        self._args = args
        self.proportion = kw.pop('sizer_proportion', 0)
        self.flag = kw.pop('sizer_flag', 0)
        self.border = kw.pop('sizer_border', 0)
        self.grid_pos = kw.pop('grid_pos', None)
        self.grid_span = kw.pop('grid_span', wx.DefaultSpan)
        self.font = kw.pop('font', None)
        self.fg_color = kw.pop('fg_color', None)
        self.bold = kw.pop('bold', None)
        self.wrap = kw.pop('wrap', None)
        self.value = kw.pop('value', None)
        self.enable = kw.pop('enable', True)
        self.callback = kw.pop('callback', None)
        self._kwargs = kw

    def pack(self, parent):
        if self._kwargs:
            self.wx_class.__init__(self, parent, *self._args, **self._kwargs)
        else:
            self.wx_class.__init__(self, parent, *self._args)

        if self.font:
            self.SetFont(self.font)

        if self.fg_color:
            self.SetForegroundColour(self.fg_color)

        if self.bold:
            font = self.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            self.SetFont(font)

        if self.wrap:
            self.Wrap(self.wrap)

        if self.value:
            self.SetValue(self.value)

        if not self.enable:
            self.Disable()

        for event in getattr(self, 'events', []):
            if self.callback:
                event(self, self.callback)




