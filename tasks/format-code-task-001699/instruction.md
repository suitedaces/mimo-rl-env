Consider adding support for `--all` on `kn service delete`
### Feature request

Kubectl has a `--all` option to mean "all instances of the specified resource in the namespace". So for example: `kubectl delete ksvc --all` will delete all KnServices in the default namespace. I find this very useful when I want to quickly clean things up.

It would be really nice if we could do: `kn service delete --all` to delete all KnServices.

It might be good to look into whether we should support `--all` on other commands, like: describe, export, list and update. I'm less sure about some of those, but I do think `delete` will be popular.

### Use case

<!-- Please add a concrete use case to demonstrate how such a feature would add value for the user. If you don't have a use case for your feature, please remove this section (however providing a good use case increases the likelihood to be picked up) -->

/kind proposal
