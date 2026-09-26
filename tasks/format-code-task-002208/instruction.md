API: What is the rationale for numeric_only of Categorical reductions?
Consider an ordered Categorical with missing values:

```
In [32]: cat = pd.Categorical(['a', np.nan, 'b', 'a'], ordered=True)

In [33]: cat.min()
Out[33]: nan

In [34]: cat.max()
Out[34]: 'b'

In [35]: cat.min(numeric_only=True)
Out[35]: 'a'

In [36]: cat.max(numeric_only=True)
Out[36]: 'b'

In [37]: cat.min(numeric_only=False)
Out[37]: nan

In [38]: cat.max(numeric_only=False)
Out[38]: 'b'
```

So from the observation above (and from the code: https://github.com/pandas-dev/pandas/blob/a89e19d59e0bff2d02e4647af1904e2c9701dd5f/pandas/core/arrays/categorical.py#L2199), it seems that `numeric_only` means that only the actual categories should be considered, and not the missing values (so codes that are not -1).

This struck me as strange, for the following reasons:

* The fact that -1 is used as the code for missing data is rather an implementation detail, but now actually determines min/max behaviour (missing value is always the minimum, but never the maximum, unless there are only missing values)

* This behaviour is different than the default for other data types in pandas, which is skipping missing values by default:

    ```
    In [1]: s = pd.Series([1, np.nan, 2, 1])  

    In [2]: s.min()
    Out[2]: 1.0

    In [3]: s.astype(pd.CategoricalDtype(ordered=True)).min()
    Out[3]: nan

    In [5]: s.min(skipna=False)
    Out[5]: nan
    ```

* The keyword in pandas to determine whether NaNs should be skipped or not for reductions is `skipna=True/False`, not `numeric_only` (this also means the `skipna` keyword for categorical series is broken / has no effect). 
  Apart from that, the name "numeric_only" is also strange to me to mean this (and is also not documented).

* The `numeric_only` keyword in reductions methods of DataFrame actually means something entirely different: should full columns be excluded from the result based on their dtype. 
  
    ```
    In [63]: cat = pd.Categorical(['a', np.nan, 'b', 'a'], ordered=True)

    In [64]: pd.Series(cat).min(numeric_only=True)
    Out[64]: 'a'

    In [65]: pd.DataFrame({'cat': cat}).min(numeric_only=True)
    Out[65]: Series([], dtype: float64)
    ```

From the above list, I don't see a good reason for having `numeric_only=False` as 1) the default behaviour and 2) altogether as an option (instead of skipna). But it seems this was implemented rather from the beginning that Categoricals were introduced.

*Am I missing something?* 
*Is there a reason we don't skip NaNs by default for Categorical?* 

Would it be an idea to deprecate `numeric_only` in favor of `skipna` and deprecate the default?

cc @jreback @jankatins
