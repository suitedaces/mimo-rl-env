I think I’ve hit a permissions hole: as a regular authenticated user with no AddContent rights on a target container, I can still POST to an object’s `@duplicate` or `@move` with `{"destination": "...", "check_permission": false}` and Guillotina copies/moves it there. I also noticed `@user_info` is reachable from a user that doesn’t have `guillotina.AccessContent` on the context.

Expected outcomes:
- `POST .../@duplicate` must not allow a request body value such as `"check_permission": false` to bypass the target container’s content-add permission requirements. A user without permission to add content at the requested destination should receive a permission/client error, and the destination should not contain the duplicate.
- `POST .../@move` must not allow a request body value such as `"check_permission": false` to bypass the target container’s content-add permission requirements. A user without permission to add content at the requested destination should receive a permission/client error, and the object should not be moved there.
- The public Python API `guillotina.content.duplicate(..., check_permission=True)` should enforce the relevant add-content security checks throughout the duplicate operation; only an explicit `check_permission=False` at that API level should disable those checks.
- `GET .../@user_info` should require `guillotina.AccessContent` on the context, so callers lacking that permission cannot access the user-info endpoint for that context.

Implementation notes:
- Preserve the existing public endpoint and API semantics except for the permission behavior described above.
- The exact validation location, internal helper structure, and error response shape are implementation details; focus on externally observable authorization behavior and object state.
