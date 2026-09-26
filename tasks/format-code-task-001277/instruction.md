## Feature request: ability to disable "invite member" per organization

We run Sentry and we'd like to be able to turn off the "invite a new member" capability for specific organizations. Right now there's no way to do this — any user with the relevant member-management scopes on an org can hit the org members endpoint (or use the "Add Member" UI under organization settings) and send invitations, and we have no switch to gate that on a per-org basis.

Our use case: depending on the plan / state of an organization we want to be able to centrally say "this org cannot invite new members right now" without having to mess with each member's role or scopes. It'd fit naturally as one of the existing organization-level toggles that can be flipped on or off per organization.

When invites are disabled for an org, we'd expect:

- Hitting the create-member API for that org should fail rather than silently going through and sending an invite email. The response should be something the frontend can distinguish from the existing "user already exists" / "invalid role" / validation errors, so it can show an appropriate "you aren't allowed to invite members" message instead of a generic failure.
- The "Add Member" page in the UI should surface that failure as a user-visible error, not just leave the form spinning or log an unknown-error to Raven.

By default, existing organizations should keep working exactly as they do today (i.e. invites stay enabled unless we explicitly turn the toggle off for an org), so this shouldn't be a breaking change for current installs.

For wiring, I'd expect a new org-level feature flag along the lines of `organizations:invite-members` (default on) gating the create-member endpoint, with a dedicated HTTP 401 response when it's off so the frontend can branch on that status specifically.
