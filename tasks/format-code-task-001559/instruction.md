BytesWarning thrown in imread in 2.11.1
There seems to be a small regression when calling `imread` and enabling `BytesWarning`s ([-bb](https://docs.python.org/3/using/cmdline.html#cmdoption-b)):

```py
from pathlib import Path

import imageio

image_bytes = Path("image.png").read_bytes()
image = imageio.imread(image_bytes)
```

Run with:

```
python -bb test.py
Traceback (most recent call last):
  File "test.py", line 6, in <module>
    image = imageio.imread(image_bytes)
  File "venv/lib/python3.9/site-packages/imageio/core/functions.py", line 159, in imread
    with imopen(uri, "ri", plugin=format) as file:
  File "venv/lib/python3.9/site-packages/imageio/core/imopen.py", line 221, in imopen
    plugin_instance = config.plugin_class(request, **kwargs)
  File "venv/lib/python3.9/site-packages/imageio/config/plugins.py", line 108, in partial_legacy_plugin
    return LegacyPlugin(request, legacy_plugin)
  File "venv/lib/python3.9/site-packages/imageio/core/legacy_plugin_wrapper.py", line 64, in __init__
    f"`{self._format.name}`" f" can not read `{self._request.raw_uri}`."
BytesWarning: str() on a bytes instance
```

Enabling `BytesWarning`s helps users catch `str`/`bytes` confusion in their own code.

### Environment

Python 3.9.8

```
pip list
Package    Version
---------- -------
click      8.0.1
imageio    2.11.1
numpy      1.21.4
pep517     0.10.0
Pillow     8.4.0
pip        21.3.1
pip-tools  6.4.0
setuptools 57.0.0
toml       0.10.2
wheel      0.36.2
```
