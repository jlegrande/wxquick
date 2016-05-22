import wx
from wx.lib.intctrl import IntCtrl
from wx.lib.scrolledpanel import ScrolledPanel
from meta import WxContainer, WxWidget
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
        msg = "Non wx widget parent passed to child's constructor when packing " \
              "frame. Parent was: " + str(parent)
        print msg
        exc = traceback.format_exc()
        print exc
        wx.MessageDialog(None,
                         '%s\n\n%s' % (msg, exc),
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
        spacer_size = getattr(child, 'spacer_size', 0)

        if spacer_size == 0:
            container.Add(child, child.proportion, child.flag, child.border)
        else:
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
    
# Wrapper Classes

class WxButton(WxWidget, wx.Button): events = [event.button]
class WxDialog(WxContainer, wx.Dialog): packer = dialog_packer
class WxFrame(WxContainer, wx.Frame): packer = frame_packer
class WxHtmlWindow(WxWidget, wx.html.HtmlWindow): pass
class WxIntCtrl(WxWidget, IntCtrl): events = [event.text]
class WxListBox(WxWidget, wx.ListBox): events = [event.listbox]
class WxMenu(WxContainer,wx.Menu): packer = menu_packer
class WxMenuBar(WxContainer, wx.MenuBar): packer = menubar_packer
class WxNotebook(WxContainer, wx.Notebook): packer = notebook_pack
class WxStaticLine(WxWidget, wx.StaticLine): pass
class WxStaticText(WxWidget, wx.StaticText): pass
class WxTextCtrl(WxWidget, wx.TextCtrl): events = [event.text]

class WxCheckListBox(WxWidget, wx.CheckListBox): 
    events = [event.checklistbox, event.listbox]

class DialogButtons(WxWidget, containers.DialogButtons):
    events = [event.button]
    packer = dlg_button_szr_packer
    
class ScrolledSizerPanel(WxContainer, ScrolledPanel): packer = sizer_layout_packer
class SizerPanel(WxContainer, wx.Panel): packer = sizer_layout_packer
class Spacer(WxWidget, containers.Spacer): pass

class VBox(WxContainer, containers.VerticalBox): packer = sizer_packer
class HBox(WxContainer, containers.HorizontalBox): packer = sizer_packer



