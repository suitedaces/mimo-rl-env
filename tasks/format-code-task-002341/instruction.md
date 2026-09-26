## Feature request: `AgentSet.get` for multiple attributes at once

When collecting data from agents in an `AgentSet`, I often want several attributes (say `wealth`, `age`, `position`) at the same time — e.g. to build a snapshot for analysis or to feed into a dataframe.

Right now `AgentSet.get` only accepts a single attribute name, so I end up calling it once per attribute:

```python
wealths   = model.agents.get("wealth")
ages      = model.agents.get("age")
positions = model.agents.get("pos")
```

This iterates over the AgentSet multiple times and is awkward when the list of attributes is dynamic (e.g. comes from a config). It would be nice if `get` could just accept multiple attribute names and return the corresponding values per agent in one call, so I can write something like

```python
data = model.agents.get([...some attribute names...])
```

and get the per-agent values back together. The single-attribute usage should keep working as before.
