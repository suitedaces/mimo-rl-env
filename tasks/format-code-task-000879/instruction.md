## Lose original request URL when using `redirect=` in `@requires`

I'm using the `requires` decorator with the `redirect` kwarg to send unauthenticated users to my login page:

```python
from starlette.authentication import requires

@requires('authenticated', redirect='login')
async def admin(request):
    ...

async def login(request):
    ...
```

The redirect itself works fine — when a user hits `/admin` without being authenticated, they end up at `/login`. The problem is that inside my `login` handler I have no way to know **where the user was originally trying to go**. I want this so I can send the user back to the page they originally requested after they successfully log in (this is a pretty standard login flow — Django's `login_required` does it via a `next` query param, for example).

Right now the decorator just builds the redirect URL from `request.url_for(redirect)` and that's it — no information about the originating URL is carried along to the login handler. So in my `login` handler, `request.query_params` is empty and `request.headers["referer"]` isn't reliable either.

Could `requires` pass the original request URL through to the redirect target somehow, so the receiving handler can read it off the request and redirect back after auth? Something along these lines on the user side:

```python
async def login(request):
    if request.method == "POST" and request.user.is_authenticated:
        original = ...  # would like to read this off the request
        if original:
            return RedirectResponse(original)
        return RedirectResponse("/")
```

Without this I have to write my own decorator that wraps the same logic just to preserve the original URL, which seems like something `requires` itself should support given it already owns the redirect.
