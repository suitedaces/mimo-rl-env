False positive: Name mangling + `@dataclass` (undefined_attribute)
This is a very specific issue. So maybe it is not needed to be fixed as I doubt somebody will ever go through this situation. Minimum reproducible example:

```python
from dataclasses import dataclass

@dataclass
class A:
    def __func(self) -> None:
        ...

    def run(self) -> None:
        self.__func()  # ERROR: Undefined attribute
```

This issue only happens with `@dataclass`. If the decorator is removed, it will work fine.
