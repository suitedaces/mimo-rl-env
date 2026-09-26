BUG: all-NaT TimedeltaArray division with object dtype array doesn't preserve dtype
```
In [27]: pd.array(["1 days", "2 days"], dtype="timedelta64[ns]") / np.array([2, 2])
Out[27]: 
<TimedeltaArray>
['0 days 12:00:00', '1 days 00:00:00']
Length: 2, dtype: timedelta64[ns]

In [28]: pd.array(["1 days", "2 days"], dtype="timedelta64[ns]") / np.array([2, 2], dtype=object)
Out[28]: 
<TimedeltaArray>
['0 days 12:00:00', '1 days 00:00:00']
Length: 2, dtype: timedelta64[ns]

In [29]: pd.array(["NaT", "NaT"], dtype="timedelta64[ns]") / np.array([2, 2])
Out[29]: 
<TimedeltaArray>
[NaT, NaT]
Length: 2, dtype: timedelta64[ns]

In [30]: pd.array(["NaT", "NaT"], dtype="timedelta64[ns]") / np.array([2, 2], dtype=object)
Out[30]: array([NaT, NaT], dtype=object)
```

The last case doesn't result in a TimedeltaArray as result.
