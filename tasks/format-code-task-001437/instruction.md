## Problem Statement

I'm seeing `parser.fieldsToExpression(...).stringify()` turn a day-of-week list like `1,3,5` into `1/2`, which seems wrong because that expression also matches another day I didn't include. Can you make it keep the explicit list in cases like that instead of shortening it into a step that changes what the cron means?

## Expected Outcomes

- When a cron field contains an explicit list of values, `parser.fieldsToExpression(...).stringify(...)` must not shorten it into a stepped expression that would match values outside the original list.
- A day-of-week list such as `1,3,5` should remain an explicit comma-separated list when stringified, because a broader step form would change the schedule.
- Existing safe step serialization should continue to work when the stepped form represents exactly the same set of values as the original field.
- The same behavior should apply through equivalent public stringify paths, including parsing an expression and stringifying it again.

## Implementation Notes

- Choose the validation and serialization approach that best fits the existing code structure.
- Preserve existing public API behavior except where needed to prevent semantically broader stepped output.
- The implementation should compare cron meaning rather than only formatting shape, so equivalent safe compact forms remain allowed.
