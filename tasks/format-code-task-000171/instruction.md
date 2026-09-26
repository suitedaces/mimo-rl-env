I'm using the comment module and I want to let my users report comments programmatically, but I don't see any way to actually submit a report through the library right now. Ideally I'd like to pass in a reason for the report (like spam, porn, spoiler, etc.) and optionally some extra text when needed. Can you add a way to do this on a comment object?

Expected outcomes:
- Comment objects provide an asynchronous `report(...)` capability that submits a report for that specific comment and returns the API response as a `dict`.
- The reporting API accepts a semantic report reason via a public `ReportReason` enum covering the service-documented report reasons, with stable integer values compatible with the underlying service. It should include the common documented categories such as other, spam advertising, pornography, and spoilers.
- Optional extra report text is accepted only for the “other” report reason; using extra text with a non-other reason should be rejected with the library’s normal argument-validation error behavior.
- Submitting a report requires an authenticated credential; attempting to report without the required login/session information should fail through the library’s normal credential-validation behavior instead of silently submitting an unauthenticated request.

Implementation notes:
- Fit the new comment-reporting capability into the existing public comment module style and asynchronous request flow.
- The exact internal data structures, helper placement, request configuration layout, and validation location are up to the implementation, as long as the public behavior above is satisfied.
- Preserve existing behavior of unrelated comment operations.
