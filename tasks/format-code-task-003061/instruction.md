# Add a binary (byte-transparent) character set and fix ECI value resolution

Our character-set / ECI machinery is used to translate raw barcode payload bytes into Unicode
and back. Two things are missing/wrong today.

## 1. A binary character set

Some symbologies carry a "this is raw 8-bit data, do not transcode it" channel, which in the
ECI register is character set **899**. We need a first-class character set for it. Add a new
`CharacterSet` enumerator named `BINARY` and wire it into the ECI lookup tables so that it is
fully addressable:

- It resolves from the ECI number `899`.
- It resolves from the encoding name `"BINARY"` (name lookups are case-insensitive, like the
  others).
- Its ECI number reports back as `899`.

`BINARY` is byte-transparent in both directions:

- **Decoding** a byte buffer as `BINARY` maps every input byte `0x00`–`0xFF` to the Unicode code
  point of the exact same numeric value. So decoding the 256-byte sequence `0x00,0x01,…,0xFF`
  yields a string whose code points are `0x0000,0x0001,…,0x00FF` in order, with no substitutions
  or dropped bytes.
- **Encoding** a string as `BINARY` is the exact inverse for code points up to `0xFF`: each code
  point becomes the byte of the same value, so a decode followed by an encode round-trips the
  original bytes. (Code points above `0xFF` cannot be represented and should be rejected the same
  way the existing single-byte Latin-1 path rejects them.)

## 2. Correct ECI numbers for `ValueForCharset`

Looking up the ECI number for a `CharacterSet` currently returns some stale/incorrect values:

- ISO-8859-1 must report its modern designator **3**, not the obsolete value `1`.
- A `CharacterSet` that has no ECI assignment (e.g. an unknown one) must report **-1** to signal
  "no ECI", rather than silently returning `0` (which is itself a valid ECI).
- Character sets that already have a single unambiguous designator keep it (for example
  ISO-8859-2 → 4, UTF-8 → 26, EUC-KR → 30), and `BINARY` reports 899.

The forward lookups (number → character set, name → character set) must stay consistent with the
existing register; you are only adding `BINARY` and correcting the reverse lookup described above.
