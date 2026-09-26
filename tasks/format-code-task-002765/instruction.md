# Add a `hierarchicalSelectors` option to the `indentation` rule

Our `indentation` rule currently expects indentation that mirrors the
*structural* nesting of the stylesheet: top-level rules sit at level 0,
declarations and nested rules get one extra level per enclosing block, and so
on.

A lot of people organise their stylesheets so that the *naming* of selectors
expresses a hierarchy — BEM-style names (`.foo`, `.foo-sub`) or combinator
chains (`#foo ul`, `#foo ul > li`) — and they like to indent those
relationships even though there's no extra block nesting. We want to support
that.

Add a new secondary option, `hierarchicalSelectors` (a boolean, defaulting to
`false`/absent), to the `indentation` rule. When it is enabled, indentation is
still measured the same way (same primary option, same warning message
`Expected indentation of <n> <space(s)|tab(s)> at line <line>`), but the
*expected* level for a rule gains extra steps based on the selector hierarchy.

Define the hierarchy like this:

- A rule **B** is *subordinate* to an earlier sibling rule **A** when B's
  selector starts with A's complete selector but is not identical to it
  (a proper prefix). Subordinate rules are expected to be indented one level
  deeper than their superordinate.
- The hierarchy nests arbitrarily deep: if C is subordinate to B and B is
  subordinate to A, then C is expected two levels deeper than A.
- Subordinate rules do not have to immediately follow their superordinate.
  Sibling rules that share the same superordinate are *peers* and are expected
  at the same level, even when other (more deeply nested) rules appear between
  them. A sibling that is not part of the hierarchy drops back to the level it
  would otherwise have.
- This extra indentation is *added on top of* the normal structural nesting, so
  hierarchical relationships work the same way inside a nested block as they do
  at the top level. Ordinary stylesheets with no prefix relationships between
  selectors are completely unaffected.

There's one special case for grouping at-rules such as `@media`: if an at-rule
directly follows a rule, contains at least one rule, and *every* rule it
directly contains is subordinate to that preceding rule, then the at-rule
itself is treated as subordinate to the preceding rule (indented one level
deeper), and the rules inside it are indented one level deeper still. If the
at-rule contains any rule that is *not* subordinate to the preceding rule, the
at-rule keeps its normal structural level.

The option only changes behavior when it is turned on; with it off (the
default) the rule must behave exactly as it does today.

## Examples (with primary option `2`)

These are warnings:

```css
.foo {}
.foo-sub {}
```

```css
.foo {}
  .foo-two {}
  .foo-two-sub {}
```

These are not:

```css
.foo {}
  .foo-sub {}
```

```css
#foo ul {}
  #foo ul > li {}
    #foo ul > li > a {}
#bar ul {}
```

```css
.foo {}
  .foo-one {}
  .foo-two {}
    .foo-two-sub {}
  .foo-three {}
.bar {}
```

```css
.foo {}
  @media print {
    .foo-one {}
    .foo-two {}
  }
.bar {}
```
