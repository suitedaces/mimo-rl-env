## Allow `--match` / `-m` to be specified multiple times

I keep my notes (recipes, in this example) in a `zk` notebook and use `zk list -m "..."` a lot. Often I want to narrow down by "must contain A AND must contain B", where A and B are independent ideas — possibly with their own NOT / phrase / wildcard operators inside.

The natural thing to type is:

```sh
zk list --tag recipe -m "pizza -pineapple" -m "mushrooms"
```

i.e. "recipes that talk about pizza but not pineapple, and that also mention mushrooms somewhere — in any order, not necessarily near the pizza part".

Today `--match` / `-m` only takes a single query, so the second `-m` just clobbers the first one. To get the same effect from a single `-m` I have to hand-merge the two queries into one fts expression, which gets awkward fast as soon as either side has a `-term`, an `OR`, or a quoted phrase — it's easy to write something that parses but means a subtly different thing than what I had in mind.

It would be much nicer if I could just pass `-m` several times and have all of the supplied queries need to match for a note to be returned, while the syntax *inside* each individual `-m` keeps working exactly like it does today (fts operators, `exact`, `re`, etc.).
