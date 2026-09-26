Regression in 0.740 for __init__subclass__
The following code does not throw errors in 0.730, but does in 0.740. Likely to do with #7723 

``` python 
class A:
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)


class B(A):
    pass

# error: Too few arguments for "__init_subclass__"
```

And slightly more complicated, a self registering subclass:

```python
from typing import ClassVar, List, Type


class A:
    registered_classes: ClassVar[List[Type["A"]]] = []

    def __init_subclass__(cls, *args, register=True, **kwargs):
        if register:
            cls.registered_classes.append(cls)
        super().__init_subclass__(*args, **kwargs)


class B(A):
    pass


class C(A, register=False):
    pass


class D(C):
    pass


print(A.registered_classes) # >>> [<class '__main__.B'>, <class '__main__.D'>]

# 13: error: Too few arguments for "__init_subclass__"
# 17: error: Missing positional argument "cls" in call to "__init_subclass__"
# 21: error: Too few arguments for "__init_subclass__"
```
