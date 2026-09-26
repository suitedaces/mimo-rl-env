## Passing a non-google-auth credentials object to `Client` fails with a confusing error much later

I recently upgraded `google-cloud` and started passing my existing
credentials object (created the way I used to with `oauth2client`) into
`google.cloud.client.Client`. The constructor accepts it without
complaint, but then later when the client actually tries to make a
request I get a confusing failure deep inside the connection / transport
code that doesn't make it at all obvious that the real problem is my
credentials object being the wrong type.

Roughly what I'm doing:

```python
from google.cloud.client import Client

# `creds` here is *not* a google.auth.credentials.Credentials instance
# (it's left over from how I used to construct credentials before).
client = Client(credentials=creds)   # silently accepted

# ... later, the first real API call blows up somewhere internal
# with a message that has nothing to do with credentials.
```

Since this library now standardises on `google-auth`, and only
`google.auth.credentials.Credentials` instances are actually supported,
it would be much friendlier if `Client` rejected unsupported credential
objects up front at construction time, with a clear message pointing the
user at the google-auth-based authentication docs. As it is now, the
error surfaces far away from the actual mistake and is very hard to
diagnose.

Passing `credentials=None` (i.e. relying on the default credentials
discovery) should of course continue to work as before.
