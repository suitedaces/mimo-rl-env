# Trigger-aware workflow graph model

Our workflow editor sends the backend a React Flow graph object describing a
workflow's topology. Historically the server treated the trigger as a special,
separate thing bolted onto the side of the graph. We're consolidating: the graph
the frontend sends now contains the trigger as a regular node in the node list,
right alongside the action nodes, and the server-side `RFGraph` model needs to
understand that shape.

A React Flow graph object is a plain dict with two keys:

- `nodes`: a list of node dicts. Each node has an `id`, a `type`, and a `data`
  object. There is exactly **one** node with `type == "trigger"`; every other
  relevant node has `type == "udf"` (an action node). An action node's `data`
  carries the namespaced action `type` (the UDF key), a human-readable `title`,
  and an `args` dict.
- `edges`: a list of edge dicts, each with a `source` and `target` node id (and
  an optional `label`). The trigger node is wired to the workflow's first action
  by a single dedicated edge (the "trigger edge"); all other edges connect action
  nodes to one another.

Rework `RFGraph` (in the workflow DSL graph module) so it parses this unified
shape and exposes the following behavior. `RFGraph.from_dict(obj)` should accept
such a dict and build the graph.

The model must distinguish the trigger from the action nodes:

- `trigger` returns the single trigger node.
- `action_nodes()` returns only the action (`udf`) nodes, preserving the order
  they appear in the input.
- `action_edges()` returns the edges that do **not** touch the trigger node.
- `entrypoint` returns the action node the trigger points to.
- A node's `ref` is the slugified form of its title (lowercased,
  non-alphanumerics collapsed to underscores), e.g. `"Action A"` -> `"action_a"`.

Dependency and ordering computations must ignore the trigger edge, treating only
the action subgraph:

- `topsort_order()` returns the action node ids in a valid topological order
  (the trigger is not part of it).
- The entrypoint action therefore has no action-level dependencies.

The graph can also be converted into the workflow's intermediate representation:
`action_statements()` returns one `ActionStatement` per action node (no external
input required), where each statement carries the node's `ref`, its action
`type`, its `args` (taken from the node data), and `depends_on` — the **sorted**
list of refs of the action nodes immediately upstream of it (the trigger
excluded).

Finally, parsing must reject malformed graphs by raising the project's workflow
validation error (`TracecatValidationError`) when:

- there is no action node,
- there is not exactly one trigger node, or
- the trigger does not connect to exactly one action node.
