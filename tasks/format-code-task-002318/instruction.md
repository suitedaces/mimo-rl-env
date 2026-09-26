## Nested `as` type assertions get wrapped in unnecessary parens

When I run Prettier on TypeScript that uses a double `as` cast (the common `value as unknown as TargetType` pattern that TS often forces you into), Prettier adds parens around the inner cast.

Input:

```ts
foo as unknown as Bar
```

Prettier output:

```ts
(foo as unknown) as Bar;
```

I'd expect it to stay as:

```ts
foo as unknown as Bar;
```

`as` is left-associative, so the parens around `foo as unknown` don't change anything — they're just noise and make the chain harder to read, especially when the double-cast is already an annoying-but-necessary workaround for TS's stricter conversion rules. Could Prettier leave nested `as` expressions unparenthesized?
