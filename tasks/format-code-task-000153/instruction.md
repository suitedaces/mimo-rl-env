# Support wildcard patterns when selecting rules

Robocop lets users refer to a rule by its id (e.g. `0501`) or by its name
(e.g. `too-long-keyword`). The same idea is used internally whenever rules are
*selected by a pattern* — for example when listing rules that match something a
user typed. Today that selection only understands **exact** strings: a pattern
matches a rule only when it is byte-for-byte equal to the rule's id or its name.
That makes it impossible to ask for "everything in the naming category" or
"every rule whose name ends in `-keyword`".

Make rule selection understand **Unix shell-style wildcards**.

Concretely:

- A pattern is checked against **both** a rule's id and its name; the rule is
  selected when **either** of them matches the pattern.
- The following wildcards are supported in a pattern:
  - `*` — matches any number of characters (including none),
  - `?` — matches exactly one character,
  - `[seq]` — matches any single character in `seq`,
  - `[!seq]` — matches any single character **not** in `seq`.
- Matching is **case-insensitive**.
- A pattern that contains no wildcard characters keeps behaving exactly as
  before: it matches only when it is equal to the rule's id or name (so existing
  exact-match callers are unaffected).

There are two layers to this behaviour:

1. The per-rule check that answers "does this rule match the given pattern?"
   returns a truthy/falsy result and must honour the rules above. It must keep
   accepting an already-compiled regular-expression object as the pattern and go
   on matching that against the rule's id and name as it does now.
2. The routine that filters a whole collection of rules by a single (string)
   pattern returns the matching rules **sorted by ascending numeric rule id**,
   and **deprecated rules are never included** in that result, regardless of
   whether they match the pattern.

A bare `*` therefore selects every non-deprecated rule.
