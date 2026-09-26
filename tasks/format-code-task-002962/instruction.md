## Problem Statement

I’m loading a WSDL that has a complex type referencing itself, and after `soap.createClient(...)` finishes, calling `client.describe()` blows up with a maximum call stack size exceeded error.

## Expected outcomes

- WSDLs whose non-primitive complex types directly or indirectly reference themselves can still be loaded with `soap.createClient(...)`.
- After such a client is created, calling `client.describe()` returns a description object instead of throwing a stack-overflow-style recursion error.
- The returned description preserves the recursive fields in a finite public description object, rather than endlessly nesting the same type.
- Existing behavior for non-recursive WSDL descriptions should remain compatible with the current public `client.describe()` output shape.

## Implementation notes

No particular internal representation is required for recursive WSDL descriptions, as long as the public `soap.createClient(...)` and `client.describe()` behavior above is satisfied.
