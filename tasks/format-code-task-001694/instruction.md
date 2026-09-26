## No way to query my own pending team access requests

After a user calls `teamRequestAccess` on some team, there doesn't seem to be any way (from the client side / RPC layer) for that same user to find out which teams they currently have a pending access request for.

`teamListRequests` goes the other direction — it lists requests that *other* users have made to teams I administer. There's no symmetric call that says "give me the access requests *I* have outstanding".

This matters for a couple of UI scenarios:

1. Showing the user a list of "teams you've requested to join, waiting on approval" somewhere in the app.
2. Before letting the user hit "Request access" on a team again, checking whether they already have a pending request for that team, so we don't double-request or have to show a confusing state.

Right now to implement either of those the client basically has to remember locally what it asked for, which won't survive reinstall / different device, and won't reflect server-side state (e.g. the request being canceled or processed elsewhere).

Could the teams RPC protocol expose a way to fetch the current user's outstanding access requests? Filtering by a specific team name (for the second use case above) would also be useful so we don't have to pull the full list just to answer "did I already request team X?".

I'd expect the new helper on the `teams` package to be something like `ListMyAccessRequests(ctx, g, *teamName)` returning the list of teams the current user has pending requests on.
