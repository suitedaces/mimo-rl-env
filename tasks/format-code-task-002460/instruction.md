I’m building Cirq circuits programmatically and I need to rename measurement keys after the circuit already exists, but right now I’m having to walk the circuit and rebuild measurements by hand. It would be really nice if Cirq had a single way to take a circuit or operation and apply a measurement-key rename map, leaving everything else alone.

Expected outcomes:
- Public API: `cirq.with_measurement_key_mapping(val, key_map)` is available as the single entry point for applying a measurement-key rename map to supported Cirq values.
- Applying the API to supported Cirq values remaps matching measurement keys according to `key_map`, including keys contained inside existing circuit/operation structures.
- Measurement keys not present in the map are left unchanged, and non-measurement behavior is preserved.
- Existing object semantics such as qubit placement, tags, measurement metadata, and contained non-measurement operations are preserved while changing only the selected measurement keys.
- Applying the API to a value that does not support measurement-key remapping returns `NotImplemented`.

Implementation notes:
- The implementation may choose the internal protocol hook, traversal structure, dispatch strategy, and object-reconstruction details, as long as the public API behavior above is satisfied.
