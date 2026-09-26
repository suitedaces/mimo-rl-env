pandas plotting raises ValueError on style strings that should be valid according to spec.
#### Code Sample

```python
import pandas as pd
from numpy.random import random
import matplotlib.pyplot as plt

data = random((7,4))
fmt = 'd'

plt.plot(data, fmt, color='green') # works as expected (no error)

df = pd.DataFrame(data)
df.plot(color='green', style=fmt)

# The previous line raises ValueError:
# Cannot pass 'style' string with a color symbol and 'color' keyword argument.
# Please use one or the other or pass 'style' without a color symbol
```

#### Full Stack Trace
```python
Traceback (most recent call last):

  File "<ipython-input-178-b2322b55aff5>", line 1, in <module>
    runfile('G:/irreplacable stuff/Scripts/playground/playground.py', wdir='G:/irreplacable stuff/Scripts/playground')

  File "C:\ProgramData\Anaconda2\lib\site-packages\spyder\utils\site\sitecustomize.py", line 705, in runfile
    execfile(filename, namespace)

  File "C:\ProgramData\Anaconda2\lib\site-packages\spyder\utils\site\sitecustomize.py", line 87, in execfile
    exec(compile(scripttext, filename, 'exec'), glob, loc)

  File "G:/irreplacable stuff/Scripts/playground/playground.py", line 30, in <module>
    df.plot(color='green', style='d')

  File "C:\ProgramData\Anaconda2\lib\site-packages\pandas\plotting\_core.py", line 2677, in __call__
    sort_columns=sort_columns, **kwds)

  File "C:\ProgramData\Anaconda2\lib\site-packages\pandas\plotting\_core.py", line 1902, in plot_frame
    **kwds)

  File "C:\ProgramData\Anaconda2\lib\site-packages\pandas\plotting\_core.py", line 1727, in _plot
    plot_obj = klass(data, subplots=subplots, ax=ax, kind=kind, **kwds)

  File "C:\ProgramData\Anaconda2\lib\site-packages\pandas\plotting\_core.py", line 931, in __init__
    MPLPlot.__init__(self, data, **kwargs)

  File "C:\ProgramData\Anaconda2\lib\site-packages\pandas\plotting\_core.py", line 182, in __init__
    self._validate_color_args()

  File "C:\ProgramData\Anaconda2\lib\site-packages\pandas\plotting\_core.py", line 215, in _validate_color_args
    "Cannot pass 'style' string with a color "

ValueError: Cannot pass 'style' string with a color symbol and 'color' keyword argument. Please use one or the other or pass 'style' without a color symbol
```
#### Problem description

`df.plot` should just pass the `style` kwarg as `fmt` arg to `matplotlib.axes.plot` but it does does some extra (sloppy) validation where it thinks that valid marker style symbols are color symbols and raises an error if the color is already defined elsewhere. The problem is clearly in `_core.py`, line 213.

This problem affects the following standard marker styles (key corresponds to `m` in the example code):
```python
{u'd': u'thin_diamond',
 u'h': u'hexagon1',
 u'o': u'circle',
 u'p': u'pentagon',
 u's': u'square',
 u'v': u'triangle_down',
 u'x': u'x'}
```

#### Expected Output
`df.plot(color='green', style=fmt)` should simply plot the plot the same way as `plt.plot(data, fmt, color='green')` without raising errors. All legal values for `fmt` arg in `pyplot.plot` should be legal for the `style` kwarg in `df.plot`.

#### Output of ``pd.show_versions()``

<details>
INSTALLED VERSIONS
------------------
commit: None
python: 2.7.14.final.0
python-bits: 64
OS: Windows
OS-release: 10
machine: AMD64
processor: Intel64 Family 6 Model 45 Stepping 7, GenuineIntel
byteorder: little
LC_ALL: None
LANG: en
LOCALE: None.None

pandas: 0.22.0
pytest: 3.5.0
pip: 9.0.3
setuptools: 39.0.1
Cython: 0.28.2
numpy: 1.14.2
scipy: 1.0.1
pyarrow: None
xarray: None
IPython: 5.6.0
sphinx: 1.7.2
patsy: 0.5.0
dateutil: 2.7.2
pytz: 2018.4
blosc: None
bottleneck: 1.2.1
tables: 3.4.2
numexpr: 2.6.4
feather: None
matplotlib: 2.2.2
openpyxl: 2.5.2
xlrd: 1.1.0
xlwt: 1.3.0
xlsxwriter: 1.0.4
lxml: 4.2.1
bs4: 4.6.0
html5lib: 1.0.1
sqlalchemy: 1.2.6
pymysql: None
psycopg2: None
jinja2: 2.10
s3fs: None
fastparquet: None
pandas_gbq: None
pandas_datareader: None
</details>
