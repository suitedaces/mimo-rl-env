Attributes can be deleted from frozen models
### Initial Checks

- [X] I confirm that I'm using Pydantic V2

### Description

While `BaseModel.__setattr__` checks `self.model_config.get('frozen', None)`, `__delattr__` doesn't. I haven't actually run into this in practice, it was just something I noticed while poking around, but it seems like a simple omission that users wouldn't expect.

I also note that https://docs.pydantic.dev/latest/concepts/models/#faux-immutability says:

> Immutability in Python is never strict. If developers are determined/stupid they can always modify a so-called "immutable" object.

but this seems like an easy mistake to make without being determined/stupid. This also means that hashing can break in a confusing way as demonstrated in the example code, which isn't the case in the example in the docs where there's a mutable non-hashable field.

### Example Code

```Python
from pydantic import BaseModel


class M(BaseModel, frozen=True):
    a: int


m = M(a=1)
s = {m}
print(m in s)  # True

del m.a  # should probably raise an error
print(m in s)  # False
s = {m}
print(m in s)  # True
```


### Python, Pydantic & OS Version

```Text
pydantic version: 2.4.2
        pydantic-core version: 2.10.1
          pydantic-core build: profile=release pgo=true
                 install path: /home/alex/work/pydantic/pydantic
               python version: 3.11.5 (main, Sep  9 2023, 21:35:25) [GCC 7.5.0]
                     platform: Linux-5.15.0-86-generic-x86_64-with-glibc2.35
             related packages: typing_extensions-4.7.1 email-validator-2.0.0.post2 pyright-1.1.330.post0 mypy-1.1.1 pydantic-extra-types-2.1.0 pydantic-settings-2.0.3
```
