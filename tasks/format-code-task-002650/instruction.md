I'm using h5web against Jupyter and HSDS files, and some datasets with odd/custom datatypes make the viewer fail to load the tree or metadata with errors like `Unknown dtype ...` / `Unknown type {...}`. In those cases I can't even inspect the dataset/datatype entry or see the original type value that came back from the provider.

Expected outcomes:
- Unknown or unsupported datatype information from Jupyter-backed datasets should not prevent the corresponding dataset entity from being returned.
- Unknown or unsupported datatype objects from HSDS-backed datasets or committed datatypes should not prevent the corresponding entity from being returned.
- Unsupported datatypes should be represented as a structured HDF5 type whose class is `HDF5TypeClass.Unknown`, with the serialized class value `H5T_UNKNOWN`.
- Returned `Dataset` and `Datatype` entities should expose the provider’s original type payload through the optional public `rawType` field when that payload is available.
- Metadata/type rendering should be able to display unsupported structured HDF5 types as an unknown type rather than surfacing the provider’s raw type string/object or failing during conversion.

Implementation notes:
- The exact validation points, conversion helpers, and internal data flow are up to the implementation.
- Preserve existing behavior for recognized Jupyter and HSDS datatypes.
- Keep the public provider entity shape compatible with existing callers while adding the optional raw type information described above.
