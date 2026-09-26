# Make `tuple` support the standard operators

Right now Python tuples that get transpiled to the JVM can be created, indexed,
sliced and iterated, but almost every operator on them is dead — using one
currently blows up with a "not implemented" error instead of behaving like
CPython. Please make tuples support the usual operator protocol so that
transpiled code behaves exactly the way it does under CPython 3.5.

Concretely, a tuple should support:

* **Rich comparisons** (`<`, `<=`, `>`, `>=`, `==`, `!=`) against another
  tuple, using Python's lexicographic ordering: compare element by element, and
  at the first position where the two tuples differ the result is decided by
  comparing those two elements; if one tuple is a prefix of the other, the
  shorter one is the smaller. Equality is element-wise and length-sensitive.
  * `==` and `!=` must also work when the other operand is **not** a tuple:
    a tuple is never equal to a non-tuple, so `==` is `False` and `!=` is
    `True` (no error).
  * The ordering comparisons (`<`, `<=`, `>`, `>=`) against a non-tuple operand
    must raise `TypeError`, matching CPython's message for unorderable types.

* **Concatenation** with `+`: `tuple + tuple` produces a new tuple with the
  elements of the left followed by the elements of the right. Adding anything
  that is not a tuple raises `TypeError` with CPython's message.

* **Repetition** with `*`: `tuple * n` for an integer `n` produces a new tuple
  with the elements repeated `n` times (`n` of zero or less yields an empty
  tuple); a boolean counts as `0`/`1`. Multiplying by something that is not an
  integer raises `TypeError` with CPython's message.

* **Truthiness**: an empty tuple is falsy and a non-empty tuple is truthy, so it
  behaves correctly in boolean contexts (`if`, `while`, `not ...`).

* **Unary operators**: `+`, `-` and `~` are not valid on tuples and must raise
  `TypeError` with CPython's message for a bad unary operand.

The observable contract is simply that each of these operations produces output
(including raised exceptions and their messages) identical to CPython 3.5 for
the same source. Existing tuple behaviour (creation, `repr`, indexing, slicing,
iteration) must keep working.
