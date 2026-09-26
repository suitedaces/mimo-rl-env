# Bulk-delete dispatches by status filter

Right now the dispatch-management backend can only soft-delete dispatches one at
a time, by passing an explicit list of dispatch ids. The UI needs a "delete all"
capability so users can clear out every dispatch that matches whatever they are
currently looking at — i.e. the active status filter plus the search box — in a
single request.

Add a bulk deletion operation to the dispatch summary data-access layer (the
same component that already handles per-id deletion and the dispatch listing).
It should accept a request object `DeleteAllDispatchesRequest` with two optional
fields:

- `status_filter`: a dispatch status enum value, defaulting to a new `ALL`
  selector that means "every status".
- `search_string`: a string, defaulting to `""`.

Expose the behavior as a `delete_all_dispatches` method that takes such a request
and returns the same response shape used by the existing per-id delete
(`success_items`, `failure_items`, `message`).

Behavior:

- Selection. Only currently-active dispatches are eligible. A dispatch is
  selected when its status matches the filter **and** the search string is a
  case-insensitive substring of either its name or its dispatch id. An empty
  search string matches everything.
- Status filter semantics:
  - `ALL` selects dispatches in any status.
  - `COMPLETED` is a group selector: it selects dispatches that are `COMPLETED`
    as well as those in the post-processing states `POSTPROCESSING`,
    `POSTPROCESSING_FAILED`, and `PENDING_POSTPROCESSING`.
  - Any other status value selects only dispatches in exactly that status.
- Deletion is a soft delete, consistent with the existing per-id delete: each
  selected dispatch and its electrons are marked inactive. Dispatches that are
  already inactive are never re-selected or reported.
- Response. `success_items` contains the dispatch ids (as UUIDs) that were
  deleted; order is not significant. When at least one dispatch was deleted the
  `message` is `"Dispatch(es) have been deleted successfully!"`. When nothing
  matched, `success_items` is empty and the `message` is
  `"No dispatches were deleted"`.

The existing per-id delete operation must keep working unchanged.
