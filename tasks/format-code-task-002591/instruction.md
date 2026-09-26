## Feature request: maximal clique discovery

I'm using LightGraphs.jl to analyze some undirected graphs (social network style data) and I'd like to enumerate all maximal cliques — i.e. the maximal complete subgraphs. As far as I can tell there's currently no built-in way to do this in LightGraphs.

The older Graphs.jl package has this functionality, but I'd really like to stay within LightGraphs since I'm already using its `Graph` type, `add_edge!`, neighbor queries, etc., and I'd rather not pull in another graph library just for this one operation.

Could clique enumeration be added to LightGraphs? Something that, given a `Graph`, returns all maximal cliques would be perfect. For example, on a tiny graph like

```julia
g = Graph(3)
add_edge!(g, 1, 2)
add_edge!(g, 2, 3)
```

I'd expect to get back the two maximal cliques `{1,2}` and `{2,3}`.

A name like `maximal_cliques(g)` would feel natural to me.

Thanks!
