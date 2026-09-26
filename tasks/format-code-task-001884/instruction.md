## Non-admin users can't change the owner of their own shopping list

I'm using Mealie as a regular (non-admin) household user. We share a shopping list and I wanted to hand it off to my partner, so on `/shopping-lists/<id>` I clicked the gear icon to open **Settings** — the dialog has an "Owner" dropdown that's supposed to let you pick a different user.

The dropdown is unusable for non-admin accounts:

- Logged in as a normal group member, the Owner select is empty — no users show up, so I can't pick anyone.
- The browser network tab shows the page is calling the admin users listing endpoint to populate that dropdown, and it comes back 403 for non-admins. So the request fails silently and the select just stays blank.
- If I log in as an admin, the same dropdown works fine and lists everyone — confirming it's purely a permissions problem on the data the dropdown is fetching, not a UI bug.

This feels wrong from a product standpoint: changing the owner of a shopping list to another member of *my own group* is a normal group-member action (we use one Mealie group per household), not an admin action. A non-admin owner of a list should be able to transfer it to another member of the same group without needing an admin to do it for them.

A few things I'd expect from the fix:

- Non-admin users opening Settings on one of their group's shopping lists should see the other members of their group in the Owner dropdown and be able to select one.
- Whatever data the dropdown fetches should be scoped to the current user's group — I shouldn't suddenly be able to see accounts from other groups on the same Mealie instance just because we relaxed the permission. The existing admin-only "list all users across all groups" behavior should stay admin-only.
- The dropdown only needs enough information to render and submit a choice (something to display per user + something to identify them when saving). It doesn't need to expose the full user record (auth method, admin flag, permissions, tokens, etc.) to non-admins.

I'd expect the new group-scoped listing to be exposed under something like `/api/users/group-users`.
