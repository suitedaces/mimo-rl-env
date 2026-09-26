## Problem Statement

I’m seeing some weird project/environment state on issue details pages: the top Environment dropdown is showing environments from other projects, even though the issue is only for one project. Also, after I switch projects and the old environment disappears, the URL seems to get rewritten again and the page flickers like another filter update happened. I noticed the “Back to Issues” link can also carry a query string that doesn’t match the filters I’m currently seeing in the app.

## Expected outcomes

- On pages where the global selection header is fixed to a single project, the top Environment dropdown should only offer environments that belong to that fixed project.
- When changing projects causes previously selected environments to become invalid and get cleared automatically, that cleanup should not behave like a user-submitted environment filter update: it should not cause an extra URL rewrite or extra filter refresh/flicker.
- The “Back to Issues” link on issue details pages should preserve the query string from the current routed location, so its filters match what the app is currently showing.

## Implementation notes

The specific component boundaries, state plumbing, and validation location are up to the implementation. Prefer preserving existing user-facing behavior except for the incorrect project/environment scoping, automatic cleanup side effects, and stale Back to Issues query behavior described above.
