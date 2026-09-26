## `qml.matrix` on `qml.exp` fails when the base operator skips wires and the coefficient is trainable

I'm building a parameterized exponential of a multi-qubit Pauli string and trying to grab its matrix representation. As soon as the tensor product has a "gap" in the wires it acts on (e.g. wires 0, 1, 4 but nothing on 2 and 3), and the coefficient is a trainable autograd array, `qml.matrix` blows up.

Minimal reproducer:

```python
import pennylane as qml
from pennylane import numpy as np

op = qml.exp(
    qml.PauliZ(wires=0) @ qml.PauliY(wires=1) @ qml.PauliZ(wires=4),
    coeff=np.array(0.25),
)
qml.matrix(op)
```

This raises a `ValueError` from inside the `Exp.matrix` path complaining about a matmul shape mismatch (something about size 8 vs size 2). The same call works fine if I either:

- pass a plain Python float as the coefficient instead of `np.array(0.25)`, or
- use a Pauli string whose wires are contiguous (e.g. `PauliZ(0) @ PauliY(1) @ PauliZ(2)`).

So it only seems to break in the combination "trainable autograd coeff" + "wires of the base op are non-contiguous". I'd expect `qml.matrix(op)` to just return the matrix of the exponential on the wires the operator declares, regardless of whether those wires happen to be contiguous, and I'd like to keep the coefficient as a trainable autograd array so I can differentiate through it later.
