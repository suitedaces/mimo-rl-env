**Extra space inserted inside LESS property access (`@map[@key]`)**

When I use LESS's property access (lookup) syntax to read a value from a namespace/map, Prettier puts a stray space after the opening bracket.

Input:

```less
a {
  color: @colors[@white];
}
```

After running Prettier:

```less
a {
  color: @colors[ @white];
}
```

The `@colors[@white]` lookup should be left alone — there shouldn't be a space between `[` and `@white`. Same applies whether the key is a variable (`@colors[@white]`) or a literal name (`@colors[white]`).
