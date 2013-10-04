import wx
import collections

ListBoxData = collections.namedtuple('ListBoxData', ['falseval', 'trueval', 'condfunc'])

def lb_cb_wrapper(listbox, callback, lbdata):
    def cb(evt):
        sel = evt.GetSelection()
        event_string = lbdata.falseval
        
        if lbdata.condfunc(sel):
            event_string = lbdata.trueval
            
        callback(event_string, listbox.GetString(sel), sel, listbox)

    return cb
    
def menuitem_cb_wrapper(menuitem, callback):
    def cb(evt):
        callback(menuitem.GetLabel(), menuitem)
        
# Event Handlers

def checklistbox(listbox, callback):
    lbdata = ListBoxData('unchecked', 'checked', listbox.IsChecked)
    cb = lb_cb_wrapper(listbox, callback, lbdata)
    wx.EVT_CHECKLISTBOX(listbox, listbox.GetId(), cb)

def listbox(listbox, callback):
    lbdata = ListBoxData('unselected', 'selected', listbox.IsSelected)
    cb = lb_cb_wrapper(listbox, callback, lbdata)
    wx.EVT_LISTBOX(listbox, listbox.GetId(), cb)
    
