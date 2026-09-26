BUG: Set type check is too strict when creating Series from dict keys
- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the latest version of pandas.

- [ ] (optional) I have confirmed this bug exists on the master branch of pandas.

---

#### Code Sample, a copy-pastable example

```python
from pandas import Series
Series({'a': 1, 'b': 2}.keys())
```

#### Problem description

Since Python 3.7 dictionaries are ordered, and therefore their keys are also ordered. In older pandas versions (prior to 1.1?) it was possible to create a `Series` from keys of a dictionary. A fix to #32582 intended to prevent an issue with sets seems to be breaking the creation of `Series` from keys of a dictionary.

Currently the following is raised:

```python
/pandas/core/series.py in __init__(self, data, index, dtype, name, copy, fastpath)
    325                     data = data.copy()
    326             else:
--> 327                 data = sanitize_array(data, index, dtype, copy, raise_cast_failure=True)
    328 
    329                 data = SingleBlockManager.from_array(data, index)

/pandas/core/construction.py in sanitize_array(data, index, dtype, copy, raise_cast_failure)
    450         subarr = _try_cast(arr, dtype, copy, raise_cast_failure)
    451     elif isinstance(data, abc.Set):
--> 452         raise TypeError("Set type is unordered")
    453     elif lib.is_scalar(data) and index is not None and dtype is not None:
    454         data = maybe_cast_to_datetime(data, dtype)

TypeError: Set type is unordered
```

#### Expected Output

Same as of `Series(list({'a': 1, 'b': 2}.keys()))`, i.e.:

```
0    a
1    b
dtype: object
```

#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------
commit           : f2ca0a2665b2d169c97de87b8e778dbed86aea07
python           : 3.7.5.final.0
python-bits      : 64
OS               : Linux
OS-release       : 5.4.0-42-generic
Version          : #46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020
machine          : x86_64
processor        : x86_64
byteorder        : little
LC_ALL           : None
LANG             : en_GB.UTF-8
LOCALE           : en_GB.UTF-8

pandas           : 1.1.1
numpy            : 1.18.1
pytz             : 2019.3
dateutil         : 2.8.1
pip              : 19.2.3
setuptools       : 41.2.0
Cython           : None
pytest           : 5.3.5
hypothesis       : None
sphinx           : None
blosc            : None
feather          : None
xlsxwriter       : None
lxml.etree       : None
html5lib         : None
pymysql          : None
psycopg2         : None
jinja2           : 2.11.1
IPython          : 7.12.0
pandas_datareader: None
bs4              : None
bottleneck       : None
fsspec           : None
fastparquet      : None
gcsfs            : None
matplotlib       : None
numexpr          : None
odfpy            : None
openpyxl         : None
pandas_gbq       : None
pyarrow          : None
pytables         : None
pyxlsb           : None
s3fs             : None
scipy            : 1.4.1
sqlalchemy       : None
tables           : None
tabulate         : None
xarray           : None
xlrd             : None
xlwt             : None
numba            : None

</details>
