import wx

def widg_init(widget, *args, **kw):
    widget._args = args
    widget.proportion = kw.pop('sizer_proportion', 0)
    widget.flag = kw.pop('sizer_flag', 0)
    widget.border = kw.pop('sizer_border', 0)
    widget.grid_pos = kw.pop('grid_pos', None)
    widget.grid_span = kw.pop('grid_span', wx.DefaultSpan)
    widget.font = kw.pop('font', None)
    widget.fg_color = kw.pop('fg_color', None)
    widget.bold = kw.pop('bold', None)
    widget.wrap = kw.pop('wrap', None)
    widget.value = kw.pop('value', None)
    widget.enable = kw.pop('enable', True)
    widget.callback = kw.pop('callback', None)
    widget._kwargs = kw

def widg_pack(widget, parent):
    if widget._kwargs:
        widget.wxClass.__init__(widget, parent, *widget._args, 
                                **widget._kwargs)
    else:
        widget.wxClass.__init__(widget, parent, *widget._args)

    if widget.font:
        widget.SetFont(widget.font)

    if widget.fg_color:
        widget.SetForegroundColour(widget.fg_color)

    if widget.bold:
        font = widget.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        widget.SetFont(font)

    if widget.wrap:
        widget.Wrap(widget.wrap)

    if widget.value:
        widget.SetValue(widget.value)
        
    if not widget.enable:
        widget.Disable()
        
    for event in widget.events:
        if widget.callback:
            event(widget, widget.callback)
        
class MetaWxWidget(type):
    def __new__(cls, clsname, bases, attrs):
        if clsname != 'WxWidget':
            attrs['__init__'] = widg_init
            attrs['pack'] = attrs.get('packer', widg_pack)
            attrs['events'] = attrs.get('events', [])
                
        return type.__new__(cls, clsname, bases, attrs)

    def __init__(self, clsname, bases, attrs):
        for base in bases:
            if base != WxWidget:
                self.wxClass = base

        type.__init__(self, clsname, bases, attrs)


def ctr_init(container, *args, **kw):
    container.children = list(args)
    container.proportion = kw.pop('sizer_proportion', 0)
    container.flag = kw.pop('sizer_flag', 0)
    container.border = kw.pop('sizer_border', 0)
    container.item_gap = kw.pop('item_gap', 0)
    container._kwargs = kw

def add_child(container, child):
    container.children.append(child)
    return container

class MetaWxContainer(type):
    def __new__(cls, clsname, bases, attrs):
        if clsname != 'WxContainer':
            attrs['__init__'] = ctr_init
            attrs['__add__'] = add_child
            attrs['pack'] = attrs.get('packer')
        return type.__new__(cls, clsname, bases, attrs)

    def __init__(self, clsname, bases, attrs):
        for base in bases:
            if base != WxContainer:
                self.wxClass = base

class WxContainer: __metaclass__ = MetaWxContainer
class WxWidget: __metaclass__ = MetaWxWidget
