Specifying self-type for first `__init__` overload affects `isinstance` type narrowing
**Bug Report**

I have a [generic class with multiple `__init__` overloads](https://github.com/ni/nitypes-python/blob/01cd89bfa4f33e8ed88eae0fe495715059653b8f/src/nitypes/waveform/_spectrum.py#L278
). One of the `__init__` overloads specifies the type of `self` in order to control what the type variable evaluates to for this overload.

When I upgraded this code to Mypy 1.16, I started getting errors in a method that uses `isinstance` to check whether another object is an instance of the same class. I expected `if isinstance(other, A):` to narrow the type of `other` to `A[Any]`, but it actually narrows to the self-type specified in the first `__init__` overload, such as `A[int]`.

If I reorder the `__init__` overloads so the first overload does not specify a self-type, then `if isinstance(other, A):` seems to narrow to `A[Any]`, or `A[T]` in methods that take a union of `A[T]` and other types. This is the behavior I expected.

With Mypy 1.15 and older, the behavior is different. Specifying a self-type for the first `__init__` overload causes `if isinstance(other, A):` to narrow the type of `other` to `Never`. I think this is why I didn't get any errors before upgrading to Mypy 1.16.

Pyright doesn't complain about this code.

**To Reproduce**

Classes A and B are the same except for the order of the `__init__` overloads.

https://mypy-play.net/?mypy=latest&python=3.12&gist=dae546cdc2f11d2f5bd582efa826e188
```python
from typing import Generic, TypeVar, overload

T = TypeVar("T")

class A(Generic[T]):
    @overload
    def __init__(self, x: T) -> None: ...

    @overload
    def __init__(self: A[int]) -> None: ...

    def __init__(self, x: T | None = None) -> None:
        pass
    
    def f(self, other: A[T] | str) -> None:
        reveal_type(other) # Union[__main__.A[T`1], builtins.str]
        if isinstance(other, A):
            reveal_type(other) # __main__.A[T`1]
        else:
            raise TypeError

class B(Generic[T]):
    @overload
    def __init__(self: B[int]) -> None: ...

    @overload
    def __init__(self, x: T) -> None: ...

    def __init__(self, x: T | None = None) -> None:
        pass
    
    def f(self, other: B[T] | str) -> None:
        reveal_type(other) # Union[__main__.B[T`1], builtins.str]
        if isinstance(other, B):
            reveal_type(other) # __main__.B[builtins.int]
        else:
            raise TypeError
```

**Expected Behavior**

```
main.py:16: note: Revealed type is "Union[__main__.A[T`1], builtins.str]"
main.py:18: note: Revealed type is "__main__.A[T`1]"
main.py:33: note: Revealed type is "Union[__main__.B[T`1], builtins.str]"
main.py:35: note: Revealed type is "__main__.B[T`1]"
```

**Actual Behavior**

Mypy 1.16:
```
main.py:16: note: Revealed type is "Union[__main__.A[T`1], builtins.str]"
main.py:18: note: Revealed type is "__main__.A[T`1]"
main.py:33: note: Revealed type is "Union[__main__.B[T`1], builtins.str]"
main.py:35: note: Revealed type is "__main__.B[builtins.int]"
```

Mypy 1.15:
```
main.py:16: note: Revealed type is "Union[__main__.A[T`1], builtins.str]"
main.py:18: note: Revealed type is "__main__.A[T`1]"
main.py:33: note: Revealed type is "Union[__main__.B[T`1], builtins.str]"
main.py:35: note: Revealed type is "Never"
```

**Your Environment**

- Mypy version used: 1.16
- Mypy command-line flags: none
- Mypy configuration options from `mypy.ini` (and other config files): `strict=true`, but it's also reproducible with none
- Python version used: 3.12
