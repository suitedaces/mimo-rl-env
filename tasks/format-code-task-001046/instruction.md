The routing daemon's Dijkstra helper currently assumes every declared node is reachable, depends on map/input order for some choices, and loses information when the edge list contains nodes or repeated links. That makes SPT results unsafe for real topology snapshots, which commonly include partitions and duplicated advertisements. Please make Topology.SPT robust and deterministic without changing its public signature or the existing Node, Edge, Path, and SPT result types.

Required behavior:

- NewTopology must treat every endpoint appearing in an edge as a topology node, even when that endpoint was omitted from the nodes argument. Edges remain directed.
- SPT must never panic because a declared node is disconnected. From a known source, unreachable nodes remain present with Distance -1 and an empty edge list, while reachable nodes still receive their shortest paths.
- If the source was not declared and does not occur in any edge, return exactly the topology's nodes, all unreachable; do not add the unknown source to the result.
- Repeated directed edges for the same ordered pair represent duplicate advertisements. Retain the smallest non-negative distance regardless of input order. Negative-distance edges are unusable and must not participate in reachability or path selection.
- For equal-cost shortest paths, choose one canonical path by lexicographically comparing the complete sequence of Node.Name values from source through destination. This result must be independent of edge slice order and Go map iteration; comparing only the final predecessor is not sufficient.
- Zero-cost edges are valid. Self-loops and zero-cost cycles must not create cyclic Path values or prevent termination. Every returned reachable path must remain a finite, loop-free directed edge sequence.
- Distance arithmetic must not wrap int64. A candidate whose addition would overflow is unusable, but an actual path whose total is exactly math.MaxInt64 remains a valid reachable path.

Keep the normal existing behavior: the source has distance zero with no edges, Path.Distance is the sum of its edge distances, and an unreachable path uses the existing -1 sentinel.
