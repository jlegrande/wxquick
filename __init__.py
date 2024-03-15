import wx
import wx.adv
import wx.html
import wx.gizmos
from wx.grid import Grid
from wx.lib.buttons import GenBitmapTextButton, GenButton
from wx.lib.platebtn import PlateButton
from wx.lib.stattext import GenStaticText
from wx.lib.intctrl import IntCtrl
from wx.lib.masked import TextCtrl, TimeCtrl
from wx.lib.scrolledpanel import ScrolledPanel
from .meta import WxSizerMixin, WxQuickContainer, WxQuickWidget
from . import util
from . import containers
from . import event

def get_set_font(func):
    def wrapper_get_set_font(*args):
        self = args[0]
        new_args = list(args)
        font = self.GetFont()
        new_args.append(font)
        func(*new_args)
        self.SetFont(font)

    return wrapper_get_set_font


class ListCtrlPacker(object):
    def pack(self, parent):
        print('lcp pack')
        cols = self._kwargs.pop('columns', [])
        super().pack(parent)

        for i, col in enumerate(cols):
            self.InsertColumn(i, col)


# Wrapper Classes

# Widgets
class WxButton(WxQuickWidget, wx.Button): events = [event.button]
class WxCheckBox(WxQuickWidget, wx.CheckBox): events = [event.checkbox]
class WxComboBox(WxQuickWidget, wx.ComboBox): events = [event.combobox]
class WxChoice(WxQuickWidget, wx.Choice): events = [event.choice]
class WxDatePicker(WxQuickWidget, wx.adv.DatePickerCtrl): pass
class WxEditableListBox(WxQuickWidget, wx.adv.EditableListBox): pass
class WxGenButton(WxQuickWidget, GenButton): events = [event.button]
class WxGenericDatePicker(WxQuickWidget, wx.adv.DatePickerCtrl): pass
class WxGenStaticText(WxQuickWidget, GenStaticText): pass

class WxGrid(WxQuickWidget, Grid):
    def pack(self, parent):
        rows, cols = self._kwargs.pop('grid_size', (1,1))
        colnames = self._kwargs.pop('columns', [])
        self.wx_class.__init__(self, parent, *self._args, **self._kwargs)
        self.CreateGrid(rows, cols)
        for i, name in enumerate(colnames):
            self.SetColLabelValue(i, name)

class WxHtmlListBox(WxQuickWidget, util.HtmlListBox): pass
class WxHtmlWindow(WxQuickWidget, wx.html.HtmlWindow):
    def pack(self, parent):
        src = self._kwargs.pop('src', None)
        super(WxHtmlWindow, self).pack(parent)
        if src:
            self.SetPage(src)

class WxIntCtrl(WxQuickWidget, IntCtrl): events = [event.text]
class WxListBox(WxQuickWidget, wx.ListBox): events = [event.listbox]
class WxPlateButton(WxQuickWidget, PlateButton):
    events = [event.button]

    def pack(self, parent):
        self.client_data = self._kwargs.pop('client_data', None)
        label_color = self._kwargs.pop('label_color', None)
        bmp = self._kwargs.pop('bitmap', None)
        super(WxPlateButton, self).pack(parent)

        if label_color:
            self.SetLabelColor(label_color)

        if bmp:
            self.SetBitmap(bmp)
        
class WxRadioBox(WxQuickWidget, wx.RadioBox): pass

class WxStaticBitmap(WxQuickWidget, wx.StaticBitmap):
    def pack(self, parent):
        path = self._kwargs.pop('path', None)
        if path:
            bitmap_type = self._kwargs.pop('bmptype', wx.BITMAP_TYPE_JPEG)
            bmp = wx.Bitmap()
            bmp.LoadFile(path)
            self._kwargs['bitmap'] = bmp
        elif not self._kwargs.get('bitmap'):
            size = self._kwargs.get('size', (-1, -1))
            self._kwargs['bitmap'] = wx.EmptyBitmap(size[0], size[1])
            
        super(WxStaticBitmap, self).pack(parent)

        self.SetScaleMode(wx.StaticBitmap.Scale_AspectFill)

    def LoadFrom(self, path):
        bmp = wx.Bitmap()
        bmp.LoadFile(path)
        self.SetBitmap(bmp)

class WxStaticLine(WxQuickWidget, wx.StaticLine): pass
class WxStaticText(WxQuickWidget, wx.StaticText):
    def pack(self, parent):
        point_size = self._kwargs.pop('point_size', None)
        italic = self._kwargs.pop('italic', None)
        if self._kwargs.pop('align_center', False):
            self._kwargs.setdefault('style', wx.ALIGN_CENTER)
            self._kwargs['style'] |= wx.ALIGN_CENTER
            
        super(WxStaticText, self).pack(parent)
        if point_size:
            self.set_font_property(lambda f: f.SetPointSize(point_size))
            
        if italic:
            self.set_font_property(lambda f: f.SetStyle(wx.FONTSTYLE_ITALIC))
            
    @get_set_font
    def set_font_property(self, prop_set_func, font):
        prop_set_func(font)
            
        
class WxSlider(WxQuickWidget, wx.Slider): events = [event.scroll]
class WxTextCtrl(WxQuickWidget, wx.TextCtrl): events = [event.text]

class WxCheckListBox(WxQuickWidget, wx.CheckListBox): 
    events = [event.checklistbox, event.listbox]

class WxListCtrl(ListCtrlPacker, WxQuickWidget, wx.ListCtrl):
    events = [event.listctrl_item_selection]

class WxEditableListCtrl(ListCtrlPacker, WxQuickWidget, util.EditableListCtrl):
    events = [event.listctrl_item_selection]

class DialogButtons(WxQuickWidget, containers.DialogButtons):
    events = [event.button]

    def pack(self, parent):
        self.wx_class.__init__(self, parent, *self._args)
        cb = self.callback
        if not cb:
            return
        
        child_sizer = self.GetChildren()[0].GetSizer()
        buttons = [c.GetWindow() for c in child_sizer.GetChildren() if c.IsWindow()]

        for evt in self.events:
            for butt in buttons:
                evt(butt, cb)

class MaskedTextCtrl(WxQuickWidget, TextCtrl): pass
class MaskedTimeCtrl(WxQuickWidget, TimeCtrl): pass
class LEDNumberCtrl(WxQuickWidget, wx.gizmos.LEDNumberCtrl): pass

# Containers
class WxDialog(WxQuickContainer, wx.Dialog):
    def pack(self, parent=None, center=True):
        super().pack(parent)
        if len(self.children) == 1:
            try:
                self.SetSizer(self.children[0])
                self.SetAutoLayout(True)
                if not self._kwargs.get('size'):
                    self.Fit()
            except TypeError:
                pass

        if center:
            self.CenterOnParent()

class WxGridBagSizer(WxQuickContainer, wx.GridBagSizer):
    def pack(self, parent):
        self.wx_class.__init__(self, **self._kwargs)
        for child in self.children:
            child.pack(parent)
            self.Add(child,
                     child.grid_pos,
                     child.grid_span,
                     child.proportion,
                     child.flag,
                     child.border)

class WxFrame(WxQuickContainer, wx.Frame):
    def pack(self, parent=None, show=False, center=True):
        try:
            super().pack(parent)
        except TypeError:
            import traceback
            exc = traceback.format_exc()
            print(exc)
            wx.MessageDialog(None,
                             '%s' % exc,
                             'Invalid Parent', wx.OK|wx.ICON_ERROR).ShowModal()
            raise

        #self.Fit()
        if center:
            self.CenterOnScreen()

        if show:
            self.Show()
    
class WxMenu(WxQuickContainer, wx.Menu):
    def pack(self, frame):
        self.title = self._kwargs.get('title', '')
        self.wx_class.__init__(self)
        for item_id, item_text, item_help, callback in self.children:
            menuitem = self.Append(item_id, item_text, item_help)
            frame.Bind(wx.EVT_MENU, event.menuitem_cb_wrapper(menuitem, callback), menuitem)
    
class WxMenuBar(WxQuickContainer, wx.MenuBar):
    def pack(self, frame):
        frame.CreateStatusBar()
        self.wx_class.__init__(self)
        for menu in self.children:
            menu.pack(frame)
            self.Append(menu, menu.title)

        frame.SetMenuBar(self)
    
class WxNotebook(WxQuickContainer, wx.Notebook):
    def notebook_pack(self, parent=None, show=False):
        self.wx_class.__init__(self, parent, **self._kwargs)
        for child in self.children:
            text = child._kwargs.pop('tab_name')
            if not text:
                print('[WARNING] Child of notebook does not have a tab name.')
                continue
            selected = child._kwargs.pop('tab_selected', False)
            child.pack(self)
            self.AddPage(child, text, selected)
    
class WxPopupWindow(WxQuickContainer, wx.PopupWindow):
    def pack(self, parent=None):
        center = self._kwargs.pop('center', False)
        super().pack(parent)

        if center:
            if parent:
                self.CenterOnParent()
            else:
                res = wx.GetDisplaySize()
                center = [res.GetWidth()/2, res.GetHeight()/2]
                size = self.GetSize()
                self.SetPosition((center[0]/2 - size.GetWidth()/2,
                                  center[1]/2 - size.GetHeight()/2))

class WxStaticBox(WxQuickContainer, wx.StaticBox): pass
class WxStaticBoxSizer(WxSizerMixin, wx.StaticBoxSizer):
    def pack(self, parent):
        box = wx.StaticBox(parent, label=self._kwargs.pop('label'))
        super().pack(parent, box)

class ScrolledSizerPanel(WxQuickContainer, ScrolledPanel):
    def pack(self, parent=None):
        super().pack(parent)

        # Sizer layout expects only one child, which is the sizer
        sizer = self.children[0]
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Layout()
        sizer.Fit(self)
        self.SetupScrolling()

class SizerPanel(WxQuickContainer, wx.Panel):
    def pack(self, parent=None):
        bgcolor = self._kwargs.pop('bg_color', None)
        super().pack(parent)

        if bgcolor:
            self.SetBackgroundColour(wx.Colour(bgcolor[0], bgcolor[1], bgcolor[2]))
            
        # SizerPanel expects only one child, which is the sizer
        sizer = self.children[0]
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.Layout()
        sizer.Fit(self)

class Spacer(WxQuickWidget, containers.Spacer): pass
class VBox(WxSizerMixin, containers.VerticalBox): pass
class HBox(WxSizerMixin, containers.HorizontalBox): pass

def HSpacer(size):
    return Spacer((size, 0))

def VSpacer(size):
    return Spacer((0, size))

def StretchSpacer(proportion=1):
    return Spacer((0, 0), proportion)

# wx.SizerItem configuration
class Layout:
    def __init__(self, **kwargs):
        config_defaults = {
            'proportion': 0,
            'flag': 0,
            'border': 0}

        for k, v in config_defaults.items():
            setattr(self, k, kwargs.get(k, v))

    def _set_border_size(self, border_size):
        if border_size is not None:
            self.border = border_size
        
    def center(self):
        self.flag |= wx.ALIGN_CENTER
        return self

    def center_vertical(self):
        self.flag |= wx.ALIGN_CENTER_VERTICAL
    
    def expand(self):
        self.flag |= wx.EXPAND
        return self

    def border_all(self, border=None):
        self.flag |= wx.ALL
        self._set_border_size(border)
        return self

    def border_left(self, border):
        self.flag |= wx.LEFT
        self._set_border_size(border)
        return self
    
    def border_left_right(self, border=None):
        self.flag |= wx.LEFT|wx.RIGHT
        self._set_border_size(border)
        return self

    def border_right(self, border):
        self.flag |= wx.RIGHT
        self._set_border_size(border)
        return self

    def border_top_bottom(self, border=None):
        self.flag |= wx.TOP|wx.BOTTOM
        self._set_border_size(border)
        return self

# Font
def BoldFont(point_size, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL):
    return util.bold_font(point_size, family, style)

def Font(point_size,
         family=wx.FONTFAMILY_DEFAULT,
         style=wx.FONTSTYLE_NORMAL,
         weight=wx.FONTWEIGHT_NORMAL,
         underline=False,
         face=''):
    return util.font(point_size, family, style, weight, underline, face)

# Convenience Dialogs
def ErrorDialog(error, caption, parent=None):
    return wx.MessageDialog(parent, error, caption, wx.OK|wx.ICON_ERROR)

def InfoDialog(error, caption, parent=None):
    return wx.MessageDialog(parent, error, caption, wx.OK|wx.ICON_INFORMATION)

def ConfirmDialog(error, caption, parent=None):
    return wx.MessageDialog(parent,
                            error,
                            caption,
                            wx.YES|wx.NO|wx.NO_DEFAULT|wx.ICON_WARNING)

def DirDialog(prompt,
              style=wx.DD_DEFAULT_STYLE,
              parent=None,
              defaultPath=None):
    
    if not defaultPath:
        defaultPath = wx.StandardPaths.Get().GetDocumentsDir()
        
    return wx.DirDialog(parent, prompt, style=style, defaultPath=defaultPath)
