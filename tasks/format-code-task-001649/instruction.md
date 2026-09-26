## A few API inconsistencies around `Guard` reuse and the default hasher

I've been using `flurry::HashMap` in a multi-threaded service and ran into two papercuts that feel like they should be fixed together.

### 1. Some methods don't accept a `&Guard`, breaking guard reuse

The crate-level docs explicitly encourage reusing a single `Guard` across multiple calls to amortize the cost of pinning:

> You obtain a `Guard` using `epoch::pin`, and you can use references to the same guard to make multiple API calls if you wish.

And indeed, most of the API follows that pattern — `get`, `insert`, `remove`, `iter`, etc. all take `&Guard`. But a handful of methods don't:

- `contains_key`
- `get_and`
- `reserve`
- `retain`
- `retain_force`

These pin their own `Guard` internally. So if I'm doing something like:

```rust
let guard = epoch::pin();
map.reserve(extra);              // wants to use `guard`, can't
for k in incoming {
    map.insert(k, compute(), &guard);
}
map.retain(|k, _| keep(k));      // same issue
```

I can't pass my already-pinned guard to `reserve` / `retain`, even though I'm explicitly trying to keep one epoch alive across the whole batch. The methods just silently pin a fresh one each time. This is inconsistent with the rest of the API and works against the documented guard-reuse model. It would be nice if all of these accepted `&Guard` like everything else.

### 2. `HashMap::new()` is hard-wired to `RandomState`

I wanted to construct a map with a custom hasher type:

```rust
let map: HashMap<MyKey, MyVal, MyBuildHasher> = HashMap::new();
```

where `MyBuildHasher: BuildHasher + Default`. This doesn't compile — `new()`, `with_capacity()`, `Default`, and the `FromIterator` impls are all defined only for `HashMap<K, V, RandomState>`. The only way to get a custom hasher in is via `with_hasher(MyBuildHasher::default())`, which is annoying when the hasher already implements `Default` and there's no reason `new()` couldn't just use it.

It would be great if these convenience constructors worked for any `S: BuildHasher + Default`, with the current `RandomState` behavior preserved as the default when the user doesn't specify `S`.

Both of these are small, but together they make the API noticeably nicer to use.
