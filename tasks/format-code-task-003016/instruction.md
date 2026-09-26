## Problem Statement

Hey, I'm using xgi for some higher-order network stuff and I really need to work with simplicial complexes, not just hypergraphs — the whole point is that if I have a triangle {1,2,3} in there, the edges {1,2}, {1,3}, {2,3} should also be considered part of the complex automatically, and adding the same face twice (or in a different order) shouldn't duplicate it. Right now I'd have to babysit all of that myself on top of Hypergraph. Could you add a proper SimplicialComplex class that handles the downward-closure and dedup for me? Ideally it'd also stop me from accidentally calling the regular add_edge stuff on it, since that doesn't really make sense for a complex. Oh, and somewhat related — it'd be handy to have a quick way to ask a Hypergraph "which edges are duplicates?", I keep writing that loop by hand.

## Expected outcomes

- xgi should expose a public `SimplicialComplex` type that can be imported and instantiated like the other core classes, and that works as a specialized kind of `Hypergraph`.
- The simplicial-complex API should provide simplex-oriented ways to add one simplex, add several simplices, and check whether a simplex is present.
- Adding a simplex should use order-independent face identity, avoid duplicate faces, and make the relevant lower-dimensional non-singleton faces available automatically.
- Attempts to use the regular Hypergraph edge add/remove mutation APIs on a `SimplicialComplex` should fail with `XGIError` and guide users toward simplex-oriented operations instead.
- The user-facing summary for a `SimplicialComplex` should describe simplices rather than ordinary hypergraph edges, including the object name when one is set.
- `Hypergraph` should provide a public helper for reporting edge memberships that occur more than once, returning no entries when there are no duplicates.

## Implementation notes

- The concrete internal representation, identifier allocation, helper functions, validation location, and counting algorithm are up to the implementation, as long as the public behavior above is preserved.
- Tests and callers should rely on public class, method, exception, view, and summary behavior rather than on private storage layout.
