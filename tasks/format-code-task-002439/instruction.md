mypy incorrectly marks a @staticmethod definition of an attribute A to be incompatible with A's signature in a parent class.
**Bug Report**
When a class **C** defines an attribute **a** to be a union type with `Callable` as one of its types (`a: Callable | ...`), **mypy** incorrectly marks a `@staticmethod` definition of **a** in a child class that inherits from **C** to be incompatible with **a**'s signature in **C**.

Worth noting that the following code produces no errors:
```python
from typing import Callable


class Parent:
    foo: Callable[[str], str]

class Child2(Parent):
    @staticmethod
    def foo(x: str) -> str:
        return x.lower()
```

but the following code does

```python
from typing import Callable


class Parent:
    foo: Callable[[str], str] | str 


class Child1(Parent):
    foo = "bar"  # OK


class Child2(Parent):
    @staticmethod
    def foo(x: str) -> str:  # Signature of "foo" incompatible with supertype "Parent"
        return x.lower()
```

**Expected Behavior**
No errors.



**Actual Behavior**
```shell
example.py: note: In class "Child2":
example.py:14: error: Signature of "foo" incompatible with supertype "Parent"  [override]
Found 1 error in 1 file (checked 1 source file)
```
**Environment**

<!-- Include as many relevant details about the environment you experienced the bug in -->

- Mypy version used: `0.941`
- Mypy command-line flags: `--strict`, `--show-error-codes`,  `--show-error-context`
- Mypy configuration options from `mypy.ini` (and other config files):
- Python version used: `3.10.3`
- Operating system and version: MacOS 12.3
