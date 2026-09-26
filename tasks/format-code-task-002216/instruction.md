Inconsistent MultiIndex behaviour when indexing selects no rows
```python
mi = pd.MultiIndex.from_arrays([
        np.array(['a', 'a', 'b', 'b']), 
        np.array(['1', '2', '2', '3']), 
        np.array(['alpha', 'beta', 'alpha', 'beta']),
    ], names=['one', 'two', 'three'])
df = pd.DataFrame(np.random.rand(4, 3), index=mi)
df2 = df.loc[('b', '1', slice(None)), :]
print(df2)
print(df2.index)
```
Output
```
Empty DataFrame
Columns: [0, 1, 2]
Index: []
MultiIndex(levels=[['a', 'b'], ['1', '2', '3'], ['alpha', 'beta']],
           labels=[[], [], []],
           names=['one', 'two', 'three'])
```
Indexing `df` results in an empty dataframe in this case. However, if the third level of the MultiIndex is left out (as below), it results in a `KeyError`.
```python
df2 = df.loc[('b', '1'), :]
```

In my opinion, this behaviour is confusing and inconsistent. Preferably, both cases would throw `KeyError`.

This particular behaviour was previously discussed in issue #19543.

#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------
commit: None
python: 3.6.1.final.0
python-bits: 64
OS: Linux
OS-release: 4.4.0-43-Microsoft
machine: x86_64
processor: x86_64
byteorder: little
LC_ALL: None
LANG: en_US.UTF-8
LOCALE: en_US.UTF-8

pandas: 0.22.0
pytest: None
pip: 9.0.1
setuptools: 27.2.0
Cython: None
numpy: 1.14.0
scipy: 1.0.0
pyarrow: None
xarray: None
IPython: 6.2.1
sphinx: None
patsy: None
dateutil: 2.6.1
pytz: 2017.3
blosc: None
bottleneck: None
tables: 3.4.2
numexpr: 2.6.4
feather: None
matplotlib: None
openpyxl: 2.4.9
xlrd: 1.1.0
xlwt: None
xlsxwriter: None
lxml: None
bs4: None
html5lib: 1.0b10
sqlalchemy: None
pymysql: None
psycopg2: None
jinja2: 2.10
s3fs: None
fastparquet: None
pandas_gbq: None
pandas_datareader: None

</details>
