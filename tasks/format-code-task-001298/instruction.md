## Deleting a tracked time entry via the API crashes the server

I'm building a small dashboard on top of Gitea's time tracking and ran into trouble with the delete endpoint.

### What I did

1. Created an issue in one of my repos.
2. Logged a couple of time entries against it via `POST /repos/{owner}/{repo}/issues/{index}/times`. That worked fine and I got back the entries with their IDs.
3. Tried to remove one of them with:

   ```
   DELETE /repos/{owner}/{repo}/issues/{index}/times/{id}
   ```

### What happened

Instead of getting `204 No Content` back, the request fails with a `500 Internal Server Error`. The Gitea process logs an error around that request and the time entry is left in a weird state — subsequent calls to delete the same id still don't behave like a normal "already gone" response, they just keep erroring out instead of cleanly returning a 404.

I'd expect:

- Deleting an existing tracked time entry to just succeed with `204`.
- Deleting a tracked time id that doesn't exist anymore (already removed, or never existed) to return `404 Not Found`, not a 500 and not silently succeed.

This is fairly important for us because the dashboard does a lot of "create then delete" cycles when users edit their logged times, and right now any delete tips the API over.
