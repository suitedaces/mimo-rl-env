## Problem Statement

I'm seeing weird behavior in the AWS cost report when I group by org unit: paging doesn't actually change the org_entities list, the total count looks wrong, and sorting by cost doesn't seem to affect the org units inside each day. Also, passing `*` as the org unit probably shouldn't be accepted there. While you're in the repo, can you also make pyup only open security-related updates and make the unit test dependency cache separate per git ref?

## Expected outcomes

- AWS cost report requests grouped by `org_unit_id` apply `filter[limit]` and `filter[offset]` to each returned day's `org_entities` list, so different offsets expose different windows and the limit caps the number of org units returned per day.
- AWS cost report pagination metadata for `group_by[org_unit_id]` reflects the number of unique org unit entities available before the requested page is applied.
- AWS cost report requests grouped by `org_unit_id` order each day's `org_entities` by `values[0].cost.total.value`; `order_by[cost]=asc` returns ascending order, and `order_by[cost]=desc` returns descending order.
- AWS cost report requests with `group_by[org_unit_id]=*` are rejected as invalid input with an `org_unit_id` validation error that includes `Unsupported parameter or invalid value`.
- The pyup configuration only opens dependency updates for insecure packages.
- The unit test workflow dependency cache is separated by git ref so different branches or refs do not share the same dependency cache key.

## Implementation notes

The specific data structures, helper boundaries, and validation locations are up to the implementer. Preserve the existing public API shape for AWS report requests and responses while making the observed behavior consistent with the outcomes above.
