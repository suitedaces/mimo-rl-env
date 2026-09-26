## `qml.specs` reports `depth=None` for circuits with custom multi-layer operations

I've been defining my own operations by subclassing `ResourcesOperation` so I can plug them into PennyLane circuits while still being able to inspect resource counts. Some of these custom ops are themselves multi-layer constructs (a small ansatz or a decomposition I've worked out by hand), so their `resources()` returns a `Resources` object with `depth` greater than 1.

The problem is that as soon as I put one of these into a QNode and look at the specs, the overall circuit depth comes back as `None` instead of a number.

Minimal example:

```python
import pennylane as qml
from pennylane.resource import Resources, ResourcesOperation

class MyLayeredOp(ResourcesOperation):
    num_wires = 2
    def resources(self):
        # this op internally is e.g. 3 layers deep
        return Resources(num_wires=2, num_gates=4,
                         gate_types={"Hadamard": 2, "CNOT": 2},
                         gate_sizes={1: 2, 2: 2},
                         depth=3)

dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def circuit():
    qml.Hadamard(0)
    MyLayeredOp(wires=[0, 1])
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))

print(qml.specs(circuit)())
```

The `"depth"` entry in the specs dict is `None`. If I change `MyLayeredOp.resources()` to return `depth=1`, the specs dict reports a proper integer depth again, so the issue is specifically about custom ops whose self-reported depth is bigger than 1.

From a user's point of view this is pretty inconvenient — the whole reason I'm using `ResourcesOperation` and giving it a meaningful `depth` is so that tools like `qml.specs` can give me a faithful picture of the circuit's resource footprint. Falling back to `None` means I have to compute depth manually whenever any of my custom ops is more than one layer deep, which defeats the purpose.

Could `qml.specs` (and whichever underlying depth computation it relies on) be made to honor the `depth` declared by a custom `ResourcesOperation`, so that an integer circuit depth is returned even when the circuit contains custom ops with `depth > 1`?
