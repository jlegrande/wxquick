import wx
import collections

ListBoxData = collections.namedtuple('ListBoxData', ['falseval', 'trueval', 'condfunc'])

def lb_cb_wrapper(listbox, callback, lbdata):
    def cb(evt):
        sel = evt.GetSelection()
        event_string = lbdata.falseval
        if lbdata.condfunc(sel):
            event_string = lbdata.trueval
            
        callback(event_string, listbox.GetString(sel), sel, listbox, evt)

    return cb
    
def menuitem_cb_wrapper(menuitem, callback):
    def cb(evt):
        callback(menuitem.GetLabel(), menuitem, evt)

    return cb
    
def button_cb_wrapper(button, callback):
    def cb(evt):
        callback('clicked', button, evt)

    return cb
    
def choice_cb_wrapper(choice, callback):
    def cb(evt):
        callback(evt.GetString(), choice, evt)
    return cb

def text_ctrl_change_wrapper(text_ctrl, callback):
    def cb(evt):
        callback('text_ctrl_changed', text_ctrl.GetValue(), evt)
    return cb

def list_ctrl_item_selection_wrapper(list_ctrl, callback):
    def cb(evt):
        evt_str = 'selected'
        idx = evt.GetIndex()
        if not list_ctrl.IsSelected(idx):
            evt_str = 'deselected'
        callback(evt_str, idx, list_ctrl, evt)

    return cb
    
# Event Handlers

def checklistbox(listbox, callback):
    lbdata = ListBoxData('unchecked', 'checked', listbox.IsChecked)
    cb = lb_cb_wrapper(listbox, callback, lbdata)
    wx.EVT_CHECKLISTBOX(listbox, listbox.GetId(), cb)

def listbox(listbox, callback):
    lbdata = ListBoxData('unselected', 'selected', listbox.IsSelected)
    cb = lb_cb_wrapper(listbox, callback, lbdata)
    wx.EVT_LISTBOX(listbox, listbox.GetId(), cb)

def button(button, callback):
    wx.EVT_BUTTON(button, button.GetId(), button_cb_wrapper(button, callback))

def choice(wxchoice, callback):
    wx.EVT_CHOICE(wxchoice,
                  wxchoice.GetId(),
                  choice_cb_wrapper(wxchoice, callback))
    
def text(text_ctrl, callback):
    wx.EVT_TEXT(text_ctrl, 
                text_ctrl.GetId(), 
                text_ctrl_change_wrapper(text_ctrl, callback))

def listctrl_item_selection(list_ctrl, callback):
    wx.EVT_LIST_ITEM_SELECTED(list_ctrl,
                              list_ctrl.GetId(),
                              list_ctrl_item_selection_wrapper(list_ctrl,
                                                               callback))

    wx.EVT_LIST_ITEM_DESELECTED(list_ctrl,
                                list_ctrl.GetId(),
                                list_ctrl_item_selection_wrapper(list_ctrl,
                                                                 callback))
