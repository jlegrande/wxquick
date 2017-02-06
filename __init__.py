import wx
import wx.html
from wx.grid import Grid
from wx.lib.intctrl import IntCtrl
from wx.lib.masked import TextCtrl
from wx.lib.scrolledpanel import ScrolledPanel
from meta import WxContainer, WxWidget
import util
import containers
import event

# Container Packing functions

def child_packer(container, parent=None):
    container.wxClass.__init__(container, parent, **container._kwargs)

    for child in container.children:
        child.pack(container)
        
def frame_packer(container, parent=None, show=False, center=True):
    try:
        child_packer(container, parent)
    except TypeError as e:
        import traceback
        exc = traceback.format_exc()
        print exc
        wx.MessageDialog(None,
                         '%s' % exc,
                         'Invalid Parent', wx.OK|wx.ICON_ERROR).ShowModal()
        raise
        
    #container.Fit()
    if center:
        container.CenterOnScreen()
        
    if show:
        container.Show()

def notebook_pack(container, parent=None, show=False):
    container.wxClass.__init__(container, parent, **container._kwargs)
    for child in container.children:
        text = child._kwargs.pop('tab_name')
        if not text:
            print '[WARNING] Child of notebook does not have a tab name.'
            continue
        selected = child._kwargs.pop('tab_selected', False)
        child.pack(container)
        container.AddPage(child, text, selected)

def sizer_layout_packer(container, parent=None):
    child_packer(container, parent)
    
    # Sizer layout expects only one child, which is the sizer
    sizer = container.children[0]
    container.SetSizer(sizer)
    container.SetAutoLayout(True)
    container.Layout()
    sizer.Fit(container)

def sizer_packer(container, parent):
    container.wxClass.__init__(container, **container._kwargs)
    for child in container.children:
        child.pack(parent)
        spacer_size = getattr(child, 'spacer_size', None)
        if not spacer_size:
            container.Add(child, child.proportion, child.flag, child.border)
        else:
            try:
                w, h = spacer_size
                container.Add(w, h, 0)
            except TypeError:
                container.AddSpacer(spacer_size)

        if container.item_gap > 0:
            container.AddSpacer(container.item_gap)
    
def menu_packer(menu, frame):
    menu.title = menu._kwargs.get('title', '')
    menu.wxClass.__init__(menu)
    for item_id, item_text, item_help, callback in menu.children:
        menuitem = menu.Append(item_id, item_text, item_help)
        frame.Bind(wx.EVT_MENU, event.menuitem_cb_wrapper(menuitem, callback), menuitem)

def menubar_packer(menubar, frame):
    frame.CreateStatusBar()
    menubar.wxClass.__init__(menubar)
    for menu in menubar.children:
        menu.pack(frame)
        menubar.Append(menu, menu.title)

    frame.SetMenuBar(menubar)

def dialog_packer(dialog, parent=None, center=True):
    child_packer(dialog, parent)
    if len(dialog.children) == 1:
        try:
            dialog.SetSizer(dialog.children[0])
            dialog.SetAutoLayout(True)
            if not dialog._kwargs.get('size'):
                dialog.Fit()
        except TypeError:
            pass

    if center:
        dialog.CenterOnParent()
        
def dlg_button_szr_packer(butt_szr, parent):
    butt_szr.wxClass.__init__(butt_szr, parent, *butt_szr._args)
    cb = butt_szr.callback
    if cb:
        child_sizer = butt_szr.GetChildren()[0].GetSizer()
        buttons = [c.GetWindow() for c in child_sizer.GetChildren() if c.IsWindow()]

        for event in butt_szr.events:
            for butt in buttons:
                event(butt, cb)

def popup_packer(popup, parent=None):
    center = popup._kwargs.pop('center', False)
    child_packer(popup, parent)

    if center:
        if parent:
            popup.CenterOnParent()
        else:
            res = wx.GetDisplaySize()
            center = [res.GetWidth()/2, res.GetHeight()/2]
            size = popup.GetSize()
            popup.SetPosition((center[0]/2 - size.GetWidth()/2,
                              center[1]/2 - size.GetHeight()/2))
def grid_packer(grid, parent):
    rows, cols = grid._kwargs.pop('grid_size', (1,1))
    colnames = grid._kwargs.pop('columns', [])
    grid.wxClass.__init__(grid, parent, *grid._args, **grid._kwargs)
    grid.CreateGrid(rows, cols)
    for i, name in enumerate(colnames):
        grid.SetColLabelValue(i, name)

def listctrl_packer(listctrl, parent):
    cols = listctrl._kwargs.pop('columns', [])
    meta.widg_pack(listctrl, parent)

    for i, col in enumerate(cols):
        listctrl.InsertColumn(i, col)

# Wrapper Classes

class WxButton(WxWidget, wx.Button): events = [event.button]
class WxCheckBox(WxWidget, wx.CheckBox): events = [event.checkbox]
class WxChoice(WxWidget, wx.Choice): events = [event.choice]
class WxDatePicker(WxWidget, wx.DatePickerCtrl): pass
class WxDialog(WxContainer, wx.Dialog): packer = dialog_packer
class WxFrame(WxContainer, wx.Frame): packer = frame_packer
class WxGenericDatePicker(WxWidget, wx.GenericDatePickerCtrl): pass
class WxGrid(WxWidget, Grid): packer = grid_packer
class WxHtmlWindow(WxWidget, wx.html.HtmlWindow): pass
class WxIntCtrl(WxWidget, IntCtrl): events = [event.text]
class WxListBox(WxWidget, wx.ListBox): events = [event.listbox]

class WxMenu(WxContainer,wx.Menu): packer = menu_packer
class WxMenuBar(WxContainer, wx.MenuBar): packer = menubar_packer
class WxNotebook(WxContainer, wx.Notebook): packer = notebook_pack
class WxPopupWindow(WxContainer, wx.PopupWindow): packer = popup_packer
class WxRadioBox(WxWidget, wx.RadioBox): pass
class WxStaticLine(WxWidget, wx.StaticLine): pass
class WxStaticText(WxWidget, wx.StaticText): pass
class WxSlider(WxWidget, wx.Slider): events = [event.scroll]
class WxTextCtrl(WxWidget, wx.TextCtrl): events = [event.text]

class WxCheckListBox(WxWidget, wx.CheckListBox): 
    events = [event.checklistbox, event.listbox]

class WxListCtrl(WxWidget, wx.ListCtrl):
    packer = listctrl_packer
    events = [event.listctrl_item_selection]

class WxEditableListCtrl(WxWidget, util.EditableListCtrl):
    packer = listctrl_packer
    events = [event.listctrl_item_selection]

class DialogButtons(WxWidget, containers.DialogButtons):
    events = [event.button]
    packer = dlg_button_szr_packer

class MaskedTextCtrl(WxWidget, TextCtrl): pass
class ScrolledSizerPanel(WxContainer, ScrolledPanel): packer = sizer_layout_packer
class SizerPanel(WxContainer, wx.Panel): packer = sizer_layout_packer
class Spacer(WxWidget, containers.Spacer): pass

class VBox(WxContainer, containers.VerticalBox): packer = sizer_packer
class HBox(WxContainer, containers.HorizontalBox): packer = sizer_packer

def HSpacer(size): return Spacer((size, 0))
def VSpacer(size): return Spacer((0, size))

def BoldFont(point_size, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL):
    return util.bold_font(point_size, family, style)

def Font(point_size,
         family=wx.FONTFAMILY_DEFAULT,
         style=wx.FONTSTYLE_NORMAL,
         weight=wx.FONTWEIGHT_NORMAL,
         underline=False,
         face=''):
    return util.font(point_size, family, style, weight, underline, face)

def ErrorDialog(error, caption, parent=None):
    return wx.MessageDialog(parent, error, caption, wx.OK|wx.ICON_ERROR)

def InfoDialog(error, caption, parent=None):
    return wx.MessageDialog(parent, error, caption, wx.OK|wx.ICON_INFORMATION)

def ConfirmDialog(error, caption, parent=None):
    return wx.MessageDialog(parent,
                            error,
                            caption,
                            wx.YES|wx.NO|wx.NO_DEFAULT|wx.ICON_WARNING)
