BUG: DataFrame.astype(dict) can cause column metadata to be lost
#### Code Sample, a copy-pastable example if possible

Setup:
```python
In [2]: df = pd.DataFrame(data=np.random.randint(5, size=(3, 4)),
   ...:                   columns=pd.UInt64Index(range(500, 504), name='foo'))
   ...:

In [3]: df
Out[3]:
foo  500  501  502  503
0      4    4    2    1
1      0    2    3    1
2      1    4    0    0

In [4]: df.columns
Out[4]: UInt64Index([500, 501, 502, 503], dtype='uint64', name='foo')
```

Using `.astype(dict)` loses column metadata:
```python
In [5]: df = df.astype({500: 'float64', 501: 'uint64'})

In [6]: df.columns
Out[6]: Int64Index([500, 501, 502, 503], dtype='int64')
```

#### Problem description

Column metadata is lost: the `name` has been removed and it has been cast from `UInt64Index` to `Int64Index`.

#### Expected Output

I'd expect the columns post-`astype` to be the same as pre-`astype`.
