## Can't chain assertions, and no built-in truthy/falsy check

I'm using this library to write tests and ran into two things that feel like they should already work but don't.

### 1. Chaining doesn't work

I often want to make several assertions about the same value. Right now I have to repeat `expect(...)` over and over:

```js
expect([1, 2, "foo", 3]).toBeAn(Array);
expect([1, 2, "foo", 3]).toInclude("foo");
expect([1, 2, "foo", 3]).toExclude("bar");
```

The natural thing to write would be:

```js
expect([1, 2, "foo", 3])
  .toBeAn(Array)
  .toInclude("foo")
  .toExclude("bar");
```

But that blows up — the second call in the chain doesn't have anything to call on, so I get an error immediately. It would be really nice if assertions on the same value just chained together.

### 2. No simple "this should have a value" / "this should not have a value" check

Lots of times I just want to say "this thing should be there" or "this thing should be empty/missing" without committing to an exact expected value. Things like checking that a lookup returned something, or that an optional field is unset.

Today I have to fake it with `toBe` against a specific value, or pick some other assertion that kinda-sorta works, which reads awkwardly and doesn't really say what I mean. It'd be much clearer to have dedicated assertions for "has a value" vs "doesn't have a value" alongside the other matchers.

Both of these feel like basic ergonomics for a BDD-style assertion library — would love to see them supported.

(Naming-wise, I'd expect the new matchers to be something like `toExist()` / `toNotExist()` to line up with the existing `toBe` / `toNotBe` style.)
