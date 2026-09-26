BUG: to_numeric incorrectly converting values >= 16,777,217 with downcast='float'
### 

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the [latest version](https://pandas.pydata.org/docs/whatsnew/index.html) of pandas.

- [X] I have confirmed this bug exists on the master branch of pandas.


### Reproducible Example

```python
import pandas as pd
import numpy as np

# Series: Result 608202560.0
pd.to_numeric(pd.Series([608202549]), downcast='float')

#Series: Result 608202560.0
pd.to_numeric(pd.Series([608202549.0]), downcast='float')

# Single: Result 608202549
pd.to_numeric(608202549, downcast='float')

# List: Result array([608202560, 608202560])
pd.to_numeric([608202548, 608202549], downcast='float').astype(int)

# Range: 1st issue at 16777217
arr = np.arange(0, 6e8, dtype='int64')
a = pd.Series(arr)
b = pd.to_numeric(a, downcast='float').astype(int)
np.where(a != b)[0]
```


### Issue Description

When attempting to use `to_numeric()` on a Pandas Series or list with values >= 16777217, the resulting float is not expected given the input number.

```python
pd.to_numeric(pd.Series([608202549]), downcast='float')
0    608202560.0 

>>> pd.to_numeric(pd.Series([608202549.0]), downcast='float')
0    608202560.0
```

This behavior does not occur if the value is passed as a scalar, but does also appear if a List is passed. By comparing values within a range, it seems the issue starts from 16,777,217 onward. This seems to have roots in the discussion about 32 bit floating point in this [Stack Overflow](https://github.com/pandas-dev/pandas/issues/23676#issuecomment-438488603) as well as another Pandas issue on float issues with rank #18271

**Edit-** I updated this issue to be clear that this is affecting both integers and floats larger than 16,777,217

### Expected Behavior

`to_numeric()` should yield the same functional number in float form as the original value(s)

### Installed Versions

<details>

>>> pd.show_versions()

INSTALLED VERSIONS
------------------
commit           : 73c68257545b5f8530b7044f56647bd2db92e2ba
python           : 3.9.4.final.0
python-bits      : 64
OS               : Darwin
OS-release       : 20.6.0
Version          : Darwin Kernel Version 20.6.0: Wed Jun 23 00:26:27 PDT 2021; root:xnu-7195.141.2~5/RELEASE_ARM64_T8101
machine          : arm64
processor        : arm
byteorder        : little
LC_ALL           : None
LANG             : en_US.UTF-8
LOCALE           : en_US.UTF-8

pandas           : 1.3.3
numpy            : 1.21.2
pytz             : 2021.1
dateutil         : 2.8.2
pip              : 21.0.1
setuptools       : 54.2.0
Cython           : None
pytest           : None
hypothesis       : None
sphinx           : None
blosc            : None
feather          : None
xlsxwriter       : None
lxml.etree       : None
html5lib         : None
pymysql          : None
psycopg2         : None
jinja2           : None
IPython          : None
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
pyxlsb           : None
s3fs             : None
scipy            : None
sqlalchemy       : None
tables           : None
tabulate         : None
xarray           : None
xlrd             : None
xlwt             : None
numba            : None

</details>
