S.pluck documentation is incorrect
The documentation for [`pluck`](https://github.com/sanctuary-js/sanctuary/blob/0853d0a592233fd602e8167760e33812d1870fa8/index.js#L3044-L3045) states that it is equivalent to `map(prop(k), xs)`. This is only the case if `xs` is an `Array`.

Either the documentation should be changed, or `pluck` should be updated to handle Functors in general (matching [`R.pluck`](http://ramdajs.com/docs/#pluck)'s behavior).

Incidentally, `R.pluck` works for Arrays and indices as well as Objects and keys (for obvious reasons).
