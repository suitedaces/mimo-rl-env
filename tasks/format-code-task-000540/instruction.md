## NoneType binary/comparison ops don't match CPython behavior

I've been running some Python snippets through Batavia and noticed a bunch of operations involving `None` behave differently from CPython 3.

### Comparisons

In CPython 3, ordering comparisons against `None` raise `TypeError`:

```python
>>> None < 1
TypeError: unorderable types: NoneType() < int()
>>> None <= 1
TypeError: ...
>>> None > 1
TypeError: ...
>>> None >= 1
TypeError: ...
```

In Batavia, these just return `False` silently, so code that's supposed to blow up keeps running and produces wrong results downstream. Only `==` / `!=` should work against `None` (and they do — that part's fine).

### Bitwise operators

```python
>>> None & 1
>>> None ^ 1
>>> None | 1
```

In CPython these raise `TypeError` ("unsupported operand type(s) for ...") like the other unsupported binary ops on `None`. In Batavia I get a `NotImplementedError` saying the dunder hasn't been implemented yet, which makes it look like Batavia is incomplete rather than the user's code being wrong.

### Subscripting

```python
>>> None[0]
```

CPython says `'NoneType' object is not subscriptable`. Batavia phrases this as if it were a binary operand mismatch ("unsupported operand type(s) for []: ..."), which doesn't match and is misleading — subscripting isn't a binary op.

### `pow` / `**`

```python
>>> None ** 2
```

CPython's message mentions both `**` and `pow()` in the unsupported-operand text. Batavia's message only mentions `pow`, so anyone using the `**` operator and grepping for it in the error won't find anything.

Could the `None` dunder methods be aligned with CPython here? The other binary ops on `None` (`+`, `-`, `*`, `/`, `//`, `%`, `<<`, `>>`) already raise `TypeError` with CPython-shaped messages, so this is just filling in the remaining cases consistently.
