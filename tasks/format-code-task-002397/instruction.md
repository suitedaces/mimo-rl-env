## `request.user` is resolved from the *unauthenticated* userid

While reading through `warehouse/accounts/__init__.py` I noticed that the
`request.user` request method is implemented like this:

```python
def _user(request):
    login_service = request.find_service(ILoginService)
    return login_service.get_user(request.unauthenticated_userid)
```

This looks wrong from a security standpoint. `unauthenticated_userid`
returns whatever userid the session claims to be, **without** going through
the authentication policy's callback (`_authenticate` in the same file,
which is what actually checks that the user exists / is valid / etc.).

In other words, if a session somehow carries a userid that fails the
authenticate callback (deleted user, invalidated session, tampered
cookie, …), `request.user` will still happily return a `User` object for
that id. Anywhere in the codebase that gates behavior on `request.user`
being truthy is then trusting an identity that the auth policy itself
rejected.

I'd expect `request.user` to reflect the *authenticated* identity only —
i.e. if the request isn't authenticated, `request.user` should be `None`,
and otherwise it should correspond to the same user that the rest of
Pyramid's auth machinery sees.

Could `_user` be reworked so it's based on the authenticated identity
instead?
