BUG: Inconsistent behavior: Occasional crash on same code and data
[x] I have checked that this issue has not already been reported.
[x]  I have confirmed this bug exists on the latest version of pandas.

**Description**
When reading csv with pd.read_csv, giving both names= and dtypes= arguments, the program occasionally crashes. Surprisingly, sometimes the application completes its execution cycle normally - without any change in code or data.

I had initially used only the _dtype_ argument, but the first row of my data would be considered as column headers (the csv, otherwise has no headers). Instead of using headers=None, I added _names_ argument, which on one hand made all my rows read as data while on the other set the desired column headers in DataFrame.

But after this change, the program's behavior has become inconsistent; occasional crashing while normal execution at other times.

### Reproducing Code Example
**Example Code and Data**
Minimal code along with a small data file, that demonstrate the reported behavior, is:
 
```python
import pandas as pd

df = pd.read_csv('data\\test3.csv', names={'pVal1', 'pClass'}, dtype={'pVal1':int, 'pClass':bool})
print (df)
```
The data file test3.csv contains:
```
1,TRUE
2,FALSE
3,TRUE
```

The problem goes away if we remove either of the two arguments (names, dtype). With any of the following statements, the program executes normally:
```
df = pd.read_csv('data\\test3.csv', names={'pVal1', 'pClass'})
```
or
```
df = pd.read_csv('data\\test3.csv', dtype={'pVal1':int, 'pClass':bool})
```

### Error message:
**Demonstration of Inconsistent Behaviour**

I am posting the result of two consecutive executions; first successful, the second failing with error:

**Successful Execution**
(ml) C:\Users\pyuser\projs\ml>py err.py
   pVal1  pClass
0      1    True
1      2   False
2      3    True

**Crash with Error**
(ml) C:\Users\pyuser\projs\ml>py err.py
Traceback (most recent call last):
  File "pandas\_libs\parsers.pyx", line 1152, in pandas._libs.parsers.TextReader
._convert_tokens
TypeError: Cannot cast array from dtype('int64') to dtype('bool') according to t
he rule 'safe'

During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "err.py", line 3, in <module>
    df = pd.read_csv('data\\test3.csv', names={'pVal1', 'pClass'}, dtype={'pVal1
':int, 'pClass':bool})
  File "C:\Users\pyuser\projs\ml\lib\site-packages\pandas\io\parsers.py", line 676
, in parser_f
    return _read(filepath_or_buffer, kwds)
  File "C:\Users\pyuser\projs\ml\lib\site-packages\pandas\io\parsers.py", line 454
, in _read
    data = parser.read(nrows)
  File "C:\Users\pyuser\projs\ml\lib\site-packages\pandas\io\parsers.py", line 113
3, in read
    ret = self._engine.read(nrows)
  File "C:\Users\pyuser\projs\ml\lib\site-packages\pandas\io\parsers.py", line 203
7, in read
    data = self._reader.read(nrows)
  File "pandas\_libs\parsers.pyx", line 860, in pandas._libs.parsers.TextReader.
read
  File "pandas\_libs\parsers.pyx", line 875, in pandas._libs.parsers.TextReader.
_read_low_memory
  File "pandas\_libs\parsers.pyx", line 952, in pandas._libs.parsers.TextReader.
_read_rows
  File "pandas\_libs\parsers.pyx", line 1084, in pandas._libs.parsers.TextReader
._convert_column_data
  File "pandas\_libs\parsers.pyx", line 1160, in pandas._libs.parsers.TextReader
._convert_tokens
ValueError: cannot safely convert passed user dtype of bool for int64 dtyped dat
a in column 0

**Software and Library Versions**
### Numpy/Python version information:
(ml) C:\Users\pyuser\projs\ml>python --version
Python 3.8.2

(ml) C:\Users\pyuser\projs\ml>python -c "import numpy; print(numpy.version.version
)"
1.18.4

(ml) C:\Users\pyuser\projs\ml>python -c "import pandas; print(pandas.__version__)"
1.0.5

<!-- Output from 'import sys, numpy; print(numpy.__version__, sys.version)' -->
1.18.4 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AM
D64)]
