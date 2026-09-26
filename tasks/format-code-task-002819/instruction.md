## Feature request: declare reverse `wants` from a stack

Right now a stack can use `wants = [...]` to say "whenever I'm selected, also pull in these other stacks". That works, but it only lets me express the dependency from one direction: the *selecting* stack has to know about all the things it should drag along.

I keep running into the opposite need. I have a stack — say a shared monitoring / alerting / compliance stack — that should be applied **whenever certain other stacks are selected**, but I don't want to (or can't) go edit every one of those other stacks and add my stack to their `wants`. Reasons vary: the consuming stacks are owned by different teams, or there are many of them and the list will grow, or I just want the coupling declared in the dependent stack itself (it's the one that knows it needs to ride along).

What I'd like is to declare this from the *other* side, inside the stack that wants to be dragged in. Something along the lines of: "this stack should be selected whenever any of these other stacks are selected."

Example of the kind of thing I want to express (pseudo-config):

```hcl
# in stacks/monitoring/stack.tm.hcl
stack {
  name = "monitoring"
  # I want this stack to be pulled in whenever stacks/app-a or stacks/app-b
  # are selected, WITHOUT having to edit those stacks.
}
```

When I then run terramate against `stacks/app-a` (or it shows up via changed-stack detection), `stacks/monitoring` should be included in the selected set the same way it would have been if `app-a` had listed it under `wants`. Order semantics should match `wants` — it's just the inverse direction of the same relationship.

Right now there's no way to do this; my only options are to add the monitoring stack into every consumer's `wants`, which doesn't scale and puts the declaration in the wrong place.

Could the stack schema gain a way to declare this reverse relationship, and have the orchestration layer expand the selected stack set accordingly? A natural name for the new attribute would be something like `wanted_by` (mirroring `wants`).
