# Locate the argument under the cursor in a search query

The search query editor needs to know which argument the user's caret is currently
sitting on so it can offer the right autocomplete suggestions and replace the correct
span of text. We already have a helper that splits a raw query string into its
arguments, but nothing tells us *where* a given caret offset lands.

Add a utility, exported from the search query utils (the same module that exposes
`splitQueryByArgs`), that resolves the argument at a caret offset:

```
getArgumentAtOffset(query: string, offset?: number)
```

Given the raw `query` string and a caret `offset` (a position between characters,
`0 .. query.length`), it returns the argument the caret is on as

```
{ value: string, start: number, stop: number }
```

or `null` when the caret is not on any argument.

Semantics:

- **Tokenization must match how the editor already breaks a query into arguments.**
  Spaces and newlines separate arguments. A run wrapped in matching single (`'`) or
  double (`"`) quotes is one argument, and the quote characters are part of it (so
  spaces inside quotes do not split). A backslash escapes the following character, so
  an escaped space or quote stays inside the current argument and does not separate it
  or toggle quoting. Finally, a lone `*` that immediately follows the token `LOAD`
  joins it to form a single `LOAD *` argument.

- `start` is the index of the argument's first character and `stop` is the index just
  past its last character, both measured in the original `query` string — i.e.
  `query.slice(start, stop)` is exactly the returned `value` (quotes and escapes
  included, verbatim).

- An argument is "under the caret" when `start <= offset <= stop`. Because arguments
  are always separated by at least one whitespace character, at most one argument can
  match. A caret resting at the very end of an argument (`offset === stop`) or at its
  very start (`offset === start`) counts as being on that argument.

- When the caret falls in whitespace between arguments, before the first argument with
  whitespace in between, after a trailing separator, or in an empty query, return
  `null`.

- `offset` defaults to the end of the query (`query.length`) when omitted.

The result must be consistent with the editor's existing argument splitting for the
same input.
