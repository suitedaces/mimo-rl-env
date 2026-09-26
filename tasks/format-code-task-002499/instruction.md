incorrect substitution of generic parameters
MRE:
```py
import dishka as d
import typing as t

A = t.TypeVar("A")
B = t.TypeVar("B")

class C(t.Generic[A, B]):
 pass

def func(b: type[B]) -> C[int, B]:
 print(b)

provider = d.Provider(scope=d.Scope.APP)
provider.provide(func)
c = d.make_container(provider)
c.get(C[int, bool])
```

Expected output: `<class 'bool'>`
Real output: `<class 'int'>`
Dishka version: 1.4.2
