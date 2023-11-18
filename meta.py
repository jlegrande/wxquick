import wx
import inspect

class WxQuickBase(object):
    def nearest_wxquick_class(self, cls):
        '''The nearest wxquick class could be "cls" or a superclass that "cls" is 
           derived from.

           A wxquick class is a class that subclasses one of the following:
               - WxQuickContainer
               - WxQuickWidget
               - WxSizerMixin'''
        
        for base in cls.__bases__:
            if base in (WxQuickContainer, WxQuickWidget, WxSizerMixin):
                return cls

            nearest_cls = self.nearest_wxquick_class(base)
            if nearest_cls:
                return nearest_cls

        return None

        
    @property
    def wx_class(self):
        wxquick_base = self.nearest_wxquick_class(type(self))
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

    def __add__(self, child):
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
        self.bg_color = kw.pop('bg_color', None)
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

        if self.grid_pos:
            self.grid_pos = wx.GBPosition(self.grid_pos[0], self.grid_pos[1])
            
        if self.font:
            self.SetFont(self.font)

        if self.bg_color:
            if isinstance(self.bg_color, list) or isinstance(self.bg_color, tuple):
                self.SetBackgroundColour(self.bg_color[0], self.bg_color[1], self.bg_color[2])
            else:
                self.SetBackgroundColour(self.bg_color)
            
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


class WxSizerMixin(WxQuickContainer):
    def pack(self, parent, container_parent=None):
        if container_parent:
            self.wx_class.__init__(self, container_parent, **self._kwargs)
        else:
            self.wx_class.__init__(self, **self._kwargs)

        for child in self.children:
            child.pack(parent)
            if self.center_children:
                child.flag |= wx.ALIGN_CENTER
            spacer_size = getattr(child, 'spacer_size', None)
            if not spacer_size:
                self.Add(child, child.proportion, child.flag, child.border)
            else:
                sizer_proportion = getattr(child, 'proportion', 0)
                try:
                    w, h = spacer_size
                    self.Add(w, h, sizer_proportion)
                except TypeError:
                    self.AddSpacer(spacer_size)

            if self.item_gap > 0:
                self.AddSpacer(self.item_gap)


