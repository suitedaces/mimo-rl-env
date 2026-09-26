BUG: roundtrip fidelity for a tz-aware DTI with a fixed format HDFStore
#### Code Sample, a copy-pastable example if possible

```python
import pandas as pd

time = pd.Timestamp('2000-01-01 01:00:00', tz='US/Eastern')
df = pd.DataFrame(data=[0], index=[time])
df.to_hdf('./df.hdf', 'df')
df2 = pd.read_hdf('./df.hdf')
print('DataFrames: ')
print(df)
print(df2)

print('\nFirst Element of index: ')
print(df.index[0])
print(df2.index[0])

print('\nValues: ')
print(df.index[0].value)
print(df2.index[0].value)

print('\nTimezone Info:')
print(df.index[0].tzinfo)
print(df2.index[0].tzinfo)
```
#### Problem description

The output of the above code sample is:
```
DataFrames: 
                           0
2000-01-01 01:00:00-05:00  0
                           0
2000-01-01 01:00:00-05:00  0

First Element of index: 
2000-01-01 01:00:00-05:00
2000-01-01 06:00:00-05:00

Values: 
946706400000000000
946724400000000000

Timezone Info:
US/Eastern
US/Eastern
```
I would expect the outputs to be the same in all these cases. The error occurs after saving and loading a DataFrame with a timezone aware index. The index remains timezone aware but the index value changes to an incorrect value. This incorrect value seems to be the value it would have if the local time were actually UTC time. This error occurs for an index with multiple entries as well.

#### Expected Output
```
DataFrames: 
                           0
2000-01-01 01:00:00-05:00  0
                           0
2000-01-01 01:00:00-05:00  0

First Element of index: 
2000-01-01 01:00:00-05:00
2000-01-01 01:00:00-05:00

Values: 
946706400000000000
946706400000000000

Timezone Info:
US/Eastern
US/Eastern

```
#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------
commit: None
python: 3.6.2.final.0
python-bits: 64
OS: Linux
OS-release: 3.10.0-514.21.1.el7.x86_64
machine: x86_64
processor: x86_64
byteorder: little
LC_ALL: None
LANG: en_US.UTF-8
LOCALE: en_US.UTF-8

pandas: 0.20.3
pytest: None
pip: 9.0.1
setuptools: 36.3.0
Cython: None
numpy: 1.12.1
scipy: 0.19.1
xarray: 0.9.6
IPython: 6.2.0
sphinx: None
patsy: 0.4.1
dateutil: 2.6.1
pytz: 2017.2
blosc: None
bottleneck: 1.2.1
tables: 3.4.2
numexpr: 2.6.4
feather: None
matplotlib: 2.0.0
openpyxl: None
xlrd: None
xlwt: None
xlsxwriter: None
lxml: None
bs4: None
html5lib: 0.999999999
sqlalchemy: None
pymysql: None
psycopg2: None
jinja2: 2.9.6
s3fs: None
pandas_gbq: None
pandas_datareader: None

</details>
