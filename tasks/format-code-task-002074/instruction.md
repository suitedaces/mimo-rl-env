<!-- Please describe the issue in detail here, and fill in the fields below -->

f2py tries to report the version of f2py in the docstring of the extension module. However, as the import of ```__svn_version__```  in ```numpy/numpy/f2py/__version__.py``` always fails, the f2py version reported in the docstrings always has the value of ```'2'```.

f2py should instead use a versioning mechanism that actually works, or at least include the NumPy version in the resported f2py version. This way it would be possible for projects like SciPy to query the version of f2py used for cmpilation (which might be different from the currently imported numpy) and correct for known bugs, such as the recently fixed issue with callbacks to Python not being threadsafe.

https://github.com/numpy/numpy/blob/581eab37b5d558ba9b8035f3fa82cfa617e70e26/numpy/f2py/__version__.py#L1-L8

Here is an example showing the problem:
```
>>> _cobyla.__doc__
"This module '_cobyla' is auto-generated with f2py (version:2).\nFunctions:\n  x,dinfo = minimize(calcfc,m,x,rhobeg,rhoend,dinfo,iprint=1,maxfun=100,calcfc_extra_args=())\n."
```

One concrete way I'd find useful: have the compiled module expose something like a `__f2py_numpy_version__` attribute that downstream code can query at runtime.
