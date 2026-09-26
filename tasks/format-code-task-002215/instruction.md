BUG: NBC change in reindexing logic of Series.__setitem__ in pandas=1.1.0
- [x] I have checked that this issue has not already been reported.

- [x] I have confirmed this bug exists on the latest version of pandas.

- [ ] (optional) I have confirmed this bug exists on the master branch of pandas.

Hi, 

The following example of using `Series.__setitem__` shows different results on **pandas=1.0.5** and **pandas=1.1.3**:

```
import pandas as pd
import numpy as np

S1 = pd.Series([0, 1, -12, 3, -10, 5, 6, 7, 8, -11, -13], dtype=np.int32)
idx = pd.Series([4, 9, 2, 10], dtype=np.int64)
value = pd.Series([-10, -11, -12, -13], dtype=np.int32)
S1[idx] = value  
S1
```

It looks like  [#33643](https://github.com/pandas-dev/pandas/pull/33643) changed the semantics of setitem operation when assigned values are `pandas.Series`, i.e. the old-behavior was to first align value with idx and then assign value items to S1 basing on idx.values as index labels, so result was:

```
>>> S1
0      0
1      1
2    -12
3      3
4    -10
5      5
6      6
7      7
8      8
9    -11
10   -13
dtype: int32
```

And now the result is as if `S1[idx]` took precedence before the actual assignment, so that labels in `idx.values` which are absent in `value.index` are assigned NaNs:

```
>>> S1
0      0.0
1      1.0
2    -12.0
3      3.0
4      NaN
5      5.0
6      6.0
7      7.0
8      8.0
9      NaN
10     NaN
dtype: float64
```

Can you please confirm this was intentional change (as I don't see any tests updated to reflect that, nor there are mentions in "What’s new in 1.1.0" section of the documentation)? From the user perspective it looks like with new implementation, user will have to ensure that `value.index == idx.values` to achieve the same result, which is not a big deal of course, but still it's some additional code. 

First version where the issue appears:
```
INSTALLED VERSIONS
------------------
commit           : 4071c3b872e4ef98a2a2d7c752dd5d2030c4df6e
python           : 3.7.7.final.0
python-bits      : 64
OS               : Windows
OS-release       : 10
Version          : 10.0.18362
machine          : AMD64
processor        : Intel64 Family 6 Model 142 Stepping 10, GenuineIntel
byteorder        : little
LC_ALL           : None
LANG             : None
LOCALE           : None.None

pandas           : 1.1.0.dev0+1307.g4071c3b87
```

Kind Regards,
Alexey.
