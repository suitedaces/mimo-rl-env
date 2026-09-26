# Add cell representation hashing

Our cell library can build cells, serialize them to BOC and parse them back, but
there is currently no way to get the canonical hash of a cell. We need it: a cell's
hash is what uniquely identifies it (and its whole sub-tree of references) across the
TON blockchain, and downstream code — dictionaries, account state, message
identifiers — all rely on being able to address a cell by its hash.

Please add a way to compute the **standard cell representation hash** of a finished
cell. Expose it as a `Hash()` method on the built cell type that returns the raw
32-byte digest (`[]byte`).

The value must be the representation hash exactly as defined by the TON cell
specification, so that it matches the hashes the network itself assigns to cells.
Concretely, the digest is the SHA-256 over the cell's standard representation, which
is the concatenation of, in order:

- the two descriptor bytes — the first encodes the reference count (an ordinary,
  non-special, level-0 cell), the second encodes the cell's data bit-length;
- the cell's data bytes; when the bit-length is not a multiple of 8, the data is
  augmented with the standard completion tag (a single `1` bit followed by zero bits
  up to the next byte boundary) before being hashed;
- for every reference, in reference order, its depth encoded as a 2-byte big-endian
  value (a cell's depth is 0 when it has no references, otherwise one more than the
  maximum depth among its references);
- for every reference, in reference order, that reference's own 32-byte
  representation hash.

Behavioral expectations:

- The result is always 32 bytes.
- It is fully deterministic: hashing the same cell, or two independently built but
  identical cells, yields the same bytes; hashing the same cell twice does not change
  the cell or its hash.
- It is sensitive to content: cells that differ in their data, in the number or
  content of their references, or in the order of their references must produce
  different hashes.
- An empty cell (no data, no references) hashes to the SHA-256 of its two
  zero descriptor bytes.
