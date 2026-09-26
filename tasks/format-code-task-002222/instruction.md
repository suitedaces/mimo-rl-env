BUG: numpy functions (eg, np.add) on DataFrames with 'out' parameter no longer work properly
- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the latest version of pandas.

- [ ] (optional) I have confirmed this bug exists on the master branch of pandas.

---

#### Code Sample, a copy-pastable example

```python
# works
foo = np.array([1,2,3,4]).reshape(2,2)
bar = np.zeros_like(foo)
np.add(foo, 1, out=bar)
print(bar)

# doesn't work. bar remains an array of zeros
foo = np.array([1,2,3,4]).reshape(2,2)
df = pd.DataFrame(foo)
bar = np.zeros_like(df)
np.add(df, 1, out=bar)
print(bar)
```

#### Problem description

Many numpy functions accept an `out` parameter as a way of storing the result. In the current pandas version (1.2.3), when the numpy function takes in a DataFrame as input, it no longer stores the result to the `out` array.

In pandas 1.0.1 (and earlier, on my other machine), the behavior works as expected. (see Expected Output). I am using numpy==1.19 for both machines.

Curiously, note that this problem is not seen for `pd.Series`. The below code works fine:

```python
foo = np.array([1,2,3,4])
series = pd.Series(foo)
bar = np.zeros_like(series)
np.add(series, 1, out=bar)
print(bar)
```

One workaround is to instead use `np.add(df.values, 1, out=bar)` but I am using several packages that require the older behavior.

#### Expected Output

```python
>>> print(bar)

[[2 3]
 [4 5]]
```

#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------
commit           : f2c8480af2f25efdbd803218b9d87980f416563e
python           : 3.7.4.final.0
python-bits      : 64
OS               : Linux
OS-release       : 3.10.0-1062.1.1.el7.x86_64
Version          : #1 SMP Fri Sep 13 22:55:44 UTC 2019
machine          : x86_64
processor        : x86_64
byteorder        : little
LC_ALL           : None
LANG             : en_GB.UTF-8
LOCALE           : en_GB.UTF-8

pandas           : 1.2.3
numpy            : 1.19.5
pytz             : 2019.3
dateutil         : 2.8.1
pip              : 19.3.1
setuptools       : 41.4.0
Cython           : 0.29.21
pytest           : None
hypothesis       : None
sphinx           : None
blosc            : None
feather          : None
xlsxwriter       : None
lxml.etree       : 4.5.0
html5lib         : None
pymysql          : None
psycopg2         : None
jinja2           : 2.10.3
IPython          : 7.11.1
pandas_datareader: None
bs4              : 4.9.1
bottleneck       : None
fsspec           : 0.8.2
fastparquet      : None
gcsfs            : None
matplotlib       : 3.1.3
numexpr          : 2.7.0
odfpy            : None
openpyxl         : 3.0.4
pandas_gbq       : None
pyarrow          : 0.13.0
pyxlsb           : None
s3fs             : 0.5.1
scipy            : 1.4.1
sqlalchemy       : 1.3.13
tables           : 3.6.1
tabulate         : 0.8.7
xarray           : None
xlrd             : 1.2.0
xlwt             : None
numba            : 0.49.1

</details>
