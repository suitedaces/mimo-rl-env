## `get_touched_functions` misses functions modified only by deletions

When mining commits, `get_touched_functions` is supposed to give us the set of functions a commit touches in a given file. But it only looks at the added lines of the patch — the deleted lines are never passed in.

The result is that if a commit only removes lines from a function (no additions inside that function), the function is not recorded in `commit.functions[path]` at all. From a "which functions did this commit modify" point of view that's clearly wrong: deleting code from a function is just as much a modification as adding code to it.

A simple example: a commit that removes a few lines from `foo()` and adds nothing inside it. Today `_transform` ends up with no entry for `foo` for that path; we'd expect `foo` (with its line range) to be in the touched set.

It would be good to also add a unit test for `get_touched_functions` covering this case (and the existing addition-only case), since right now it's not directly tested.

Refs #1161 which introduced the function.
