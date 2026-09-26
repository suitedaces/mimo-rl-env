BUG: In Series all null-values are printed as NaN
### Pandas version checks

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [X] I have confirmed this bug exists on the master branch of pandas.


### Reproducible Example

```python
import pandas as pd
import numpy as np
s=pd.Series([1, 2, 3, 4], [True, None, np.nan, pd.NaT])
print(s)
```


### Issue Description

All null-keys are printed as NaN:

```
True    1
NaN     2
NaN     3
NaN     5
```

This is confusing

### Expected Behavior

```
True    1
None    2
nan    3
NaT   5
```
would be clearer



### Installed Versions

<details>

INSTALLED VERSIONS
------------------
commit           : c9508507024377ad9848555e5f5eb3556476c385
python           : 3.8.5.final.0
python-bits      : 64
OS               : Linux
OS-release       : 4.4.0-53-generic
Version          : #74-Ubuntu SMP Fri Dec 2 15:59:10 UTC 2016
machine          : x86_64
processor        : x86_64
byteorder        : little
LC_ALL           : None
LANG             : en_US.UTF-8
LOCALE           : en_US.UTF-8

pandas           : 1.4.0.dev0+1594.gc950850
numpy            : 1.19.1
pytz             : 2020.1
dateutil         : 2.8.1
pip              : 20.2.3
setuptools       : 58.0.4
Cython           : 0.29.24
pytest           : 6.0.2
hypothesis       : 5.28.0
sphinx           : 3.2.1
blosc            : None
feather          : None
xlsxwriter       : 1.3.6
lxml.etree       : 4.5.2
html5lib         : 1.1
pymysql          : None
psycopg2         : None
jinja2           : 2.11.2
IPython          : 7.18.1
pandas_datareader: None
bs4              : 4.9.1
bottleneck       : 1.3.2
fsspec           : 0.8.2
fastparquet      : 0.4.1
gcsfs            : 0.7.1
matplotlib       : 3.3.2
numexpr          : 2.7.1
odfpy            : None
openpyxl         : 3.0.5
pandas_gbq       : None
pyarrow          : 1.0.1
pyxlsb           : None
s3fs             : 0.4.2
scipy            : 1.5.2
sqlalchemy       : 1.3.19
tables           : 3.6.1
tabulate         : 0.8.7
xarray           : 0.16.1
xlrd             : 1.2.0
xlwt             : 1.3.0
numba            : 0.51.2
zstandard        : None

</details>
