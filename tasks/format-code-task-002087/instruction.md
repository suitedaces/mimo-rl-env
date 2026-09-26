Trace.copy: Using deepcopy causes derived Stats keys setting parent keys with computed values (leading to wrong values in edge cases)
Hi everybody,

First, I hope all of you are happy and healthy.

Second, I've got a puzzling issue when working with highly-sampled data:

-  ObsPy version: 1.2.1 (anaconda)
-  Python version: 3.7
-  Arch Linux

Working with sampling rates >= 100000. Hz produces unexpected behavior.

```
tr = Trace(data=np.ones(100000), header={'sampling_rate': 100000.})
print(tr.stats.sampling_rate)
100000.0
print(tr.copy().stats.sampling_rate)
99999.99999999999
```
I think this is a result of floating point ["representation error"](https://docs.python.org/3/tutorial/floatingpoint.html), whenever the Trace AttribDict needs to be re-evaluated, [specifically where `delta` is involved](https://github.com/obspy/obspy/blob/88687a146a7c3ca8f35c608db2243cf5fed6813c/obspy/core/trace.py#L177-L182).

Not sure how to go about addressing this though...
