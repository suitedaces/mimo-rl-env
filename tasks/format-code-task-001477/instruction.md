Plotly Scatter 3D not rendering colorbar title correctly
#### ALL software version info

python: 3.8.8 | packaged by conda-forge | (default, Feb 20 2021, 16:22:27) 
[GCC 9.3.0]
python-bits: 64
OS: Linux
OS-release: 5.4.0-1030-aws
machine: x86_64
processor: x86_64
byteorder: little
LC_ALL: None
LANG: C.UTF-8
LOCALE: en_US.UTF-8
Firefox: 88.0.1 (64-bit)
Conda: 4.10.0

pandas: 1.2.4
holoviews: 1.14.3
plotly: 4.14.3
jupyterlab: 2.2.6 
jupyterlab_server: 1.2.0

#### Description of expected behavior and the observed behavior

I am expecting that the colorbar title would be based on the column title that is designated as color in the options. However, it appears that something is not right, and instead of giving a clean title, it has `im(` prefix to the title. Ex. `im('temperature'`. Also, if I try to pass in `title` to `colorbar_opts` it gives me a `TypeError` saying that `title` already exist.

After reading the error message and digging into the code. I suspect this line is causing this issue:
https://github.com/holoviz/holoviews/blob/989c3c304a34e5043a52eba87dd056b6e48d9eea/holoviews/plotting/plotly/element.py#L603-L611

- `str(eldim)[1:-1] ` seems strange to me, and but this does result in the title issue above. If `eldim` is `dim('temperature')` doing `[1:-1]` would result in `im('temperature'`.
- Regarding optional title for `colorbar_opts` is there a reason that this is hardcoded in the code? I have made plots with the bokeh stuff, and that option is available. Seems like this behavior is confusing.

#### Complete, minimal, self-contained example code that reproduces the issue

```python
import pandas as pd
import holoviews as hv
from holoviews import opts

hv.extension('plotly')

df = pd.read_csv('https://raw.githubusercontent.com/cormorack/development/main/tempsf_test.csv', index_col='id')

scatter_opts = opts.Scatter3D(
    color='temperature', 
    cmap='viridis', 
    colorbar=True, 
    size=2,
    clim=(1, 7),

    # Adding colorbar_opts title will fail ...
    # colorbar_opts={'title': 'Temperature (degC)'}
)

hv.Scatter3D(data=df).opts(scatter_opts)
```

#### Stack traceback and/or browser JavaScript console output

<details>
<summary>Traceback when using colorbar_opts</summary>

```
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
/opt/conda/envs/cava-data/lib/python3.8/site-packages/IPython/core/formatters.py in __call__(self, obj, include, exclude)
    968 
    969             if method is not None:
--> 970                 return method(include=include, exclude=exclude)
    971             return None
    972         else:

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/core/dimension.py in _repr_mimebundle_(self, include, exclude)
   1315         combined and returned.
   1316         """
-> 1317         return Store.render(self)
   1318 
   1319 

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/core/options.py in render(cls, obj)
   1403         data, metadata = {}, {}
   1404         for hook in hooks:
-> 1405             ret = hook(obj)
   1406             if ret is None:
   1407                 continue

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/ipython/display_hooks.py in pprint_display(obj)
    280     if not ip.display_formatter.formatters['text/plain'].pprint:
    281         return None
--> 282     return display(obj, raw_output=True)
    283 
    284 

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/ipython/display_hooks.py in display(obj, raw_output, **kwargs)
    250     elif isinstance(obj, (CompositeOverlay, ViewableElement)):
    251         with option_state(obj):
--> 252             output = element_display(obj)
    253     elif isinstance(obj, (Layout, NdLayout, AdjointLayout)):
    254         with option_state(obj):

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/ipython/display_hooks.py in wrapped(element)
    144         try:
    145             max_frames = OutputSettings.options['max_frames']
--> 146             mimebundle = fn(element, max_frames=max_frames)
    147             if mimebundle is None:
    148                 return {}, {}

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/ipython/display_hooks.py in element_display(element, max_frames)
    190         return None
    191 
--> 192     return render(element)
    193 
    194 

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/ipython/display_hooks.py in render(obj, **kwargs)
     66         renderer = renderer.instance(fig='png')
     67 
---> 68     return renderer.components(obj, **kwargs)
     69 
     70 

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/renderer.py in components(self, obj, fmt, comm, **kwargs)
    408                 doc = Document()
    409                 with config.set(embed=embed):
--> 410                     model = plot.layout._render_model(doc, comm)
    411                 if embed:
    412                     return render_model(model, comm)

/opt/conda/envs/cava-data/lib/python3.8/site-packages/panel/viewable.py in _render_model(self, doc, comm)
    425         if comm is None:
    426             comm = state._comm_manager.get_server_comm()
--> 427         model = self.get_root(doc, comm)
    428 
    429         if config.embed:

/opt/conda/envs/cava-data/lib/python3.8/site-packages/panel/viewable.py in get_root(self, doc, comm, preprocess)
    482         """
    483         doc = init_doc(doc)
--> 484         root = self._get_model(doc, comm=comm)
    485         if preprocess:
    486             self._preprocess(root)

/opt/conda/envs/cava-data/lib/python3.8/site-packages/panel/layout/base.py in _get_model(self, doc, root, parent, comm)
    111         if root is None:
    112             root = model
--> 113         objects = self._get_objects(model, [], doc, root, comm)
    114         props = dict(self._init_params(), objects=objects)
    115         model.update(**self._process_param_change(props))

/opt/conda/envs/cava-data/lib/python3.8/site-packages/panel/layout/base.py in _get_objects(self, model, old_objects, doc, root, comm)
    101             else:
    102                 try:
--> 103                     child = pane._get_model(doc, root, model, comm)
    104                 except RerenderError:
    105                     return self._get_objects(model, current_objects[:i], doc, root, comm)

/opt/conda/envs/cava-data/lib/python3.8/site-packages/panel/pane/holoviews.py in _get_model(self, doc, root, parent, comm)
    237             plot = self.object
    238         else:
--> 239             plot = self._render(doc, comm, root)
    240 
    241         plot.pane = self

/opt/conda/envs/cava-data/lib/python3.8/site-packages/panel/pane/holoviews.py in _render(self, doc, comm, root)
    302                 kwargs['comm'] = comm
    303 
--> 304         return renderer.get_plot(self.object, **kwargs)
    305 
    306     def _cleanup(self, root):

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/renderer.py in get_plot(self_or_cls, obj, doc, renderer, comm, **kwargs)
    241             init_key = tuple(v if d is None else d for v, d in
    242                              zip(plot.keys[0], defaults))
--> 243             plot.update(init_key)
    244         else:
    245             plot = obj

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plot.py in update(self, key)
    980     def update(self, key):
    981         if len(self) == 1 and ((key == 0) or (key == self.keys[0])) and not self.drawn:
--> 982             return self.initialize_plot()
    983         item = self.__getitem__(key)
    984         self.traverse(lambda x: setattr(x, '_updated', True))

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plotly/element.py in initialize_plot(self, ranges, is_geo)
    124         """
    125         # Get element key and ranges for frame
--> 126         fig = self.generate_plot(self.keys[-1], ranges, is_geo=is_geo)
    127         self.drawn = True
    128 

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plotly/element.py in generate_plot(self, key, ranges, element, is_geo)
    180         # Get data and options and merge them
    181         data = self.get_data(element, ranges, style, is_geo=is_geo)
--> 182         opts = self.graph_options(element, ranges, style, is_geo=is_geo)
    183 
    184         components = {

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plotly/chart.py in graph_options(self, element, ranges, style, **kwargs)
     68 
     69     def graph_options(self, element, ranges, style, **kwargs):
---> 70         opts = super(ScatterPlot, self).graph_options(element, ranges, style, **kwargs)
     71         cdim = element.get_dimension(self.color_index)
     72         if cdim:

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plotly/element.py in graph_options(self, element, ranges, style, is_geo, **kwargs)
    250 
    251         if self._style_key is not None:
--> 252             styles = self._apply_transforms(element, ranges, style)
    253 
    254             # If style starts with '{_style_key}_', remove the prefix.  This way

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plotly/element.py in _apply_transforms(self, element, ranges, style)
    377             numeric = isinstance(val, np.ndarray) and val.dtype.kind in 'uifMm'
    378             if ('color' in k and isinstance(val, np.ndarray) and numeric):
--> 379                 copts = self.get_color_opts(v, element, ranges, style)
    380                 new_style.pop('cmap', None)
    381                 new_style.update(copts)

/opt/conda/envs/cava-data/lib/python3.8/site-packages/holoviews/plotting/plotly/element.py in get_color_opts(self, eldim, element, ranges, style)
    609                 title = eldim.pprint_label
    610 
--> 611             opts['colorbar'] = dict(title=title, **self.colorbar_opts)
    612             opts['showscale'] = True
    613         else:

TypeError: type object got multiple values for keyword argument 'title'
```

</details>

#### Screenshots or screencasts of the bug in action

![Screenshot from 2021-05-26 14-38-42](https://user-images.githubusercontent.com/17802172/119734604-17af3c80-be30-11eb-8407-e4315f47be6f.png)

Thank you so much for your time and help on this 😄 I hope it's a simple bug fix.
