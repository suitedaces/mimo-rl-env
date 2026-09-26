Removing selected points from a Points layer while hovering over an unselected point causes infinite out of bounds errors
## 🐛 Bug

I believe this error is caused, either in whole or in part, by [this line of code](https://github.com/napari/napari/blob/master/napari/layers/points/points.py#L1404). The `remove_selected` method invariably `_value` is invariably set to `None` despite it being a wildly unsafe assumption that the user is hovering over one of the deleted points.

## To Reproduce

Steps to reproduce the behavior:

1. Open an image in Napari
2. Add a Points layer
2. Add at least two points to the layer
3. Select at least one point, and hover over another without selecting it
4. Press the delete key

<details>
<summary>Example stack trace</summary>

```
IndexError                                Traceback (most recent call last)
~\mambaforge\envs\napari\lib\site-packages\vispy\app\backends\_qt.py in mouseMoveEvent(self=<vispy.app.backends._qt.CanvasBackendDesktop object>, ev=<PyQt5.QtGui.QMouseEvent object>)
    484         if self._vispy_canvas is None:
    485             return
--> 486         self._vispy_mouse_move(
        self._vispy_mouse_move = <bound method BaseCanvasBackend._vispy_mouse_move of <vispy.app.backends._qt.CanvasBackendDesktop object at 0x000002848C9E7AF0>>
        global native = undefined
        ev = <PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0>
        global pos = undefined
        ev.pos.x = undefined
        ev.pos.y = undefined
        global modifiers = undefined
        self._modifiers = <bound method QtBaseCanvasBackend._modifiers of <vispy.app.backends._qt.CanvasBackendDesktop object at 0x000002848C9E7AF0>>
    487             native=ev,
    488             pos=(ev.pos().x(), ev.pos().y()),

~\mambaforge\envs\napari\lib\site-packages\vispy\app\base.py in _vispy_mouse_move(self=<vispy.app.backends._qt.CanvasBackendDesktop object>, **kwargs={'buttons': [], 'last_event': <MouseEvent blocked=False button=None buttons=[]...ources=[] time=1628908603.588419 type=mouse_move>, 'last_mouse_press': None, 'modifiers': (), 'native': <PyQt5.QtGui.QMouseEvent object>, 'pos': (269, 425), 'press_event': None})
    211             kwargs['button'] = self._vispy_mouse_data['press_event'].button
    212
--> 213         ev = self._vispy_canvas.events.mouse_move(**kwargs)
        ev = undefined
        self._vispy_canvas.events.mouse_move = <vispy.util.event.EventEmitter object at 0x000002848C9EF880>
        kwargs = {'native': <PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0>, 'pos': (269, 425), 'modifiers': (), 'buttons': [], 'press_event': None, 'last_event': <MouseEvent blocked=False button=None buttons=[] delta=[0. 0.] handled=False is_dragging=False last_event=None modifiers=() native=<PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0> pos=[335 397] press_event=None source=None sources=[] time=1628908603.588419 type=mouse_move>, 'last_mouse_press': None}
    214         self._vispy_mouse_data['last_event'] = ev
    215         return ev

~\mambaforge\envs\napari\lib\site-packages\vispy\util\event.py in __call__(self=<vispy.util.event.EventEmitter object>, *args=(), **kwargs={'buttons': [], 'last_event': <MouseEvent blocked=False button=None buttons=[]...ources=[] time=1628908603.588419 type=mouse_move>, 'last_mouse_press': None, 'modifiers': (), 'native': <PyQt5.QtGui.QMouseEvent object>, 'pos': (269, 425), 'press_event': None})
    451                     raise RuntimeError('EventEmitter loop detected!')
    452
--> 453                 self._invoke_callback(cb, event)
        self._invoke_callback = <bound method EventEmitter._invoke_callback of <vispy.util.event.EventEmitter object at 0x000002848C9EF880>>
        cb = <bound method QtViewer.on_mouse_move of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>
        event = <MouseEvent blocked=False button=None buttons=[] delta=[0. 0.] handled=False is_dragging=False last_event=MouseEvent modifiers=() native=<PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0> pos=[269 425] press_event=None source=None sources=[] time=1628908607.0735433 type=mouse_move>
    454                 if event.blocked:
    455                     break

~\mambaforge\envs\napari\lib\site-packages\vispy\util\event.py in _invoke_callback(self=<vispy.util.event.EventEmitter object>, cb=<bound method QtViewer.on_mouse_move of <napari._qt.qt_viewer.QtViewer object>>, event=<MouseEvent blocked=False button=None buttons=[]...urces=[] time=1628908607.0735433 type=mouse_move>)
    469             cb(event)
    470         except Exception:
--> 471             _handle_exception(self.ignore_callback_errors,
        global _handle_exception = <function _handle_exception at 0x0000028482439790>
        self.ignore_callback_errors = False
        self.print_callback_errors = 'reminders'
        self = <vispy.util.event.EventEmitter object at 0x000002848C9EF880>
        global cb_event = undefined
        cb = <bound method QtViewer.on_mouse_move of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>
        event = <MouseEvent blocked=False button=None buttons=[] delta=[0. 0.] handled=False is_dragging=False last_event=MouseEvent modifiers=() native=<PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0> pos=[269 425] press_event=None source=None sources=[] time=1628908607.0735433 type=mouse_move>
    472                               self.print_callback_errors,
    473                               self, cb_event=(cb, event))

~\mambaforge\envs\napari\lib\site-packages\vispy\util\event.py in _invoke_callback(self=<vispy.util.event.EventEmitter object>, cb=<bound method QtViewer.on_mouse_move of <napari._qt.qt_viewer.QtViewer object>>, event=<MouseEvent blocked=False button=None buttons=[]...urces=[] time=1628908607.0735433 type=mouse_move>)
    467     def _invoke_callback(self, cb, event):
    468         try:
--> 469             cb(event)
        cb = <bound method QtViewer.on_mouse_move of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>
        event = <MouseEvent blocked=False button=None buttons=[] delta=[0. 0.] handled=False is_dragging=False last_event=MouseEvent modifiers=() native=<PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0> pos=[269 425] press_event=None source=None sources=[] time=1628908607.0735433 type=mouse_move>
    470         except Exception:
    471             _handle_exception(self.ignore_callback_errors,

~\mambaforge\envs\napari\lib\site-packages\napari\_qt\qt_viewer.py in on_mouse_move(self=<napari._qt.qt_viewer.QtViewer object>, event=<MouseEvent blocked=False button=None buttons=[]...urces=[] time=1628908607.0735433 type=mouse_move>)
    856             The vispy event that triggered this method.
    857         """
--> 858         self._process_mouse_event(mouse_move_callbacks, event)
        self._process_mouse_event = <bound method QtViewer._process_mouse_event of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>
        global mouse_move_callbacks = <function mouse_move_callbacks at 0x0000028486E4B160>
        event = <MouseEvent blocked=False button=None buttons=[] delta=[0. 0.] handled=False is_dragging=False last_event=MouseEvent modifiers=() native=<PyQt5.QtGui.QMouseEvent object at 0x00000284870711F0> pos=[269 425] press_event=None source=None sources=[] time=1628908607.0735433 type=mouse_move>
    859
    860     def on_mouse_release(self, event):

~\mambaforge\envs\napari\lib\site-packages\napari\_qt\qt_viewer.py in _process_mouse_event(self=<napari._qt.qt_viewer.QtViewer object>, mouse_callbacks=<function mouse_move_callbacks>, event=<MouseEvent blocked=False button=None buttons=[]...urces=[] time=1628908607.0735433 type=mouse_move>)
    815
    816         # Update the cursor position
--> 817         self.viewer.cursor.position = self._map_canvas2world(list(event.pos))
        self.viewer.cursor.position = (377.33085102453333, 47.69792969088679)
        self._map_canvas2world = <bound method QtViewer._map_canvas2world of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>
        global list = undefined
        event.pos = array([269, 425])
    818
    819         # Add the cursor position to the event

~\mambaforge\envs\napari\lib\site-packages\napari\utils\events\evented_model.py in __setattr__(self=Cursor(position=(377.33085102453333, 47.69792969088679), scaled=True, size=1, style='standard'), name='position', value=(377.33085102453333, 47.69792969088679))
    153         are_equal = self.__eq_operators__.get(name, operator.eq)
    154         if not are_equal(after, before):
--> 155             getattr(self.events, name)(value=after)  # emit event
        global getattr = undefined
        self.events = <napari.utils.events.event.EmitterGroup object at 0x0000028487CA3D00>
        name = 'position'
        value = (377.33085102453333, 47.69792969088679)
        after = (377.33085102453333, 47.69792969088679)
    156
    157     # expose the private EmitterGroup publically

~\mambaforge\envs\napari\lib\site-packages\napari\utils\events\event.py in __call__(self=<napari.utils.events.event.EventEmitter object>, *args=(), **kwargs={'value': (377.33085102453333, 47.69792969088679)})
    571                     continue
    572
--> 573                 self._invoke_callback(cb, event)
        self._invoke_callback = <bound method EventEmitter._invoke_callback of <napari.utils.events.event.EventEmitter object at 0x0000028487CA3C10>>
        cb = <bound method ViewerModel._on_cursor_position_change of Viewer(axes=Axes(visible=False, labels=True, colored=True, dashed=False, arrows=True), camera=Camera(center=(0.0, 255.5, 255.5), zoom=1.087573385518591, angles=(0.0, 0.0, 90.0), perspective=0.0, interactive=False), cursor=Cursor(position=(377.33085102453333, 47.69792969088679), scaled=True, size=1, style='standard'), dims=Dims(ndim=2, ndisplay=2, last_used=1, range=((0.0, 511.0, 1.0), (0.0, 511.0, 1.0)), current_step=(0, 0), order=(0, 1), axis_labels=('0', '1')), grid=GridCanvas(enabled=False, stride=1, shape=(-1, -1)), layers=[<Image layer 'astronaut' at 0x2849811afa0>, <Points layer 'Points' at 0x2848ac79d60>], scale_bar=ScaleBar(visible=False, colored=False, ticks=True, position='bottom_right', font_size=10.0, unit=None), text_overlay=TextOverlay(visible=False, color=array([1., 1., 1., 1.]), font_size=10.0, position='top_left', text=''), help='hold <space> to pan/zoom', status='Points [352 108]: 0', tooltip=Tooltip(visible=False, text=''), theme='dark', title='napari', mouse_move_callbacks=[], mouse_drag_callbacks=[], mouse_wheel_callbacks=[<function dims_scroll at 0x00000284877A7EE0>], _persisted_mouse_event={}, _mouse_drag_gen={}, _mouse_wheel_gen={}, keymap={'Control-Shift-C': <bound method QtViewer.toggle_console_visibility of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>})>
        event = <Event blocked=False handled=False native=None source=None sources=[] type='position'>
    574                 if event.blocked:
    575                     break

~\mambaforge\envs\napari\lib\site-packages\napari\utils\events\event.py in _invoke_callback(self=<napari.utils.events.event.EventEmitter object>, cb=<bound method ViewerModel._on_cursor_position_ch...viewer.QtViewer object at 0x0000028487CA18B0>>})>, event=<Event blocked=False handled=False native=None source=None sources=[] type='position'>)
    593             cb(event)
    594         except Exception:
--> 595             _handle_exception(
        global _handle_exception = <function _handle_exception at 0x0000028482439790>
        self.ignore_callback_errors = False
        self.print_callback_errors = 'reminders'
        self = <napari.utils.events.event.EventEmitter object at 0x0000028487CA3C10>
        global cb_event = undefined
        cb = <bound method ViewerModel._on_cursor_position_change of Viewer(axes=Axes(visible=False, labels=True, colored=True, dashed=False, arrows=True), camera=Camera(center=(0.0, 255.5, 255.5), zoom=1.087573385518591, angles=(0.0, 0.0, 90.0), perspective=0.0, interactive=False), cursor=Cursor(position=(377.33085102453333, 47.69792969088679), scaled=True, size=1, style='standard'), dims=Dims(ndim=2, ndisplay=2, last_used=1, range=((0.0, 511.0, 1.0), (0.0, 511.0, 1.0)), current_step=(0, 0), order=(0, 1), axis_labels=('0', '1')), grid=GridCanvas(enabled=False, stride=1, shape=(-1, -1)), layers=[<Image layer 'astronaut' at 0x2849811afa0>, <Points layer 'Points' at 0x2848ac79d60>], scale_bar=ScaleBar(visible=False, colored=False, ticks=True, position='bottom_right', font_size=10.0, unit=None), text_overlay=TextOverlay(visible=False, color=array([1., 1., 1., 1.]), font_size=10.0, position='top_left', text=''), help='hold <space> to pan/zoom', status='Points [352 108]: 0', tooltip=Tooltip(visible=False, text=''), theme='dark', title='napari', mouse_move_callbacks=[], mouse_drag_callbacks=[], mouse_wheel_callbacks=[<function dims_scroll at 0x00000284877A7EE0>], _persisted_mouse_event={}, _mouse_drag_gen={}, _mouse_wheel_gen={}, keymap={'Control-Shift-C': <bound method QtViewer.toggle_console_visibility of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>})>
        event = <Event blocked=False handled=False native=None source=None sources=[] type='position'>
    596                 self.ignore_callback_errors,
    597                 self.print_callback_errors,

~\mambaforge\envs\napari\lib\site-packages\napari\utils\events\event.py in _invoke_callback(self=<napari.utils.events.event.EventEmitter object>, cb=<bound method ViewerModel._on_cursor_position_ch...viewer.QtViewer object at 0x0000028487CA18B0>>})>, event=<Event blocked=False handled=False native=None source=None sources=[] type='position'>)
    591     def _invoke_callback(self, cb: Callback, event: Event):
    592         try:
--> 593             cb(event)
        cb = <bound method ViewerModel._on_cursor_position_change of Viewer(axes=Axes(visible=False, labels=True, colored=True, dashed=False, arrows=True), camera=Camera(center=(0.0, 255.5, 255.5), zoom=1.087573385518591, angles=(0.0, 0.0, 90.0), perspective=0.0, interactive=False), cursor=Cursor(position=(377.33085102453333, 47.69792969088679), scaled=True, size=1, style='standard'), dims=Dims(ndim=2, ndisplay=2, last_used=1, range=((0.0, 511.0, 1.0), (0.0, 511.0, 1.0)), current_step=(0, 0), order=(0, 1), axis_labels=('0', '1')), grid=GridCanvas(enabled=False, stride=1, shape=(-1, -1)), layers=[<Image layer 'astronaut' at 0x2849811afa0>, <Points layer 'Points' at 0x2848ac79d60>], scale_bar=ScaleBar(visible=False, colored=False, ticks=True, position='bottom_right', font_size=10.0, unit=None), text_overlay=TextOverlay(visible=False, color=array([1., 1., 1., 1.]), font_size=10.0, position='top_left', text=''), help='hold <space> to pan/zoom', status='Points [352 108]: 0', tooltip=Tooltip(visible=False, text=''), theme='dark', title='napari', mouse_move_callbacks=[], mouse_drag_callbacks=[], mouse_wheel_callbacks=[<function dims_scroll at 0x00000284877A7EE0>], _persisted_mouse_event={}, _mouse_drag_gen={}, _mouse_wheel_gen={}, keymap={'Control-Shift-C': <bound method QtViewer.toggle_console_visibility of <napari._qt.qt_viewer.QtViewer object at 0x0000028487CA18B0>>})>
        event = <Event blocked=False handled=False native=None source=None sources=[] type='position'>
    594         except Exception:
    595             _handle_exception(

~\mambaforge\envs\napari\lib\site-packages\napari\components\viewer_model.py in _on_cursor_position_change(self=Viewer(axes=Axes(visible=False, labels=True, col..._viewer.QtViewer object at 0x0000028487CA18B0>>}), event=<Event blocked=False handled=False native=None source=None sources=[] type='position'>)
    376         active = self.layers.selection.active
    377         if active is not None:
--> 378             self.status = active.get_status(self.cursor.position, world=True)
        self.status = 'Points [352 108]: 0'
        active.get_status = <bound method Layer.get_status of <Points layer 'Points' at 0x2848ac79d60>>
        self.cursor.position = (377.33085102453333, 47.69792969088679)
        global world = undefined
    379             self.help = active.help
    380             if self.tooltip.visible:

~\mambaforge\envs\napari\lib\site-packages\napari\layers\base\base.py in get_status(self=<Points layer 'Points'>, position=(377.33085102453333, 47.69792969088679), world=True)
   1079             String containing a message that can be used as a status update.
   1080         """
-> 1081         value = self.get_value(position, world=world)
        value = undefined
        self.get_value = <bound method Layer.get_value of <Points layer 'Points' at 0x2848ac79d60>>
        position = (377.33085102453333, 47.69792969088679)
        world = True
   1082         return generate_layer_status(self.name, position, value)
   1083

~\mambaforge\envs\napari\lib\site-packages\napari\layers\base\base.py in get_value(self=<Points layer 'Points'>, position=(377.33085102453333, 47.69792969088679), world=True)
    917             if world:
    918                 position = self.world_to_data(position)
--> 919             value = self._get_value(position=tuple(position))
        value = undefined
        self._get_value = <bound method Points._get_value of <Points layer 'Points' at 0x2848ac79d60>>
        position = (377.33085102453333, 47.69792969088679)
        global tuple = undefined
    920         else:
    921             value = None

~\mambaforge\envs\napari\lib\site-packages\napari\layers\points\points.py in _get_value(self=<Points layer 'Points'>, position=(377.33085102453333, 47.69792969088679))
   1352             distances = abs(view_data - displayed_position)
   1353             in_slice_matches = np.all(
-> 1354                 distances <= np.expand_dims(self._view_size, axis=1) / 2,
        distances = array([[ 23.90643223,  63.44399323],
       [ 57.00764609, 165.50606929]])
        global np.expand_dims = <function expand_dims at 0x00000284E22A7940>
        self._view_size = undefined
        global axis = undefined
   1355                 axis=1,
   1356             )

~\mambaforge\envs\napari\lib\site-packages\napari\layers\points\points.py in _view_size(self=<Points layer 'Points'>)
   1246             # Get the point sizes and scale for ndim display
   1247             sizes = (
-> 1248                 self.size[
        self.size = array([[10, 10]])
        global np.ix_ = <function ix_ at 0x00000284E22971F0>
        self._indices_view = array([0, 1])
        self._dims_displayed.mean = undefined
        global axis = undefined
   1249                     np.ix_(self._indices_view, self._dims_displayed)
   1250                 ].mean(axis=1)

IndexError: index 1 is out of bounds for axis 0 with size 1
```

</details>

## Environment

napari: 0.4.10
Platform: Windows-10-10.0.19043-SP0
Python: 3.9.6 | packaged by conda-forge | (default, Jul 11 2021, 03:37:25) [MSC v.1916 64 bit (AMD64)]
Qt: 5.15.2
PyQt5: 5.15.4
NumPy: 1.21.1
SciPy: 1.7.1
Dask: 2021.07.2
VisPy: 0.7.3

OpenGL:
- GL version: 4.6.0 - Build 27.20.100.9749
- MAX_TEXTURE_SIZE: 16384

Screens:
- screen 1: resolution 1280x720, scale 3.0

Plugins:
- console: 0.0.3
- scikit-image: 0.4.10
- svg: 0.1.5
