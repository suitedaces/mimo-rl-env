## SOFT_DELETE_CASCADE re-soft-deletes children that were already soft-deleted

I'm using `SOFT_DELETE_CASCADE` on a parent model that has a bunch of related children (also `SafeDeleteModel`). Workflow looks roughly like this:

1. Soft-delete one specific child on its own (e.g. `child.delete()`), some time ago. Its `deleted` timestamp gets set to that moment — good.
2. Later, soft-delete the parent. Because of the cascade policy, this is also supposed to soft-delete the remaining live children.

What I expected: the parent gets soft-deleted, the *still-live* children get soft-deleted now, and the child I had already deleted in step 1 is left alone — it's already deleted, there's nothing to do.

What actually happens: every related child goes through the soft-delete path again, including the ones that were already soft-deleted. So the child from step 1 has its `deleted` timestamp overwritten with the current time (I lose the original deletion time), and the soft-delete signals fire again for an object that was already in the deleted state. From the outside it looks like that child was just deleted now, which isn't true.

Could the cascade skip related objects that are already soft-deleted? Re-deleting something that's already deleted shouldn't be a no-op that quietly rewrites state.
