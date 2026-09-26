Add escape function to escape CSS identifiers
From the spec:

- If the character is NULL (U+0000), then the REPLACEMENT CHARACTER (U+FFFD).
- If the character is in the range [\1-\1f] (U+0001 to U+001F) or is U+007F, then the character escaped as code point.
- If the character is the first character and is in the range [0-9] (U+0030 to U+0039), then the character escaped as code point.
- If the character is the second character and is in the range [0-9] (U+0030 to U+0039) and the first character is a "-" (U+002D), then the character escaped as code point.
- If the character is the first character and is a "-" (U+002D), and there is no second character, then the escaped character.
- If the character is not handled by one of the above rules and is greater than or equal to U+0080, is "-" (U+002D) or "_" (U+005F), or is in one of the ranges [0-9] (U+0030 to U+0039), [A-Z] (U+0041 to U+005A), or \[a-z] (U+0061 to U+007A), then the character itself.
Otherwise, the escaped character.
