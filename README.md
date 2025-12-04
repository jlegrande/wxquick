wxquick
=======

wxquick is a declarative layer on top of wxPython (think QML for Qt). Build windows by composing wrapped widgets and sizers, then call `pack()` to instantiate and lay them out.

Quick start
-----------
```python
import wx, wxquick

app = wx.App(False)
frame = wxquick.WxFrame(
    wxquick.VBox(
        wxquick.WxStaticText(label="Name"),
        wxquick.WxTextCtrl(value="Bret Hart"),
        wxquick.WxButton(label="Submit", callback=lambda *_: print("clicked")),
        item_gap=8,
    ),
    title="Profile",
    size=(320, 200),
)
frame.pack(show=True)
app.MainLoop()
```

Hello World
-----------
```python
import wx
import wxquick

app = wx.App(False)
frame = wxquick.WxFrame(title='Hello World')
frame.pack(show=True)
app.MainLoop()
```

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

Adding children incrementally
-----------------------------
You can grow containers after creation using `+=`:
```python
from wxquick import WxFrame, WxTextCtrl, WxButton

frame = WxFrame(title="Incremental")
frame += WxTextCtrl(value="First field")
frame += WxButton(label="Save", callback=lambda *_: print("saved"))
frame.pack(show=True)
```

Layouts with sizers and grids
-----------------------------
```python
from wxquick import WxFrame, WxGridBagSizer, WxStaticText, WxTextCtrl

frame = WxFrame(
    WxGridBagSizer(
        WxStaticText("First", grid_pos=(0, 0)), WxTextCtrl(value="Macho", grid_pos=(0, 1)),
        WxStaticText("Last", grid_pos=(1, 0)), WxTextCtrl(value="Man", grid_pos=(1, 1)),
        cols=2, vgap=5, hgap=5,
    ),
    title="Grid Example",
)
frame.pack(show=True)
```

Scrollable content
------------------
```python
from wxquick import WxFrame, ScrolledSizerPanel, VBox, WxStaticText, VSpacer

frame = WxFrame(
    ScrolledSizerPanel(
        VBox(*[WxStaticText(f"Row {i}") for i in range(40)], item_gap=4)
    ),
    size=(240, 320),
    title="Scroller",
)
frame.pack(show=True)
```

Wrapped wx classes
------------------
- Containers: `WxFrame`, `WxDialog`, `WxNotebook`, `WxPopupWindow`, `WxMenu`, `WxMenuBar`, `WxFlexGridSizer`, `WxGridBagSizer`, `WxStaticBox`, `WxStaticBoxSizer`, `SizerPanel`, `ScrolledSizerPanel`, `VBox`, `HBox`, `Spacer`/`HSpacer`/`VSpacer`/`StretchSpacer`.
- Buttons: `WxButton`, `WxBitmapButton`, `WxGenButton`, `WxGradientButton`, `WxPlateButton`, `DialogButtons`.
- Text/display: `WxStaticText`, `WxGenStaticText`, `WxStaticBitmap`, `WxStaticLine`, `WxHtmlWindow`, `WxHtmlListBox`, `WxWebView`, `LEDNumberCtrl`.
- Input/selectors: `WxTextCtrl`, `WxIntCtrl`, `MaskedTextCtrl`, `MaskedTimeCtrl`, `WxCheckBox`, `WxCheckListBox`, `WxRadioBox`, `WxChoice`, `WxComboBox`, `WxDatePicker`, `WxGenericDatePicker`, `WxSlider`.
- Lists/grids: `WxListBox`, `WxListCtrl`, `WxEditableListCtrl`, `WxEditableListBox`, `WxGrid`.

Notes
-----
- Use `callback=` to bind to wrapped events; handlers receive a friendly event string and widget references.
- `pack(show=True)` constructs children, centers frames by default, and shows the window; omit `show` when embedding in a parent.
- Packer tips: `VBox`/`HBox` accept `item_gap` to add consistent spacing; use `Layout()` helpers (e.g., `.border_all(5).expand()`) on children via `item_layout=` to set sizer flags/borders.
- Callback shapes: list-type widgets send `(event_str, label, index, widget, evt)`; buttons send `('clicked', widget, evt)`; checkbox sends `('checked'|'unchecked', widget, evt)`; sliders send `('scroll', value, widget, evt)`; text controls send `('text_ctrl_changed', value, evt)`.
