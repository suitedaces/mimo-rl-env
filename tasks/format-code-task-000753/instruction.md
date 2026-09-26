# Fuse linear chains of tasks in a dask graph

A dask graph is a plain dictionary that maps keys to *tasks*. A task is a tuple whose first
element is a callable and whose remaining elements are arguments; an argument may itself be a
key (referring to another entry in the graph), a literal value, a nested task, or a (possibly
nested) list of any of these. For example:

```python
{'a': 1,
 'b': 2,
 'z': (add, 'a', 'b'),
 'y': (inc, 'z'),
 'x': (inc, 'y'),
 'w': (inc, 'x')}
```

As an optimization, long *linear* chains of tasks waste scheduler overhead: each intermediate
key has to be stored and looked up even though it is used exactly once. I'd like two public
helpers added to the core graph module.

## `subs(task, key, val)`

Return a copy of `task` in which every occurrence of `key` has been replaced by `val`. The
substitution must reach into nested tasks and into (arbitrarily nested) lists, while leaving the
callable in the leading position of a task untouched. A `task` that is itself exactly `key`
returns `val`; anything that neither matches `key` nor contains it is returned unchanged. For
example:

```python
subs((inc, 'x'), 'x', 1)            == (inc, 1)
subs((sum, [1, 'x']), 'x', 2)       == (sum, [1, 2])
subs((sum, [1, ['x']]), 'x', 2)     == (sum, [1, [2]])
```

## `fuse(dsk)`

Return a **new** graph (the input must not be mutated) that computes exactly the same results as
`dsk` but with linear chains of tasks collapsed into single tasks.

Collapsing works by inlining: a key `b` is substituted directly into the body of another key `a`
(replacing the reference to `b` with `b`'s value) and then dropped as a separate entry. Inline
`b` into `a` **if and only if**:

- `a` is the *only* entry in the graph whose task refers to `b`, and
- `a` refers to exactly one key in total — that single reference being `b`.

The second condition counts references with multiplicity: a task that mentions the same key twice
(e.g. `(add, 'b', 'b')`) refers to two keys and therefore never has anything fused into it, and a
key that is referenced twice from one place is likewise not inlined — inlining there would
duplicate work.

Apply this rule transitively, so a maximal linear chain `w -> x -> y -> z` collapses entirely into
its topmost task `w`, whose value becomes the fully nested expression. Keys that are not inlined
keep their original key name; keys that are inlined disappear from the result. A key holding a
plain value (not a task) is inlined under the same rule. A graph with no fusable chain comes back
equal to the input.

For example:

```python
fuse({'a': 1, 'b': 2,
      'z': (add, 'a', 'b'),
      'y': (inc, 'z'),
      'x': (inc, 'y'),
      'w': (inc, 'x')})
==
{'a': 1, 'b': 2,
 'w': (inc, (inc, (inc, (add, 'a', 'b'))))}
```
