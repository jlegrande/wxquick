wxquick
=======

wxquick is a declarative layer on top of wxPython, similar to QML for Qt. The goal is to simplify the building of wxPython GUIs.


Hello World:
------------

```python
import wx
import wxquick

app = wx.App(False)
frame = wxquick.WxFrame(title='Hello World')
frame.pack(show=True)
app.MainLoop()
```

What's the frame.pack() call all about? That's where the magic happens. The packer is what lays out the child widgets in the frame (and their children, and their children's children, etc.).

Not very interesting eh? Let's try a modified version of the "Building a simple text editor" example from http://wiki.wxpython.org/Getting%20Started


Building a simple text editor
-----------------------------

```python
import wx
from wxquick import WxFrame, WxTextCtrl

app = wx.App(False)
frame = WxFrame(WxTextCtrl(style=wx.TE_MULTILINE), title='Small Editor')
frame.pack(show=True)
app.MainLoop()
```

This is a little more interesting and you start to see the benefits of declaratively building your GUI. We don't have to tell the TextCtrl who its parent is because we pass the TextCtrl directly to the Frame's constructor and wxquick does the rest. If we had multiple children to pass to the frame we could do:

```python
frame = WxFrame(widget1, ..., widgetN, title='Small Editor')
```

This same pattern could be used for any container like a Frame, Panel, Sizer, etc.

We could also build the simple text editor this way:

```python
# boring imports....

app = wx.App(False)
frame = WxFrame(title='Small Editor')
text_ctrl = WxTextCtrl(style=wx.TE_MULTILINE)

frame += text_ctrl
frame.pack(show=True)

app.MainLoop()
```
     
Neat huh?        


TODO:
-----
* More/Improved documentation and examples.
* Wrap more wxPython classes