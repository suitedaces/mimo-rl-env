## `parse_module` chokes on f-strings containing a generator expression

I'm using LibCST to walk through a bunch of existing Python source files (building a small refactoring tool). On one of the files the parse just blows up, but the file itself is valid Python — `python -c` runs it fine and `ast.parse` is happy with it.

I narrowed it down to f-strings that contain a generator expression inside the `{...}` part. Minimal repro:

```python
import libcst as cst

source = 'x = f"{sum(i for i in range(10))}"'
cst.parse_module(source)
```

The same string parses fine with the stdlib:

```python
import ast
ast.parse('x = f"{sum(i for i in range(10))}"')   # OK
compile('x = f"{sum(i for i in range(10))}"', "<s>", "exec")  # OK
```

A bare generator expression wrapped in its own parens inside the f-string hits the same problem:

```python
cst.parse_module('x = f"{(i*2 for i in range(3))}"')
```

Both of these are accepted by CPython itself, so I'd expect LibCST to handle them too. Right now anything with a `for ... in ...` clause inside an f-string expression slot seems to be rejected at parse time, which means I can't run my tool over files that happen to use this pattern.

Could the f-string expression parser be updated to accept the same expression forms that CPython does here?
