Add option to ignore measurement keys when checking circuit equality
The following circuits are, for almost all purposes, equivalent, but are not considered equal by `mitiq.utils._equal` because they contain different measurement keys.

```python
import cirq

qbit = cirq.LineQubit(0)

circA = cirq.Circuit(cirq.ops.measure(qbit, key="a"))
print(circA)
# 0: ───M('a')───

circB = cirq.Circuit(cirq.ops.measure(qbit, key="b"))
print(circB)
# 0: ───M('b')───

print(cirq.CircuitDag.from_circuit(circA) == cirq.CircuitDag.from_circuit(circB))
# False
```

The change would be to update `mitiq.utils._equal` to account for this, for example by adding the argument `require_measurement_equality`.
