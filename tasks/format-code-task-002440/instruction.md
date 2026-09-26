typeddict check for multiple inheritance fails with type aliases
<!--
If you're not sure whether what you're experiencing is a mypy bug, please see the "Question and Help" form instead.
Please consider:

- checking our common issues page: https://mypy.readthedocs.io/en/stable/common_issues.html
- searching our issue tracker: https://github.com/python/mypy/issues to see if it's already been reported
- asking on gitter chat: https://gitter.im/python/typing
-->

**Bug Report**

<!--
If you're reporting a problem with a specific library function, the typeshed tracker is better suited for this report: https://github.com/python/typeshed/issues

If the project you encountered the issue in is open source, please provide a link to the project.
-->

Mypy thinks a type alias isn't a typeddict.

**To Reproduce**

```python
from typing import TypedDict, Unpack

class A(TypedDict, total=False):
    y: int
class B(TypedDict, total=False):
    x: str

D = B

class C(A, D):  # E: All bases of a new TypedDict must be TypedDict types  
    pass
```

**Expected Behavior**

no errors

**Actual Behavior**

```
main.py:10: error: All bases of a new TypedDict must be TypedDict types  [misc]
Found 1 error in 1 file (checked 1 source file)
```

**Your Environment**

<!-- Include as many relevant details about the environment you experienced the bug in -->

Checked using mypy-play.
- Mypy version used: 1.15
- Mypy command-line flags: N/A
- Mypy configuration options from `mypy.ini` (and other config files): N/A
- Python version used: 3.12

<!-- You can freely edit this text, please remove all the lines you believe are unnecessary. -->
