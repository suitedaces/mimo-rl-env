# Problem Statement

I’m seeing `shift-parser` accept strings like `"\07"` even after a `"use strict"` directive, both at the top level and inside function bodies. I expected strict mode parsing to reject those old octal escapes instead of giving me an AST — can you fix that?

# Expected outcomes

- In a script whose directive prologue enables strict mode, a later string literal containing a legacy octal escape sequence such as `\07` must fail parsing instead of producing an AST.
- In a function body whose directive prologue enables strict mode, a later string literal containing a legacy octal escape sequence must fail parsing instead of producing an AST.
- The parse error for a strict-mode legacy octal escape should identify the offending escape sequence, using the message prefix `Unexpected legacy octal escape sequence: \` followed by the octal digits that appeared in the source.
- Non-strict parsing behavior for string literals with legacy octal escape sequences should remain accepted.

# Implementation notes

- The implementation approach is up to the implementer.
- Preserve the parser’s existing public API shape and normal parsing behavior outside the strict-mode legacy-octal-escape case.
