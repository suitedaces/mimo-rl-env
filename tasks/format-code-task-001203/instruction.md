## Banned users can still use the API

We use the `:banned` role to lock abusive users out of the site, but it looks like the API doesn't honour it.

Steps to reproduce:

1. Pick a user with an existing API key and give them the banned role (`user.add_role :banned`).
2. With that user's API key, hit something like `GET /api/articles/me` — the request still goes through and returns their data, just like an unbanned user.
3. Same thing if they're signed in via the session cookie or via an OAuth token — the API treats them as a normal authenticated user.

I'd expect a banned user to be rejected by the API the same way they're blocked from acting on the site, regardless of which auth mechanism they use (session, api-key header, or doorkeeper token).

A couple of related things I noticed while poking at this:

- A banned user can still go to `/settings/account` and generate a brand-new API key for themselves. That obviously defeats the point of banning them — even if we start rejecting their existing keys, they can just mint a new one. Creating new API keys should not be allowed for banned users.
- When a user is deleted, their existing API secrets seem to stick around in the database. I'd expect those to be cleaned up alongside the rest of their auth-related records (access grants, access tokens, etc.) in the user delete flow.

Happy to help test a fix.
