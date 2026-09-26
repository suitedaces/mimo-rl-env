## Problem Statement

Right now circuit strings only seem to take single-letter element names like R, C, L — but I want to define my own custom elements with longer names (like "RR") and use them in a circuit, and at the moment it just doesn't parse them right. Could the parser be made to handle multi-letter element names? Also it'd be great if it correctly read multi-digit parameter indices too, since right now anything past single digits seems to break. Ideally custom element names would be restricted to plain uppercase letters so there's a clear rule about what counts as a valid name.

## Expected outcomes

- Multi-letter uppercase element names are supported by the public circuit-building APIs: a user-defined element such as `RR` can be made available and then used in a circuit string without being misparsed as separate one-letter elements.
- Circuit parsing correctly preserves element names and numeric suffixes when extracting elements from circuit strings, including suffixes with more than one digit.
- Element names are valid only when they consist of uppercase letters; names containing lowercase letters or digits in the name portion are rejected by validation or parsing.
- The `RR` element is available and behaves like a resistor scaled by a factor of 100, so an `RR` circuit can produce the same impedance as an equivalent resistor circuit when its parameter is adjusted accordingly.

## Implementation notes

- The internal representation, lookup strategy, parsing approach, and validation location are up to the implementer.
- Preserve existing behavior for existing single-letter elements and circuit syntax while extending support for the new naming and indexing cases.
- Error types and messages may follow the repository’s existing conventions, as long as invalid names are rejected rather than silently accepted or misparsed.
