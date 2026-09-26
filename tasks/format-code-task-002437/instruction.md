Infer Literal type for + on literal
Currently this fails:

```python
from typing import Literal

x: Literal[1] = +1
```

`main.py:3: error: Incompatible types in assignment (expression has type "int", variable has type "Literal[1]")  [assignment]`

https://mypy-play.net/?mypy=latest&python=3.10&gist=ca355823e5fdc571fb3efa9c4f0bb764

Pyright allows it; mypy probably should too.

This is similar to python/typing#1550, but technically independent as the proposed spec change is about what goes inside `Literal[]`, and this issue is about contexts where mypy should infer literal types, which is not specified precisely.
