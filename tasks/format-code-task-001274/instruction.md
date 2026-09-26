## "Create a team" button shown in project creation for users who can't create teams

In the project creation flow, there's a "+" button next to the team selector that opens the "Create a team" modal. Now that team admins can also reach the project creation flow, they see this button as well — but team admins don't have permission to create teams in the org (only org owners/managers can do that).

The "Create a team" button shouldn't be shown to users who don't have permission to create teams in the first place. It should only appear for users who can actually go through with creating a new team.

Before:
![current behavior — team admins see the create team button](https://github.com/getsentry/sentry/assets/132939361/857b893c-903f-43a7-98a3-728bed6aaadd)
