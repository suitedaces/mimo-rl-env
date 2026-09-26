Failing test case using pyupgrade 2.25.0:

```
$ echo 'a=b=c=None; print("Query:%8s %s %s" % (a, b, c))'  > test.py ; pyupgrade --py36-plus test.py ; cat test.py
Rewriting test.py
a=b=c=None; print(f"Query:{a:>8} {b} {c}")
```

```pycon
>>> a=b=c=None; print("Query:%8s %s %s" % (a, b, c))
Query:    None None None
>>> a=b=c=None; print(f"Query:{a:>8} {b} {c}")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported format string passed to NoneType.__format__
```

The problem is while ``f"{None}"`` works, advanced string format arguments do not:

```pycon
>>> "%8s" % None
'    None'
```

```pycon
>>> f"{None:>8}"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported format string passed to NoneType.__format__
```

Possible workaround:

```python
>>> a=b=c=None; print(f"Query:{str(a):>8} {b} {c}")
Query:    None None None
```

This issue was found in https://github.com/biopython/biopython/pull/3724
