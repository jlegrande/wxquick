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
    
def text_ctrl_change_wrapper(text_ctrl, callback):
    def cb(evt):
        callback('text_ctrl_changed', text_ctrl.GetValue(), evt)
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

def text(text_ctrl, callback):
    wx.EVT_TEXT(text_ctrl, 
                text_ctrl.GetId(), 
                text_ctrl_change_wrapper(text_ctrl, callback))
