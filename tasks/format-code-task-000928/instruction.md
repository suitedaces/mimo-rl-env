Rename `bannedChars` and `bannedDigits` in string module
Extracted out of https://github.com/faker-js/faker/pull/1155#discussion_r922645362

The parameter names `bannedChars` and `bannedDigits` could be unified to e.g.:
- except
- without
- exclude

This needs to be done in v8.0 so we do not make breaking changes later on
