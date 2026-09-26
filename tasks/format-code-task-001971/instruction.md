More informative exception message for `only`
Our team is thinking of replacing our use of some internal utility methods with `more-itertools`. Something we would miss, though, is that in some cases our methods give helpful debugging information. 

For example (as noted by my colleague @berquist ), compare [`get_only`](https://github.com/isi-vista/vistautils/blob/7eb87c06d3dc31d8c29f43d932ef6b834500c3f2/vistautils/collection_utils.py#L8) to [`only`](https://github.com/erikrose/more-itertools/blob/111d6deb8080040f8ec28db32eeb44b61238d860/more_itertools/more.py#L2523):

```
x = [1, 2, 3]
get_only(x)
ValueError("Expected one item in iterable but got multiple: [1, 2, 3]")
only(x)
ValueError("too many items in iterable (expected 1)")
```

The extra information provided by the former is often enough to determine the fix for a bug simply by reading the exception message.

The downside of `get_only`'s approach is that it can produce large error messages for collections with large, complex objects with bulky `__repr__`s. (collections with many elements are not a problem because we limit the number of elements we print).    In our case at least, the trade-off seems worthwhile.

Is adding a more informative message along these minds something that would be useful to `more_itertools`?  (another option: `only` currently takes an argument `too_long` which is `raise`d on error if specified.  We could allow making `too_long` a `Callable` which is called to generate the exception on failure).
