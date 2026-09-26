## Problem Statement

I’m using the tree helpers and I keep needing to transform a tree without flattening it or manually rebuilding the children. Could we add a way to map over a whole tree while preserving its shape, plus a variant that only maps the leaves? It would also be nice if the leaf collection / array conversion callbacks got the same traversal context, so I can use parent info or indexes when producing values.

## Expected Outcomes

- Structure-preserving mapping: `mapTree` should map every node in a tree and return a new tree with the original shape preserved.
- Leaf-only mapping: `mapTreeLeaves` should map only leaf nodes while preserving branch nodes and the overall tree shape.
- Leaf collection customization: `leavesBy` should collect only leaf nodes and apply its callback before placing each leaf in the returned array.
- Traversal context: callbacks used by `mapTree`, `leavesBy`, and `treeToArrayBy` should receive the standard traversal context, including the current node, sibling index, parent chain, and parent-index chain where applicable.
- Pre-bound helpers: `tree(...)` should expose pre-bound `leavesBy`, `map`, and `mapLeaves` helpers, and those helpers should work with the tree traversal behavior supplied to `tree(...)`.

## Implementation Notes

- The exact traversal strategy, helper decomposition, and data structures are up to the implementation as long as the public tree-helper behavior is preserved.
- The mapping helpers should avoid flattening as their observable result and should not require callers to manually rebuild children for ordinary use.
- Existing tree helper behavior should remain compatible unless explicitly extended by the outcomes above.
