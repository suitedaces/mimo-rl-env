read_csv cannot use dtype and true_values/false_values
Hi friends,

Not sure if this is working as intended, but it appears you cannot use both dtype and true_values or false_values kwargs when reading csv. 

```python
from io import StringIO
from csv import writer

import pandas as pd
import pytest


def test_pandas_read_write():
    df = pd.DataFrame({'A': ['yes', 'no'], 'B': ['yes', 'no']})
    out_io = StringIO(newline='')
    df.to_csv(out_io, index=False)

    out_io.seek(0)
    pd.read_csv(out_io)

    out_io.seek(0)
    kwargs = dict(dtype={'A': 'boolean', 'B': 'boolean'})

    with pytest.raises(ValueError):
        pd.read_csv(out_io, **kwargs)

    kwargs.update({'true_values': ['yes'], 'false_values': ['no']})
    out_io.seek(0)

    with pytest.raises(ValueError):
        pd.read_csv(out_io, **kwargs)

    out_io.seek(0)
    # pop dtype so true/false values work
    kwargs.pop('dtype')
    pd.read_csv(out_io, **kwargs)
```
Using converters kwarg to get the data how I like will fix my problem, but we may want to update the docs to let users know true/false user defined values will not work in conjugation with providing the boolean type.
