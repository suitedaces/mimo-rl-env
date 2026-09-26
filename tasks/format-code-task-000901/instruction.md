# Add an OP-Stack `ProtocolVersion` type

We're introducing the concept of a Superchain "Protocol Version" — a Semver-compatible
identifier that lets nodes reason about which protocol features they support and signal
recommended/required upgrades to each other. As a first step we need a self-contained value
type for it in the shared eth types package (`op-service/eth`), exported as
`eth.ProtocolVersion`, so the rest of the stack can encode, compare, log and transport it.

## Encoding

A `ProtocolVersion` is a single fixed 32-byte value. The first byte is a `version-type`
discriminator (a `uint8`) and the remaining 31 bytes are the typed payload, so the format can be
extended in the future.

For `version-type` `0`, the 32 bytes are laid out as:

```
<version-type=0 (1 byte)><reserved (7 zero bytes)><build (8 bytes)><major (4)><minor (4)><patch (4)><pre-release (4)>
```

where `major`, `minor`, `patch` and `pre-release` are big-endian `uint32` values in that order,
and `build` is 8 raw bytes.

Provide a builder for version-type 0 values, `eth.ProtocolVersionV0`, with fields
`Build [8]byte` and `Major`, `Minor`, `Patch`, `PreRelease` (all `uint32`), and an `Encode()`
method that packs them into a `ProtocolVersion` with exactly the layout above. The 7 reserved
bytes must be zero.

## Human-readable form

`String()` renders a version-type 0 value as a Semver-style string:

- The base is `vMAJOR.MINOR.PATCH` using the decimal values (no zero-padding), e.g. `v1.2.3`.
- If `pre-release` is non-zero, append `-PRERELEASE`, e.g. `v1.2.3-4`. A zero pre-release is omitted.
- If the build field is not all zero, append a `+` build suffix:
  - If, after trimming trailing zero bytes, every remaining build byte is in the Semver build
    character set (`0-9`, `a-z`, `A-Z`, `-`, `.`), present it directly as that string,
    e.g. build bytes `"OPstack\x00"` render as `+OPstack`.
  - Otherwise present all 8 build bytes as a `0x`-prefixed lowercase hex string,
    e.g. `+0xff00010203040506`.
  - An all-zero build adds no suffix.

## Comparison

Add a `Compare(other ProtocolVersion) ProtocolVersionComparison` method and an exported
`ProtocolVersionComparison` result type with named values:
`AheadMajor`, `OutdatedMajor`, `AheadMinor`, `OutdatedMinor`, `AheadPatch`, `OutdatedPatch`,
`AheadPrerelease`, `OutdatedPrerelease`, `Matching`, `DiffVersionType`, `DiffBuild`,
`EmptyVersion`, `InvalidVersion`.

Comparison semantics (receiver compared against `other`):

- If either operand is the zero value (all 32 bytes zero) → `EmptyVersion`.
- Otherwise if the two `version-type` bytes differ → `DiffVersionType`.
- Otherwise if the version type is non-zero (unrecognized) → `InvalidVersion`.
- Otherwise (both version-type 0): if the two `build` fields differ → `DiffBuild`
  (different builds are not comparable, regardless of the version numbers).
- Otherwise compare `major`, then `minor`, then `patch`, then `pre-release`, in that precedence
  order. The first field that differs decides the result: if the receiver's field is greater it is
  "ahead" (`AheadMajor`/`AheadMinor`/`AheadPatch`/`AheadPrerelease`), if smaller it is "outdated"
  (`OutdatedMajor`/…). If all four are equal → `Matching`.

## Serialization

A `ProtocolVersion` must encode in JSON (and via text marshaling) as a single `0x`-prefixed
32-byte hex string, and decode back from that same representation. Decoding input of the wrong
length must return an error.
