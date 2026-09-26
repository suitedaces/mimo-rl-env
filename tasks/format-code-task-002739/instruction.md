DIckey Fuller test breaks on constant values
#### Describe the bug

Dickey-Fuller test gives error when testing with constant values.

#### Code Sample, a copy-pastable example if possible


```python
adfuller(np.full(8, 5.0))
```
`RuntimeWarning: divide by zero encountered in log
  llf = -nobs2*np.log(2*np.pi) - nobs2*np.log(ssr / nobs) - nobs2`

#### Expected Output

I have expected that this series is stationary

#### Output of ``import statsmodels.api as sm; sm.show_versions()``

<details>

INSTALLED VERSIONS
------------------
Python: 3.10.6.final.0
OS: Linux 5.15.0-50-generic #56-Ubuntu SMP Tue Sep 20 13:23:26 UTC 2022 x86_64
byteorder: little
LC_ALL: None
LANG: en_US.UTF-8

statsmodels
===========

Installed: 0.13.2 (/home/michael/.local/lib/python3.10/site-packages/statsmodels)

Required Dependencies
=====================

cython: Not installed
numpy: 1.23.3 (/home/michael/.local/lib/python3.10/site-packages/numpy)
scipy: 1.9.2 (/home/michael/.local/lib/python3.10/site-packages/scipy)
pandas: 1.5.0 (/home/michael/.local/lib/python3.10/site-packages/pandas)
    dateutil: 2.8.2 (/home/michael/.local/lib/python3.10/site-packages/dateutil)
patsy: 0.5.3 (/home/michael/.local/lib/python3.10/site-packages/patsy)

Optional Dependencies
=====================

matplotlib: 3.6.1 (/home/michael/.local/lib/python3.10/site-packages/matplotlib)
    backend: module://matplotlib_inline.backend_inline 
cvxopt: Not installed
joblib: Not installed

Developer Tools
================

IPython: 8.5.0 (/home/michael/.local/lib/python3.10/site-packages/IPython)
    jinja2: 3.1.2 (/home/michael/.local/lib/python3.10/site-packages/jinja2)
sphinx: Not installed
    pygments: 2.13.0 (/home/michael/.local/lib/python3.10/site-packages/pygments)
pytest: Not installed
virtualenv: 20.16.5 (/home/michael/.local/lib/python3.10/site-packages/virtualenv)

</details>
