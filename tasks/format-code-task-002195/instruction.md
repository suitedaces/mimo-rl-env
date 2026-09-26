API: Return type of DataFrame.asof
#### Code Sample, a copy-pastable example if possible

```python
# Your code here
In [135]: df = pd.DataFrame({'a': range(10), 'b': range(10)}, 
                            index=pd.date_range('2014-01-01', periods=10))

In [136]: df.asof('2014-01-15')
Out[136]: 
a    9
b    9
Name: 2014-01-10 00:00:00, dtype: int32

In [137]: df.asof('2013-01-15')
Out[137]: nan
```
#### Problem description

I got tripped up by `[137]` returning a scalar - it makes sense for a `Series`, but not sure it does with a  `DataFrame` lookup?  So maybe it should instead return an empty Series, e.g.
```
In [138]: df.asof('2013-01-15')
Out[138]: 
a  NaN
b  NaN
dtype: float64
```


#### Output of ``pd.show_versions()``
<details>
# Paste the output here pd.show_versions() here
INSTALLED VERSIONS
------------------
commit: None
python: 3.5.2.final.0
python-bits: 64
OS: Windows
OS-release: 7
machine: AMD64
processor: Intel64 Family 6 Model 78 Stepping 3, GenuineIntel
byteorder: little
LC_ALL: None
LANG: None
LOCALE: None.None

pandas: 0.19.0
nose: 1.3.7
pip: 8.1.2
setuptools: 23.0.0
Cython: 0.24.1
numpy: 1.11.2
scipy: 0.18.1
statsmodels: 0.6.1
xarray: 0.8.2
IPython: 5.1.0
sphinx: 1.3.1
patsy: 0.4.1
dateutil: 2.5.3
pytz: 2016.4
blosc: None
bottleneck: 1.1.0
tables: 3.2.2
numexpr: 2.6.1
matplotlib: 1.5.3
openpyxl: 2.3.2
xlrd: 1.0.0
xlwt: 1.1.2
xlsxwriter: 0.9.2
lxml: 3.6.0
bs4: 4.4.1
html5lib: 0.999
httplib2: 0.9.2
apiclient: 1.5.3
sqlalchemy: 1.0.13
pymysql: None
psycopg2: None
jinja2: 2.8
boto: 2.40.0
pandas_datareader: 0.2.1
</details>
