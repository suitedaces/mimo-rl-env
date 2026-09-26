# Upgrade the templated expression language with literals and inline ternaries

Our templated expressions — the `${{ ... }}` snippets used throughout workflow
definitions — can currently only reference a context (`ACTIONS`, `INPUTS`,
`SECRETS`, `TRIGGER`, ...) or call an inline function (`FNS.<name>(...)`),
optionally followed by a `-> <type>` typecast. Authors keep hitting walls when
they just want a constant value or a small conditional, and today the only way
to get a literal into an expression is to wrap it in a typecast like `int(5)`.

Make the expression language richer in three ways.

**1. Literals as first-class expressions.** A full template whose body is a bare
literal must evaluate to the corresponding native Python value, with the right
type:

- Integer literals → `int` (e.g. `${{ 42 }}` is `42`, `${{ -5 }}` is `-5`).
- Float literals → `float` (e.g. `${{ 3.14 }}` is `3.14`).
- String literals wrapped in single or double quotes → `str` with the quotes
  stripped and the inner text (including spaces) preserved
  (`${{ "hello world" }}` is `hello world`, and `${{ 'hi' }}` is `hi`).
- Boolean literals `True` and `False` → `bool`.

The existing `-> <type>` typecast must keep working when applied to a literal
(e.g. `${{ 42 -> str }}` is the string `"42"`).

Literals must also be usable directly as function arguments, without a
typecast — `${{ FNS.add(1, 2) }}` evaluates to `3` and
`${{ FNS.greater_than(5, 2) }}` evaluates to `True`.

**2. Inline ternary expressions.** Support the form `A if C else B`. The
condition `C` is evaluated and standard Python truthiness decides the result: if
`C` is truthy the expression evaluates to `A`, otherwise to `B`. Each of `A`,
`C`, and `B` may itself be any supported operand — a literal, a context
reference, or a function call. For example, with an operand where `INPUTS.x` is
`20`:

- `${{ "yes" if INPUTS.flag else "no" }}` picks the branch based on `INPUTS.flag`.
- `${{ "big" if FNS.greater_than(INPUTS.x, 10) else "small" }}` is `"big"`.
- `${{ "a" if 0 else "b" }}` is `"b"` and `${{ "a" if 1 else "b" }}` is `"a"`.

**3. Short-circuit evaluation.** Only the selected branch of a ternary is
evaluated. The branch that is not taken must never be evaluated, so an otherwise
failing operand in the untaken branch (for instance a reference to a context
path that does not exist) must not cause the expression to raise.

All existing expression behavior — context/jsonpath lookups, inline function
calls, inline typecasts of function arguments, typecasting of results, and
inline substitution inside larger strings — must continue to work exactly as
before.
