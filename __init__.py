import wx
from meta import WxContainer, WxWidget
import containers
import event

# Container Packing functions

def child_packer(container, parent=None):
    container.wxClass.__init__(container, parent, **container._kwargs)
    for child in container.children:
        child.pack(container)
    
def frame_packer(container, parent=None, show=False, center=True):
    child_packer(container, parent)
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
        container.Add(child, child.proportion, child.flag, child.border)

def menu_packer(menu, frame):
    menu.title = menu._kwargs.get('title', '')
    menu.wxClass.__init__(menu)
    for item_id, item_text, item_help, callback in menu.children:
        menuitem = menu.Append(item_id, item_text, item_help)
        frame.Bind(wx.EVT_MENU, menuitem_cb_wrapper(menuitem, callback), menuitem)

def menubar_packer(menubar, frame):
    frame.CreateStatusBar()
    menubar.wxClass.__init__(menubar)
    for menu in menubar.children:
        menu.pack(frame)
        menubar.Append(menu, menu.title)

    frame.SetMenuBar(menubar)

        
# Wrapper Classes

class WxButton(WxWidget, wx.Button): events = [event.button]
class WxFrame(WxContainer, wx.Frame): packer = frame_packer
class WxHtmlWindow(WxWidget, wx.html.HtmlWindow): pass
class WxListBox(WxWidget, wx.ListBox): events = [event.listbox]
class WxMenu(WxContainer,wx.Menu): packer = menu_packer
class WxMenuBar(WxContainer, wx.MenuBar): packer = menubar_packer
class WxNotebook(WxContainer, wx.Notebook): packer = notebook_pack
class WxStaticText(WxWidget, wx.StaticText): pass
class WxTextCtrl(WxWidget, wx.TextCtrl): events = [event.text]
class SizerPanel(WxContainer, wx.Panel): packer = sizer_layout_packer
class VBox(WxContainer, containers.VerticalBox): packer = sizer_packer
class HBox(WxContainer, containers.HorizontalBox): packer = sizer_packer

class WxCheckListBox(WxWidget, wx.CheckListBox): 
    events = [event.checklistbox, event.listbox]
