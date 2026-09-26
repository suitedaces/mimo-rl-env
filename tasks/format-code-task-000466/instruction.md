Rewriting TypedDict can lead to SyntaxError
pyupgrade checks if the keys of a TypedDict are strings, but not if they are valid for usage in class syntax.

Here's a minimal input:

```python
from typing_extensions import TypedDict

MyDict = TypedDict("MyDict", {"my-key": str, "another key": int})
```


This is the rewrite produced by `pyupgrade --py36-plus minimal.py`:

```python
from typing_extensions import TypedDict

class MyDict(TypedDict):
    my-key: str
    another key: int
```

The `-` and the space in the keys are invalid syntax.
