## Approvals validator: leaving a plain comment on a PR seems to wipe out a previous approval

I'm using mergeable with the `approvals` validator configured (just requiring 1 approval). I'm hitting a weird case where an already-approved PR stops being considered approved.

Repro is roughly:

1. Open a PR.
2. A reviewer submits an **Approve** review. ✅ mergeable marks the PR as approved, as expected.
3. The same reviewer (or another one) later submits a **Comment** review on the PR — no approval, no request-changes, just the "Comment" option in the GitHub review UI.
4. mergeable re-evaluates and now the PR is **no longer approved**, even though the original Approve review was never dismissed.

Per the GitHub review semantics, leaving a plain comment on a PR shouldn't nullify an existing approval — only "Request changes" or dismissing the review should. So this is surprising behavior.

I dug a bit and it really does look tied to the comment-style review specifically: if step 3 is skipped, the PR stays approved indefinitely. As soon as any reviewer drops a comment-only review in there, the approval check flips to failing.

Would expect: comment-only reviews are ignored when computing the approval state, and the prior Approve review should still count.
