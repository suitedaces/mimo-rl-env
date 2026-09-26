Autofix(): Indexing error
The autofix function produces the following error: 
> IndexError: boolean index did not match indexed array along dimension 0; dimension is 138 but corresponding boolean dimension is 2

Code to reproduce the error: 
```python
def test_autofix():
    x = load_sample()
    s = bct.autofix(bct.binarize(bct.threshold_proportional(x, .41)))
    assert np.allclose(np.sum(s), 7752)
```

This is due to the following line: 
https://github.com/aestrivex/bctpy/blob/c8cfdeeca7d2437b93754ea3237f3e44b9c22957/bct/utils/other.py#L272

Proposed substituition:

```python
W[np.where(np.isinf(W))] = 0
W[np.where(np.isnan(W))] = 0
```
