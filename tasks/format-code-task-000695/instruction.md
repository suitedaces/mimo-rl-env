## Filtering users by their GitHub user ID

We have a Coder deployment where most users sign in via GitHub OAuth. The `users` table already stores each user's GitHub user ID (it gets populated when they log in), but there doesn't seem to be a way to actually search/filter users by it from the outside.

A couple of concrete situations where this matters for us:

- Someone leaves the org, their GitHub username gets renamed/transferred, but the numeric GitHub user ID is stable. We'd like to look up the Coder account from that stable ID.
- We have some automation that, given a GitHub user ID from a webhook, needs to find the matching Coder user to take action on (audit, suspend, list workspaces, etc.). Right now we have to fetch all users and filter client-side, which doesn't scale.

I tried `coder users list` and the `GET /api/v2/users` endpoint — neither seems to accept any GitHub-ID-based filter. The data is clearly there in the DB, it's just not queryable.

Could we get a first-class way to filter the users list by GitHub user ID, both from the CLI (`coder users list`) and from the HTTP API? It would be enough for our use case if exact-match filtering is supported (one GitHub user ID in, the matching Coder user out, or empty if none).
