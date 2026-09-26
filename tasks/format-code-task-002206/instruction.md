BUG: DataFrame.merge(suffixes=) does not respect None
```python-traceback
>>> import pandas as pd
>>> print(pd.__version__)
0.24.0rc1+6.gabfe72d7c.dirty
>>> from pandas import DataFrame
>>> df = DataFrame([1])
>>> df
   0
0  1
>>>
>>> df.columns
RangeIndex(start=0, stop=1, step=1)
>>>
>>> result = df.merge(df, left_index=True, right_index=True, suffixes=(None,'_dup'))
>>> result
   0None  0_dup
0      1      1
>>>
>>> result.columns
Index(['0None', '0_dup'], dtype='object')
>>>
>>> expected = result.rename(columns = {'0None':0})
>>> expected
   0  0_dup
0  1      1
>>>
>>> expected.columns
Index([0, '0_dup'], dtype='object')
```
specifying an empty string changes the dtype of the column label

```python-traceback
>>> result = df.merge(df, left_index=True, right_index=True, suffixes=('','_dup'))
>>> result
   0  0_dup
0  1      1
>>> result.columns
Index(['0', '0_dup'], dtype='object')

```
