# Problem Statement

I’m seeing OAuth app revocation leave stuff behind: I deauthorized an OAuth 2.0 app in Account Settings, but existing tokens/sessions for that app and user can still be used afterward. I also found old OAuth tokens after an upgrade for apps that don’t show up as authorized anywhere anymore, and those sessions are still valid.

# Expected outcomes

- **OAuth app deauthorization cleanup**
  - When a user deauthorizes an OAuth 2.0 app, authorization artifacts that were previously issued for that specific user/app pairing should no longer be usable to continue the OAuth flow or create/use sessions for that app.
  - Existing OAuth tokens or sessions for that deauthorized app and user should no longer remain valid after deauthorization.
  - Deauthorizing one app for one user must not invalidate authorization artifacts, tokens, or sessions for other users or other OAuth apps.

- **Upgrade cleanup for orphaned OAuth data**
  - During a normal repository upgrade, OAuth tokens for apps that are no longer authorized by that user should no longer remain valid.
  - Sessions associated with those stale OAuth tokens should also no longer remain valid.
  - OAuth tokens and sessions for apps that are still authorized by the relevant user should be preserved.

- **Failure handling**
  - If deauthorization cannot invalidate the OAuth authorization artifacts for the user/app pairing, the deauthorization request should fail rather than silently leaving stale authorization data behind.
  - The user-visible/localized error text for that failure should be `Unable to remove oauth data.`

- **Migration rollback behavior**
  - Because the upgrade cleanup removes stale OAuth token/session data, rolling back that migration should not recreate deleted OAuth access tokens or sessions.

# Implementation notes

- The exact data access structure, helper functions, and cleanup location are up to the implementer, as long as the externally observable OAuth deauthorization and upgrade behaviors above are satisfied.
- Keep existing OAuth behavior unchanged for authorized apps, unrelated users, and unrelated sessions.
- The upgrade behavior should work for the repository’s supported SQL database backends during the normal upgrade path.
