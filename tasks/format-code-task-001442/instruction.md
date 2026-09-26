## `hclwrite.TokensForValue` produces awkward single-line output for objects/maps

I'm using `hclwrite` in a small Go tool that generates `.hcl` files
programmatically — I build up a `cty.Value` (typically an object with a
handful of attributes, sometimes nested) and pass it through
`TokensForValue` so I can write it out as HCL source for humans to read
and edit.

For lists and tuples the output looks reasonable, but for objects and
maps everything gets crammed onto one line, separated by commas:

```hcl
config = { bar = 5, baz = true, foo = "foo" }
```

This is pretty far from how the same value would normally be written by
hand or by `terraform fmt`, where you get one attribute per line and no
commas:

```hcl
config = {
  bar = 5
  baz = true
  foo = "foo"
}
```

It's especially noticeable once the values get nested or the number of
attributes grows past two or three — the single-line format becomes
genuinely hard to read, and diffs of the generated files are basically
unreadable since any change to a single attribute rewrites the entire
line.

Could `TokensForValue` emit objects and maps in the conventional
multi-line style instead, so the generated output looks like the HCL
people actually write?
