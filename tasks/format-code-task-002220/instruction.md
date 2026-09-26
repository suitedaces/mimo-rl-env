BUG: ExcelWriter with mode='a' corrupts file
- [x] I have checked that this issue has not already been reported.

- [x]  I have confirmed this bug exists on the latest version of pandas.

- [ ] (optional) I have confirmed this bug exists on the master branch of pandas.

---

**Note**: Please read [this guide](https://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports) detailing how to provide the necessary information for us to reproduce your bug.

#### Code Sample, a copy-pastable example

```python
import pandas as pd

df = pd.DataFrame()

with pd.ExcelWriter('test.xlsx', mode='w', engine='openpyxl') as writer:
    df.to_excel(writer)

with pd.ExcelWriter('test.xlsx', mode='a', engine='openpyxl') as writer:
    df.to_excel(writer)

```

#### Problem description

Appending to excel file with pandas>=1.2 produces file which Excel reports as corrupted and opens only after repair, forcing you to first open and repair file before passing it to someone else.
Looking at file with 7-Zip File Manager shows that after writing file with mode='a', some .xml files (app.xml, core.xml, theme1.xml, sheet1.xml) inside archive are duplicated (somehow). After Excel rapars file duplicates are gone, everything else looks the same.

With pandas 1.1.5 and same versions of other packages everything works as expected.

#### Expected Output

File which could be opened by Excel without any warnings.

#### Output of ``pd.show_versions()``

<details>

INSTALLED VERSIONS
------------------
commit           : 9d598a5e1eee26df95b3910e3f2934890d062caa
python           : 3.8.6.final.0
python-bits      : 64
OS               : Windows
OS-release       : 10
Version          : 10.0.19041
machine          : AMD64
processor        : Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
byteorder        : little
LC_ALL           : None
LANG             : None
LOCALE           : Russian_Russia.1251
pandas           : 1.2.1
numpy            : 1.20.0
pytz             : 2021.1
dateutil         : 2.8.1
pip              : 21.0.1
setuptools       : 49.6.0.post20210108
Cython           : None
pytest           : None
hypothesis       : None
sphinx           : None
blosc            : None
feather          : None
xlsxwriter       : None
lxml.etree       : 4.6.2
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
openpyxl         : 3.0.6
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
