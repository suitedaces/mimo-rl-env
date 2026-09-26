# Problem Statement

I’m using `ModelParamTraversal` to walk and update parameter trees, but importing it from `flax.optim` feels like the wrong place. Please make it available from `flax.traverse_util` as well, and move the docs there so it’s easier to find.

# Expected outcomes

- `flax.traverse_util.ModelParamTraversal(filter_fn)` is importable and usable as a public traversal utility for matching parameter-tree entries.
- Existing code that imports or accesses `flax.optim.ModelParamTraversal` continues to work.
- The API docs for `flax.traverse_util` include `ModelParamTraversal`, and the optimizer docs no longer present it as an optimizer-specific API item.

# Implementation notes

- The exact code organization is up to the implementer as long as the public import surface, traversal behavior, and backward compatibility are preserved.
- Follow the repository’s existing API-doc style.
- Avoid changing observable traversal semantics beyond the new public location and doc placement.
