<!-- 
Thank you for taking the time to file a bug report. 
Please fill in the fields below, deleting the sections that 
don't apply to your issue. You can view the final output
by clicking the preview button above.
Note: This is a comment, and won't appear in the output.
-->

I am having an issue for a specific usage of the count_neighbors method of a KDTree. With the new "weights" argument in 1.6.0, this error occurs when counting neighbors between two different arrays A and B, with their respective weight arrays in a tuple for the "weights" arg :

#### Reproducing code example:
<!-- 
If you place your code between the triple backticks below, 
it will be rendered as a code block. 
-->

```
r = np.arange(0.05, 1, 0.05)

A = np.random.random(21).reshape((7,3))
B = np.random.random(45).reshape((15,3))

wA = np.random.random(7)
wB = np.random.random(15)

kdA = KDTree(A)
kdB = KDTree(B)

nAB = kdA.count_neighbors(kdB, r, cumulative=False, weights=(wA,wB))
```

#### Error message:
<!-- If any, paste the *full* error message inside a code block
as above (starting from line Traceback)
-->

```
Process finished with exit code -1073741819 (0xC0000005)
```

There is no Traceback, simply this exit code when the last line is executed. I was initially working with very large arrays when it occured, so I thought it could be a memory issue, but the example above produces the same error. Note that there is no such error when using count_neighbors between the same two KDTrees, with the same weights, as shown here:

```
nAA = kdA.count_neighbors(kdA, r, cumulative=False, weights=(wA,wA))
```

#### Scipy/Numpy/Python version information:
<!-- You can simply run the following and paste the result in a code block
```
import sys, scipy, numpy; print(scipy.__version__, numpy.__version__, sys.version_info)
```
-->

```
1.6.0 1.20.0 sys.version_info(major=3, minor=8, micro=6, releaselevel='final', serial=0)
```

It is possible that I misinterpreted the documentation, and that weighting is only implemented for two identical arrays. If that is the case, it would be useful to be able to do it for different ones.

Thanks!
