I'm using `schemaspec.Resource.As` to decode into a struct that has an interface field and a `[]MyInterface` field. The child blocks are registered extension types that implement that interface, but after `As` runs those fields are still nil/empty and the same blocks are still sitting in the remainder. I thought my registration might be wrong, but decoding the concrete extension types directly works.

Expected outcomes:
- Interface slice fields: when `(*Resource).As(target interface{}) error` decodes a struct containing a field of type `[]MyInterface`, registered child extension blocks whose concrete types implement `MyInterface` should be decoded into their concrete values and appended to that slice.
- Interface slice fields: child blocks successfully decoded into a matching interface slice field should be treated as consumed and should not remain in the decoded resource remainder/extras.
- Single interface fields: when `(*Resource).As(target interface{}) error` decodes a struct containing a field of type `MyInterface`, and exactly one registered child extension block implements that interface, the field should be set to the decoded concrete extension value.
- Ambiguous single interface fields: when a single interface field could be filled by more than one matching registered child block, `(*Resource).As(target interface{}) error` should return an error using the format `more than one blocks implement %q`.

Implementation notes:
- The concrete mechanism for discovering registered extension types, selecting matching child blocks, and consuming decoded blocks is up to the implementation.
- Preserve existing decoding behavior for concrete extension fields, resource fields, attributes, and non-matching remainder content.
- Matching should be based on externally observable registration and Go interface assignability semantics, not on hard-coded block names used by a particular test.
