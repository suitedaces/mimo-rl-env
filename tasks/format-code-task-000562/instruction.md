## Problem Statement

It feels kind of clunky that whenever I have a `MnemonicCode` or a `BIP32Path` I have to reach into `.words` or `.path` before I can do anything useful with it — like `mnemonic.words.mkString(" ")` or `path.path.foldLeft(...)`. Same story with `DeriveAddressesResult`, I just want to map/iterate over the addresses directly without going through `.addresses` every time. Could these wrapper types just behave like the sequence they're wrapping so I can call `.map`, `.mkString`, `.length`, indexing, etc. straight on them? Would save a lot of `.x.y` noise in calling code.

## Expected outcomes

- Sequence-backed wrapper values should support normal read-style Scala sequence operations directly on the wrapper, while preserving the same element order and values as their existing underlying sequence fields.
- `MnemonicCode` should be usable directly as a sequence of words: operations such as `mkString`, `length`, indexing, iteration, and mapping should behave the same as they do on `mnemonic.words`.
- `BIP32Path` should be usable directly as a sequence of `BIP32Node` values: operations such as `toList`, `foldLeft`, `length`, indexing, and iteration should behave the same as they do on `path.path`.
- `DeriveAddressesResult` should be usable directly as a sequence of `BitcoinAddress` values: operations such as `length`, indexing, iteration, and mapping should behave the same as they do on `result.addresses`.
- Existing construction, validation, serialization, and domain-specific behavior of the affected types should continue to work; this change is about reducing access boilerplate for sequence-like wrappers, not changing their underlying data.

## Implementation notes

- Prefer a reusable approach over one-off forwarding methods when several wrappers need the same sequence behavior, but the exact API shape, delegation strategy, data structures, and placement of shared code are up to the implementer.
- Do not require callers to use the old inner-field access pattern when a direct sequence operation on the wrapper is sufficient.
