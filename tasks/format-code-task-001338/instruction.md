# Problem Statement

I’m seeing the ASN.1 string types accept clearly invalid text — for example `PrintableString` lets through characters it shouldn’t, `IA5String` accepts non-ASCII, and `VisibleString` doesn’t complain about control characters. Could you make these restricted string types reject invalid input instead of silently storing or decoding it?

# Expected outcomes

- `ct.crypto.asn1.types.PrintableString` rejects values containing characters outside the ASN.1 PrintableString character repertoire when constructed or converted from a string-like value.
- Strict decoding of `ct.crypto.asn1.types.PrintableString` rejects encoded content containing characters outside the ASN.1 PrintableString character repertoire; non-strict decoding continues to allow such content.
- `ct.crypto.asn1.types.IA5String` rejects values containing non-7-bit-ASCII characters when constructed or converted from a string-like value.
- Strict decoding of `ct.crypto.asn1.types.IA5String` rejects encoded content containing non-7-bit-ASCII characters; non-strict decoding continues to allow such content.
- `ct.crypto.asn1.types.VisibleString` rejects values containing control characters, DEL, or non-visible/non-ASCII characters when constructed or converted from a string-like value.
- Strict decoding of `ct.crypto.asn1.types.VisibleString` rejects encoded content containing control characters, DEL, or non-visible/non-ASCII characters; non-strict decoding continues to allow such content.
- Invalid restricted-string input should fail with `ct.crypto.error.ASN1Error`; valid input for each string type should continue to round-trip through the existing public construction and decoding paths.

# Implementation notes

The validation mechanism, shared helpers, data structures, and exact location of the checks are implementation choices. Preserve existing behavior for unrestricted or unrelated ASN.1 string types, and keep the strict versus non-strict decoding distinction intact.
