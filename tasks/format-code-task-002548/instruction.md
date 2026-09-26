# Problem Statement

When I run rustfmt on files that have `lazy_static! { ... }` blocks, everything inside the macro just gets left untouched — the `static ref` declarations keep whatever weird indentation and alignment they came with. Could rustfmt actually format the contents of those blocks like it does for regular `static` items? And obviously if there's something funky inside it (comments, or syntax that isn't the usual `static ref NAME: TYPE = EXPR;` shape), I'd rather it just leave it alone than spit out broken code.

# Expected outcomes

- Formatting `lazy_static! { ... }` blocks should normalize ordinary `static ref` declarations in the block, including indentation, spacing around names/types/assignments, and formatting of right-hand-side expressions in the same spirit as comparable Rust items.
- Multiple ordinary `static ref` declarations in the same `lazy_static!` block should each be formatted consistently, while preserving their declaration order and visibility.
- If the contents of a `lazy_static!` block are not in the ordinary `static ref NAME: TYPE = EXPR;` form, rustfmt should avoid producing broken output and should not force those contents through the new formatting behavior.
- If a `lazy_static!` block contains comments, rustfmt should preserve the comments and avoid applying formatting that would drop, move, or otherwise mishandle them.

# Implementation notes

The implementation may choose any internal parsing, validation, and fallback strategy that fits rustfmt’s existing architecture. The important contract is the externally visible formatted output: normal `lazy_static!` declarations should become consistently formatted, while unsupported or comment-sensitive contents should remain safe and not be corrupted.
