## Separator DSL methods produce incorrect lookahead / possible tokens

When a rule uses the separator variants of the repetition DSL methods (`MANY_SEP` / `AT_LEAST_ONE_SEP`), the computation of the possible next tokens / lookahead paths gives wrong results.

For example, given a rule along the lines of:

```ts
this.RULE("list", () => {
    this.MANY_SEP({
        SEP: Comma,
        DEF: () => { this.CONSUME(Identifier) }
    })
})
```

After consuming an `Identifier`, the set of possible following tokens should include the separator (`Comma`) as one of the options (since the repetition may continue), in addition to whatever can follow the rule. In practice the separator is missing / not produced correctly by the path computation, which then breaks downstream features that rely on it (syntactic content assist, lookahead, etc.).

The non-separator variants (`MANY` / `AT_LEAST_ONE`) behave correctly for the same shape of grammar — the problem is specific to the `*_SEP` DSL methods.

Could the path / lookahead computation be fixed so that separator repetition methods produce the same kind of correct results as their non-separator counterparts?
