## `av stack sync` leaves me on a detached HEAD after pruning merged branches

I noticed this on my normal stacked-branches workflow with `av`. Steps:

1. I'm on a feature branch (let's call it `feature-foo`) — verified with
   `git status` before I start.
2. Run `av stack sync`.
3. The sync rebases on top of `master`, pushes to GitHub, and asks me whether
   to delete branches that have been merged. I say yes (some parents earlier
   in the stack have already been merged into `master`).
4. Sync finishes successfully.

After it finishes, I'm no longer on `feature-foo`. `git status` shows
`HEAD detached at <some commit>` instead. I have to manually `git checkout
feature-foo` to get back to where I was.

It happens whether or not `feature-foo` itself was one of the branches
deleted in the prune step — even when only an ancestor branch in the stack
gets pruned, I still end up detached.

What I'd expect:

- After sync (including the prune step) finishes, I should be back on the
  same branch I was on when I ran `av stack sync`.
- If the branch I was on actually got deleted during prune (because it was
  merged), then falling back to the default branch (`master`/`main`) would
  be reasonable.
- Either way, I shouldn't be left on a detached HEAD — that's not a state
  I was in before running the command, and it's easy to miss and then
  accidentally commit onto.

Happy to provide more details if useful.
