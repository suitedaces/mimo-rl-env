It seems `changesInclude` is not supported in Starlark.

(I'd expect the Starlark-side builtin to be something like `changes_include`, with a way to feed in the list of affected files via a larker option such as `WithAffectedFiles`.)
