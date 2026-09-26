Vault's Shamir shares currently contain only polynomial payload bytes and a final x-coordinate. That is enough for interpolation, but it gives recovery tooling no way to know the intended threshold or detect a damaged/mismatched share before returning garbage. Introduce a self-describing verified share envelope for newly split secrets while retaining read compatibility with shares already stored or distributed.

New shares returned by `shamir.Split` must use this exact byte layout:

- bytes 0-3 are the ASCII marker `VSS1`;
- byte 4 is the threshold, in the existing valid range 2 through 255;
- bytes 5-20 are an opaque 16-byte share-set identifier, identical in every share returned by one `Split` call;
- byte 21 is that share's nonzero, unique x-coordinate;
- starting at byte 22 are exactly `len(secret)` Shamir y-value bytes;
- the final 32 bytes are `SHA-256(secret)`, identical in every share.

This makes the public `ShareOverhead` constant 54, and every returned share must be `len(secret) + ShareOverhead` bytes long. The number of shares, threshold rules, and underlying Shamir reconstruction behavior remain as before.

`shamir.Combine` must recognize the new envelope and validate the complete supplied set before returning a secret. If any supplied share starts with `VSS1`, all supplied shares must be valid VSS1 shares of the same length and must agree on marker, threshold, identifier, and digest. Their x-coordinates must be distinct and nonzero. Fewer shares than the encoded threshold is an error; exactly the threshold or any larger valid subset reconstructs successfully regardless of input order. Recompute SHA-256 after interpolation and reject a payload or digest mismatch. Every supplied share participates in this decision: a corrupt extra share must not be ignored merely because an earlier threshold-sized subset is valid.

Keep backward compatibility for the legacy `y-bytes || x-coordinate` format when none of the supplied shares has the VSS1 marker. Valid legacy shares must continue to reconstruct in any order, including when more than two points are supplied. Apply the nonzero-coordinate check to legacy shares as well, while retaining the existing checks for too few shares, unequal or too-short shares, and duplicate coordinates.

For every validation or integrity failure, `Combine` returns a nil secret and a non-nil error; error wording is not prescribed. Preserve `Split`'s existing rejection of an empty secret, parts below threshold, parts above 255, and thresholds outside 2 through 255.
