## Analyzing try pushes times out because we try to apply too many patches

When I run the patch analysis on a try push, sometimes it pulls back a huge stack of patches and then times out before it can finish. The stack size doesn't match what was actually pushed.

For example, on this push:
https://treeherder.mozilla.org/#/jobs?repo=try&selectedJob=296920031&revision=ada172630f8641c8ec0fc9de09755658f7a5eaa7

we end up with 76 patches to apply and analyze, which is way more than what this push actually contributed on top of the base — most of those patches are stuff that was already on the base revision the developer pushed against. We just inherit all of that context when we hit the hgmo `json-automationrelevance` endpoint for the try revision, and then we try to apply/analyze all of it. On a push of any reasonable size this basically guarantees a timeout.

For try pushes, the stack we work on should be limited to the patches that are actually part of *this* push (i.e. the new ones the developer is testing), not the entire history that automationrelevance happens to return alongside them. For non-try branches the current behavior is fine.

Could `get_hgmo_stack` be adjusted so that, when the branch is `try`, the returned stack only contains the changesets that were actually pushed in that try push, instead of every changeset the endpoint returns?
