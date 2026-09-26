DeprecationWarning for pkg_resources.declare_namespace("google.logging")
Starting from `setuptools==67.3.0`, it has started raising DeprecationWarning. Some libraries treat them as errors during testing.

See: https://setuptools.pypa.io/en/latest/history.html#v67-3-0.

```python
/lib/python3.11/site-packages/pkg_resources/__init__.py:2804: DeprecationWarning: Deprecated call to `pkg_resources.declare_namespace('google.logging')`.
  Implementing implicit namespace packages (as specified in PEP 420) is preferred to `pkg_resources.declare_namespace`. See https://setuptools.pypa.io/en/latest/references/keywords.html#keyword-namespace-packages
    declare_namespace(pkg)
```

See similar discussion in https://github.com/matplotlib/matplotlib/issues/25244 and https://github.com/pypa/setuptools/pull/3434#issuecomment-1435697632. 

Also opened a similar issue in `google.cloud`: https://github.com/googleapis/python-storage/issues/1000.
