```
>>> a = Const(1) - Const(2)                                                                                                                                                                     
>>> a.shape()
unsigned(3)
```

The correct result here (`-1`) is obviously not representable in an unsigned shape.
