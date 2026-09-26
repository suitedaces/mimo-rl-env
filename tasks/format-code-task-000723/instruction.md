## Role REST API silently drops `handle` on create / update

I'm wiring up a small admin tool against the Corteza system API and I want to give each role a stable, machine-friendly `handle` next to its display `name` (similar to what users and the signup endpoint already accept). The `Role` type itself looks like it carries a handle, and other resources expose it on their endpoints, so I assumed `POST /roles/` and `PUT /roles/{roleID}` would too.

What I'm seeing:

- I `POST` to `/roles/` with a body containing `name`, `handle`, and `members`. The role is created, but when I `GET` it back the `handle` is empty. Same thing if I send the field at create time and then read the role list — handle is never populated.
- I tried patching it in afterwards via `PUT /roles/{roleID}` with `handle` in the body. Also a no-op — the field appears to be ignored, the stored role still has no handle.
- Looking at `docs/system/README.md` under "Create role" / "Update role details", the request parameter tables only list `name` and `members`. Compare that to the users / signup sections where `handle` is listed explicitly. So it looks like the role endpoints just never wired `handle` through, even though the underlying model supports it.

Expected: `POST /roles/` and `PUT /roles/{roleID}` should accept `handle` in the request body, persist it on the role, and the API spec + docs for those two endpoints should reflect that the parameter exists. Required-ness of `handle` should follow whatever convention the existing `name` parameter uses on each of those endpoints (so that create and update stay consistent with each other).
