`convert_mfile` fails on recent IPython versions
============================================

I'm trying to convert one of my Matlab `.m` files into an IPython notebook using `pymatbridge.publish.convert_mfile`, so I can re-run it interactively with the `%%matlab` magic. Something like:

```python
from pymatbridge.publish import convert_mfile
convert_mfile('my_script.m')
```

On older IPython this used to work, but with a recent IPython install it blows up partway through and no `.ipynb` is written. The notebook construction code in `publish.py` seems to be calling into `IPython.nbformat` in a way that doesn't match what current IPython exposes anymore, so the function never gets to actually serialize anything.

Could `convert_mfile` be updated so it works against current `IPython.nbformat` and produces a notebook file that opens cleanly in the notebook UI? The end result I want is the same as before — a `.ipynb` with the matlab-magic loader at the top, then alternating markdown / `%%matlab` code cells corresponding to the `%`-comments and code blocks in the m-file.
