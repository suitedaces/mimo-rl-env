## printer expands empty blocks onto two lines

When I run HCL through the `hcl/printer`, empty blocks are getting formatted with a stray newline between the braces. For example, given input like:

```hcl
variable "foo" {}
variable "foo" {
}

foo {
}

foo {
  bar = "mssola"
}
```

the printer outputs the empty blocks as

```hcl
variable "foo" {
}
```

instead of leaving them as `variable "foo" {}` on a single line. This happens both for blocks that were already written as `{}` in the source and for blocks written as `{\n}`.

This doesn't match what `gofmt` does for empty Go blocks — `gofmt` keeps `func f() {}` on one line and only expands the braces when there's something inside. I'd expect the HCL printer to follow the same convention: collapse truly empty blocks to `{}`, and only break onto multiple lines when the block actually has items (or comments) in it.

One thing to be careful about: a block can look "empty" in the sense that it has no items but still contain a standalone comment, e.g.

```hcl
variable "foo" {
  # Standalone comment should be still here
}
```

That comment should obviously still be preserved on its own line — it's only the genuinely empty `{}` case that should be kept on one line.
