RP-initiated Logout with expired django session not revoking the tokens
**Describe the bug**
If there's not active Django session when calling the RP-initiated Logout view with a valid `id_token_hint`, then the tokens won't be revoked. 

Since there's not active session, the code will always prompt a confirmation form : https://github.com/jazzband/django-oauth-toolkit/blob/11294ab5678691fb6bc21ecf917dca3099311a9e/oauth2_provider/views/oidc.py#L234-L237

But in `do_logout()` the code relies on `self.request.user` which is an `AnonymousUser`, therefore no tokens will be revoked : https://github.com/jazzband/django-oauth-toolkit/blob/11294ab5678691fb6bc21ecf917dca3099311a9e/oauth2_provider/views/oidc.py#L364-L368

The app may even crash (it's my case because the User PK is a UuidField, and `"AnonymousUser"` isn't a valid uuid) 


**To Reproduce**

<!-- Steps to reproduce the behavior -->
Have a Django application with django-oauth-toolkit installed
Set `settings.SESSION_COOKIE_AGE=10` (seconds)
Perform an oauth login
Call RP-initiated Logout view passing the retrieved id_token in `id_token_hint` params.

**Expected behavior**
The tokens for the user found with `id_token_hint` should be revoked.

**Version**
master branch on commit https://github.com/jazzband/django-oauth-toolkit/commit/11294ab5678691fb6bc21ecf917dca3099311a9e

<!-- Have you tested with the latest version and/or master branch? -->
<!-- Replace '[ ]' with '[x]' to indicate that. -->
- [ ] I have tested with the latest published release and it's still a problem.
- [x] I have tested with the master branch and it's still a problem.

**Additional context**
<!-- Add any other context about the problem here. -->
