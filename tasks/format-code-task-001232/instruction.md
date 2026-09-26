# Support `!important` in the diagram style sheets

Gaphor styles diagrams with a small CSS engine. Selectors are matched against
diagram nodes and the matching rules are cascaded into a single set of style
properties, where more specific selectors (and, on a tie, rules that appear
later in the sheet) win.

Right now the engine silently ignores the standard CSS `!important` marker: a
declaration written as `color: red !important` is treated exactly like
`color: red`, so it can still be overridden by a more specific or later rule.
That makes it impossible to force a property value from a base/general rule.

Please make the cascade honor `!important`.

Expected behavior, observable when a compiled style sheet is matched against a
node:

- A declaration flagged `!important` takes precedence over any conflicting
  declaration that is **not** important, even when the non-important
  declaration comes from a selector with higher specificity, and even when the
  non-important declaration appears later in the style sheet.
- Importance is a property of the individual declaration, not of the whole
  rule. Non-important declarations sitting in the same `{ ... }` block as an
  important one keep cascading normally.
- When two `!important` declarations target the same property, the usual
  cascade decides the winner: higher specificity first, and on a tie the
  declaration that appears later in the sheet.
- When no `!important` is involved, the cascade is unchanged: specificity
  first, then source order.
- The `!important` marker only affects priority — it must not leak into or
  corrupt the parsed property value. A declaration parses to the same value
  whether or not it carries `!important`. Recognition follows the CSS rules
  (case-insensitive, optional surrounding whitespace).

The behavior is exercised through the existing public styling API used to
compile a style sheet and match a node against it.
