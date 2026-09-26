BUG: series.__getitem__(invalid_string) raises UFuncTypeError instead of KeyError
### Modin version checks

- [X] I have checked that this issue has not already been reported.

- [X] I have confirmed this bug exists on the latest released version of Modin.

- [X] I have confirmed this bug exists on the main branch of Modin. (In order to do this you can follow [this guide](https://modin.readthedocs.io/en/stable/getting_started/installation.html#installing-from-the-github-master-branch).)


### Reproducible Example

```python
import modin.pandas as pd

s = pd.Series([1])
print(s['a'])
```


### Issue Description

Modin raises an error from a long stack trace ending with `UFuncTypeError: ufunc 'less' did not contain a loop with signature matching types (<class 'numpy.dtype[str_]'>, <class 'numpy.dtype[int64]'>) -> <class 'numpy.dtype[bool_]'>` . pandas raises a shorter error ending with `KeyError: 'a'`.

### Expected Behavior

Modin error should match pandas error.

### Error Logs

<details>

<summary>Modin stack trace</summary>

```python-traceback

UserWarning: Distributing <class 'list'> object. This may take some time.
---------------------------------------------------------------------------
UFuncTypeError                            Traceback (most recent call last)
File ~/software_sources/modin/modin/pandas/series.py:2453, in Series._getitem(self, key)
   2452     else:
-> 2453         result = self._query_compiler.getitem_row_array(key)
   2454 except TypeError:

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()

File ~/software_sources/modin/modin/core/storage_formats/pandas/query_compiler.py:2233, in PandasQueryCompiler.getitem_row_array(self, key)
   2231 def getitem_row_array(self, key):
   2232     return self.__constructor__(
-> 2233         self._modin_frame.take_2d_labels_or_positional(row_positions=key)
   2234     )

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:124, in lazy_metadata_decorator.<locals>.decorator.<locals>.run_f_on_minimally_updated_metadata(self, *args, **kwargs)
    123         obj._propagate_index_objs(axis=0)
--> 124 result = f(self, *args, **kwargs)
    125 if apply_axis is None and not transpose:

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:676, in PandasDataframe.take_2d_labels_or_positional(self, row_labels, row_positions, col_labels, col_positions)
    674     col_positions = self.columns.get_indexer_for(col_labels)
--> 676 return self._take_2d_positional(row_positions, col_positions)

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:813, in PandasDataframe._take_2d_positional(self, row_positions, col_positions)
    812 # Get dict of row_parts as {row_index: row_internal_indices}
--> 813 row_partitions_dict = self._get_dict_of_block_index(
    814     0, sorted_row_positions, are_indices_sorted=True
    815 )
    816 new_row_lengths = self._get_new_lengths(row_partitions_dict, axis=0)

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:1354, in PandasDataframe._get_dict_of_block_index(self, axis, indices, are_indices_sorted)
   1353     return OrderedDict([(0, np.array([], dtype=np.int64))])
-> 1354 negative_mask = np.less(indices, 0)
   1355 has_negative = np.any(negative_mask)

UFuncTypeError: ufunc 'less' did not contain a loop with signature matching types (<class 'numpy.dtype[str_]'>, <class 'numpy.dtype[int64]'>) -> <class 'numpy.dtype[bool_]'>

During handling of the above exception, another exception occurred:

UFuncTypeError                            Traceback (most recent call last)
Input In [30], in <cell line: 4>()
      1 import modin.pandas as pd
      3 s = pd.Series([1])
----> 4 print(s['a'])

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    113 """
    114 Compute function with logging if Modin logging is enabled.
    115
   (...)
    125 Any
    126 """
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()
    131 logger_level = getattr(logger, log_level)

File ~/software_sources/modin/modin/pandas/base.py:3190, in BasePandasDataset.__getitem__(self, key)
   3188     return self._getitem_slice(indexer)
   3189 else:
-> 3190     return self._getitem(key)

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    113 """
    114 Compute function with logging if Modin logging is enabled.
    115
   (...)
    125 Any
    126 """
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()
    131 logger_level = getattr(logger, log_level)

File ~/software_sources/modin/modin/pandas/series.py:2455, in Series._getitem(self, key)
   2453             result = self._query_compiler.getitem_row_array(key)
   2454     except TypeError:
-> 2455         result = self._query_compiler.getitem_row_array(key)
   2456 if reduce_dimension:
   2457     return self._reduce_dimension(result)

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    113 """
    114 Compute function with logging if Modin logging is enabled.
    115
   (...)
    125 Any
    126 """
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()
    131 logger_level = getattr(logger, log_level)

File ~/software_sources/modin/modin/core/storage_formats/pandas/query_compiler.py:2233, in PandasQueryCompiler.getitem_row_array(self, key)
   2231 def getitem_row_array(self, key):
   2232     return self.__constructor__(
-> 2233         self._modin_frame.take_2d_labels_or_positional(row_positions=key)
   2234     )

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    113 """
    114 Compute function with logging if Modin logging is enabled.
    115
   (...)
    125 Any
    126 """
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()
    131 logger_level = getattr(logger, log_level)

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:124, in lazy_metadata_decorator.<locals>.decorator.<locals>.run_f_on_minimally_updated_metadata(self, *args, **kwargs)
    122     elif apply_axis == "rows":
    123         obj._propagate_index_objs(axis=0)
--> 124 result = f(self, *args, **kwargs)
    125 if apply_axis is None and not transpose:
    126     result._deferred_index = self._deferred_index

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:676, in PandasDataframe.take_2d_labels_or_positional(self, row_labels, row_positions, col_labels, col_positions)
    672 if col_labels is not None:
    673     # Get numpy array of positions of values from `col_labels`
    674     col_positions = self.columns.get_indexer_for(col_labels)
--> 676 return self._take_2d_positional(row_positions, col_positions)

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    113 """
    114 Compute function with logging if Modin logging is enabled.
    115
   (...)
    125 Any
    126 """
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()
    131 logger_level = getattr(logger, log_level)

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:813, in PandasDataframe._take_2d_positional(self, row_positions, col_positions)
    811 sorted_row_positions = self._get_sorted_positions(row_positions)
    812 # Get dict of row_parts as {row_index: row_internal_indices}
--> 813 row_partitions_dict = self._get_dict_of_block_index(
    814     0, sorted_row_positions, are_indices_sorted=True
    815 )
    816 new_row_lengths = self._get_new_lengths(row_partitions_dict, axis=0)
    817 new_index, _ = self._get_new_index_obj(
    818     row_positions, sorted_row_positions, axis=0
    819 )

File ~/software_sources/modin/modin/logging/logger_decorator.py:128, in enable_logging.<locals>.decorator.<locals>.run_and_log(*args, **kwargs)
    113 """
    114 Compute function with logging if Modin logging is enabled.
    115
   (...)
    125 Any
    126 """
    127 if LogMode.get() == "disable":
--> 128     return obj(*args, **kwargs)
    130 logger = get_logger()
    131 logger_level = getattr(logger, log_level)

File ~/software_sources/modin/modin/core/dataframe/pandas/dataframe/dataframe.py:1354, in PandasDataframe._get_dict_of_block_index(self, axis, indices, are_indices_sorted)
   1349 if isinstance(indices, np.ndarray) and indices.size == 0:
   1350     # This will help preserve metadata stored in empty dataframes (indexes and dtypes)
   1351     # Otherwise, we will get an empty `new_partitions` array, from which it will
   1352     #  no longer be possible to obtain metadata
   1353     return OrderedDict([(0, np.array([], dtype=np.int64))])
-> 1354 negative_mask = np.less(indices, 0)
   1355 has_negative = np.any(negative_mask)
   1356 if has_negative:
   1357     # We're going to modify 'indices' inplace in a numpy way, so doing a copy/converting indices to numpy.

UFuncTypeError: ufunc 'less' did not contain a loop with signature matching types (<class 'numpy.dtype[str_]'>, <class 'numpy.dtype[int64]'>) -> <class 'numpy.dtype[bool_]'>

```

</details>


<details>

<summary>pandas stack trace</summary>

```python-traceback
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Input In [31], in <cell line: 4>()
      1 import pandas as pd
      3 s = pd.Series([1])
----> 4 print(s['a'])

File ~/opt/anaconda3/envs/modin-dev/lib/python3.10/site-packages/pandas/core/series.py:958, in Series.__getitem__(self, key)
    955     return self._values[key]
    957 elif key_is_scalar:
--> 958     return self._get_value(key)
    960 if is_hashable(key):
    961     # Otherwise index.get_value will raise InvalidIndexError
    962     try:
    963         # For labels that don't resolve as scalars like tuples and frozensets

File ~/opt/anaconda3/envs/modin-dev/lib/python3.10/site-packages/pandas/core/series.py:1069, in Series._get_value(self, label, takeable)
   1066     return self._values[label]
   1068 # Similar to Index.get_value, but we do not fall back to positional
-> 1069 loc = self.index.get_loc(label)
   1070 return self.index._get_values_for_loc(self, loc, label)

File ~/opt/anaconda3/envs/modin-dev/lib/python3.10/site-packages/pandas/core/indexes/range.py:389, in RangeIndex.get_loc(self, key, method, tolerance)
    387             raise KeyError(key) from err
    388     self._check_indexing_error(key)
--> 389     raise KeyError(key)
    390 return super().get_loc(key, method=method, tolerance=tolerance)

KeyError: 'a'
```

</details>

### Installed Versions

<details>

INSTALLED VERSIONS
------------------
commit           : 027f92a7655ae5b473839b7956ff52bf7879f3cc
python           : 3.10.4.final.0
python-bits      : 64
OS               : Darwin
OS-release       : 21.5.0
Version          : Darwin Kernel Version 21.5.0: Tue Apr 26 21:08:22 PDT 2022; root:xnu-8020.121.3~4/RELEASE_X86_64
machine          : x86_64
processor        : i386
byteorder        : little
LC_ALL           : None
LANG             : en_US.UTF-8
LOCALE           : en_US.UTF-8

Modin dependencies
------------------
modin            : 0.15.0+153.g027f92a7
ray              : 2.0.0
dask             : 2022.7.1
distributed      : 2022.7.1
hdk              : None

pandas dependencies
-------------------
pandas           : 1.4.4
numpy            : 1.23.2
pytz             : 2022.2.1
dateutil         : 2.8.2
setuptools       : 61.2.0
pip              : 22.2.2
Cython           : None
pytest           : 7.1.2
hypothesis       : None
sphinx           : 4.5.0
blosc            : None
feather          : 0.4.1
xlsxwriter       : None
lxml.etree       : 4.9.1
html5lib         : None
pymysql          : None
psycopg2         : 2.9.3
jinja2           : 3.1.2
IPython          : 8.4.0
pandas_datareader: None
bs4              : 4.11.1
bottleneck       : None
brotli           : 1.0.9
fastparquet      : 0.8.1
fsspec           : 2022.7.1
gcsfs            : None
markupsafe       : 2.1.1
matplotlib       : 3.5.2
numba            : None
numexpr          : 2.8.3
odfpy            : None
openpyxl         : 3.0.10
pandas_gbq       : 0.17.7
pyarrow          : 8.0.0
pyreadstat       : None
pyxlsb           : None
s3fs             : 2022.7.1
scipy            : 1.9.0
snappy           : None
sqlalchemy       : 1.4.39
tables           : 3.7.0
tabulate         : None
xarray           : 2022.6.0
xlrd             : 2.0.1
xlwt             : None
zstandard        : None


</details>
