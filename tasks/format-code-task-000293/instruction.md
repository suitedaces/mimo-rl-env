# Add "helper" classes with function-like, parameterized syntax

Atomizer currently only understands *pattern* rules: a rule has a `prefix` plus a
list of `properties`, and a class name such as `P-10px` maps the matched value
onto those properties. We want to support a second kind of rule — a **helper** —
that behaves more like a function: the class name carries a parenthesized,
comma-separated argument list, and the rule supplies a declaration template whose
placeholders are filled in from those arguments.

## Declaring a helper rule

A helper is just another entry in the rules array passed to the `Atomizer`
constructor (or to `addRules`), distinguished by `type: 'helper'`:

```js
{
    type: 'helper',
    name: 'Line clamp',
    prefix: 'LineClamp',
    declaration: {
        'lines': '$0',
        'max-height': '$1'
    },
    rules: {
        '.base': { 'overflow': 'hidden' }
    }
}
```

- `prefix` is the token that starts the class name.
- `declaration` is a map of CSS property → value that acts as a template. A value
  may contain numbered placeholders `$0`, `$1`, `$2`, … referring to the
  arguments (0-indexed) taken from the class name.
- `rules` is optional. When present it is a map of additional, ready-made CSS
  blocks (selector → declarations) that this helper depends on.

A helper rule and ordinary pattern rules must be able to coexist in the same
`Atomizer` instance; class names of both kinds must be recognized.

## Class-name syntax

A helper class name is the prefix followed by a parenthesized, comma-separated
argument list, e.g. `LineClamp(2,40px)`. The argument list may also be empty,
e.g. `Bar()`. These names must be picked up by `findClassNames` just like
ordinary atomic class names are.

## CSS generation

`getCss` must turn a helper class name into a CSS rule whose selector is that
class name (with CSS-special characters such as `(`, `)` and `,` backslash-escaped,
exactly as other atomic class selectors are escaped) and whose body is the
helper's `declaration` with every `$N` placeholder replaced by the Nth argument
parsed from the class name. For example, with the helper above,
`LineClamp(2,40px)` yields a rule `.LineClamp\(2\,40px\)` declaring `lines: 2`
and `max-height: 40px`.

If the helper defines `rules`, those base CSS blocks must also appear verbatim in
the generated output.

A helper that has no `declaration` is invalid: when `getCss` is asked to generate
a class for such a helper it must throw an `Error`.
