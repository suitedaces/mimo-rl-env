`Variable.__repr__` raises error when underlying data is not initialized
In v2, the following code raises an error.

```
In [1]: import chainer
In [2]: a = chainer.Variable()
In [4]: a.data is None
Out[4]: True
In [5]: repr(a)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-5-f35fccf361ee> in <module>()
----> 1 repr(a)

/Users/oonokenta/dev/chainer/chainer/variable.py in __repr__(self)
    305 
    306     def __repr__(self):
--> 307         return variable_repr(self)
    308 
    309     def __str__(self):

/Users/oonokenta/dev/chainer/chainer/variable.py in variable_repr(var)
     75         prefix = 'variable'
     76 
---> 77     if arr.size > 0 or arr.shape == (0,):
     78         lst = numpy.array2string(arr, None, None, None, ', ', prefix + '(')
     79     else:  # show zero-length shape unless it is (0,)

AttributeError: 'NoneType' object has no attribute 'size'
```

It is because `variable_repr(var)` assumes that  `var.data` is not `None`.
