## Automated transactions don't see inferred amounts

I have a journal that uses an automated transaction (transaction modifier) to tag a portion of food expenses, and like in most of my transactions I leave one posting's amount blank so hledger infers it. Something like:

```journal
= expenses:food
    (budget:food)   *-1

2020/01/01 lunch
    expenses:food      $10
    assets:cash
```

When I run with `--auto`:

```
$ hledger -f test.journal --auto print
```

I don't get the result I'd expect. The auto-generated posting from the `=` rule doesn't behave as if it matched a $10 food posting — it's as if the modifier sees the food posting before the cash side has been filled in, so the matched amount isn't really there yet.

If I instead spell both sides out explicitly:

```journal
2020/01/01 lunch
    expenses:food      $10
    assets:cash       $-10
```

then `--auto` produces what I expected (the budget posting reflects the $10 food amount).

So the bug seems specific to combining `--auto` automated transactions with the very common style of leaving one posting blank. As a user I'd expect those two features to compose: the automated postings should be generated against the transaction as it will actually appear (after amount inference), regardless of whether I wrote both amounts by hand or let hledger fill one in.

Without `--auto`, inferred amounts work fine, so this is only an issue when transaction modifiers are involved.
