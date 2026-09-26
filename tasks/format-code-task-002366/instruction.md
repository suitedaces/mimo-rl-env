pvsystem.Array.get_irradiance raises an error if solar_zenith is passed as a float
**Bug Description**
`pvsystem.get_irradiance` documentation says solar_zenith can be passed as a float or a Series. However, if `dni_extra` is not defined and `solar_zenith` is passed as float, then `solar_zenith.index` is not defined and the call to `irradiance.get_extra_irradiance` with `solar_zenith.index` as an argument fails.

**To Reproduce**
Steps to reproduce the behavior:
`test_sys = pvsystem.PVSystem()`
`test_sys.get_irradiance(0.0, 0.0, 0.0, 0.0, 0.0)`

**Error message** 
`AttributeError: 'float' object has no attribute 'index'`

**Expected behavior**
Return a DataFrame containing the irradiance components, as specified in [the documentation](https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.pvsystem.Array.get_irradiance.html).

**Possible solutions**
1.  Ask for datetime if `dni_extra` is not passed as argument
2. Remove float from supported types for `solar_zenith`

**Versions:**
 - ``pvlib.__version__``: 0.9.0
 - ``pandas.__version__``: 1.3.3
 - python: 3.9
