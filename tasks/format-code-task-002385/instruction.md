``nodes.Module`` don't have a ``end_lineno`` and ``end_col_offset``
### Steps to reproduce

```python
import astroid

code = """
    print("a module")
    """

module = astroid.parse(code)
print(module.end_lineno)
print(module.end_col_offset)
```

### Current behavior

`AttributeError` on both of the last lines.

### Expected behavior

@cdce8p Let me know if I misunderstood you, but I thought we wanted these to be accessible on all nodes, just initialised as `None`.
If that was not the case, I would make the case to do so as it allows you to do `node.end_lineno` without running in to `AttributeError`'s.

### Version

Latest `main`.
