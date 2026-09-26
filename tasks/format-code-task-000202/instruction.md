Support adding observable to scalar `0`?
### Feature details

It would be nice to be able to do the following:
```
H = sum([qml.PauliX(i) for i in range(10)])
```

The issue here is that `sum` naturally starts at integer 0 but there's no way to add observables to an integer 0. Philosophically it seems valid to use `0` as the zero element of dxd matrices (similar behavior is supported for numpy arrays, e.g.).

### Implementation

```
    def __add__(self, other):
        r"""The addition operation between Observables/Tensors/qml.Hamiltonian objects."""
        if isinstance(other, numbers.Number) and other == 0:
            return self
        if isinstance(other, qml.Hamiltonian):
            return other + self
        if isinstance(other, (Observable, Tensor)):
            return qml.Hamiltonian([1, 1], [self, other], simplify=True)
        raise ValueError(f"Cannot add Observable and {type(other)}")
```
I'm assuming anything that is a `Number` implements `__eq__`, might need to double check that though.

### How important would you say this feature is?

1: Not important. Would be nice to have.

### Additional information

Workarounds:
```
H = sum([qml.PauliX(i) for i in range(10)], start=0*qml.PauliX(0)) # meh
H = qml.PauliX(0)
for i in range(1, 10):
    H += qml.PauliX(i) # ugh
```

For reference, the corresponding operation works in cirq:
```
H = sum([cirq.X(j) for j in cirq.LineQubit.range(10)])
```
