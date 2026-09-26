Archive manifest filtering currently uses `internal/file.GlobMatch(pattern, name)`, but its wildcard behavior is byte-oriented and allows ordinary stars to consume directory separators. That makes archive paths behave differently from path-aware globbing elsewhere in Syft and makes patterns unexpectedly broad. Make this matcher path-aware while keeping its boolean API and existing simple matches compatible.

Matching is case-sensitive and applies to the entire pattern and name. Do not clean or normalize either value: a leading slash, repeated slash, or `.` component remains significant. Ordinary characters match literally.

Use these metacharacter rules:

- `*` matches zero or more Unicode code points other than `/`; `?` matches exactly one Unicode code point other than `/`.
- Exactly two stars used as a complete path component form a recursive `**` wildcard. It matches zero or more complete components, so `/usr/**/package.json` matches both `/usr/package.json` and deeper paths. A leading recursive component can match a root-level file, a trailing `/**` includes the base path itself and its descendants, and a bare `**` matches any whole path, including the empty path.
- Star runs that are not exactly `**` as a complete component are non-recursive and behave like one ordinary `*`. Thus `ab**cd` stays within one component, and a complete `***` component matches one component rather than crossing separators.
- Character classes match one non-separator Unicode code point. Support listed characters, inclusive ranges such as `[0-9]` and `[α-ω]`, and negation when either `!` or `^` is the first class character.
- Backslash quoting makes `*`, `?`, `[`, `]`, and backslash itself literal rather than metacharacters.

Malformed patterns must return `false` without panicking. This includes an unclosed or empty class, a descending range such as `[z-a]`, and a trailing escape. Preserve the existing behavior covered by the current `TestGlobMatch` table, including empty/exact matches and ordinary wildcard backtracking.
