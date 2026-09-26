## Feature request: easy access to support values on `TreeNode`

I'm working with phylogenetic trees that have bootstrap / Bayesian support values attached to internal nodes (a very common situation — basically any tree produced by RAxML, IQ-TREE, MrBayes, etc.). In Newick these usually show up as the internal node label, sometimes followed by `:branch_length`, e.g.

```
((a,b)95,(c,d):1.0);
((a,b)1.0:2.5,(c,d)'0.97:species_A');
```

When I parse these with `TreeNode.read([...])`, the support value ends up baked into `node.name` as a string, mixed in with whatever else is in the label (branch length, taxon annotation, quoted comment, ...). So if I want to do something simple like "drop / collapse every internal node whose bootstrap is below 70", I currently have to write my own parser for the node-name string at every call site, and remember all the corner cases (no label at all, label that's only a name, label that's `support:annotation`, label that's just a branch length, etc.).

It would be really nice if `TreeNode` itself exposed the support value as a first-class thing, so I could just do

```python
for node in tree.non_tips():
    s = node.support()
    if s is not None and s < 70:
        ...
```

and not have to care about how it's encoded in the label. When the node doesn't carry a support value (e.g. the label is a taxon name, or there's no label at all), I'd expect to get back something falsy/`None` rather than an error, so the above filter pattern stays clean.

Could this be added to `skbio.tree.TreeNode`?
