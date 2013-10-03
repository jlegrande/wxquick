import wx
from meta import WxContainer, WxWidget
import containers
import event

# Container Packing functions

def child_packer(container, parent=None):
    container.wxClass.__init__(container, parent, **container._kwargs)
    for child in container.children:
        child.pack(container)
    
def frame_packer(container, parent=None, show=False):
    child_packer(container, parent)
    container.Fit()
    if show:
        container.Show()

def sizer_layout_packer(container, parent=None):
    child_packer(container, parent)
    
    # Sizer layout expects only one child, which is the sizer
    sizer = container.children[0]
    container.SetSizer(sizer)
    container.SetAutoLayout(True)
    sizer.Fit(container)

def sizer_packer(container, parent):
    container.wxClass.__init__(container, **container._kwargs)
    for child in container.children:
        child.pack(parent)
        container.Add(child, child.proportion, child.flag, child.border)

def menu_packer(menu, frame):
    menu.name = menu._kwargs.get('name', '')
    menu.wxClass.__init__(menu)
    for item_id, item_text, item_help, callback in menu.children:
        menuitem = menu.Append(item_id, item_text, item_help)
        frame.Bind(wx.EVT_MENU, callback, menuitem)

def menubar_packer(menubar, parent):
    parent.CreateStatusBar()
    menubar.wxClass.__init__(menubar)
    for menu in menubar.children:
        menu.pack(parent)
        menubar.Append(menu, menu.name)

    parent.SetMenuBar(menubar)

        
# Wrapper Classes

class WxFrame(WxContainer, wx.Frame): packer = frame_packer
class WxStaticText(WxWidget, wx.StaticText): pass
class WxListBox(WxWidget, wx.ListBox): events = [event.listbox]
class WxMenu(WxContainer,wx.Menu): packer = menu_packer
class WxMenuBar(WxContainer, wx.MenuBar): packer = menubar_packer
class WxTextCtrl(WxWidget, wx.TextCtrl): pass
class SizerPanel(WxContainer, wx.Panel): packer = sizer_layout_packer
class VBox(WxContainer, containers.VerticalBox): packer = sizer_packer
class HBox(WxContainer, containers.HorizontalBox): packer = sizer_packer

class WxCheckListBox(WxWidget, wx.CheckListBox): 
    events = [event.checklistbox, event.listbox]
