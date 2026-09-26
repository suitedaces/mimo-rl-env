## Allow using stdlib `ssl.SSLContext` with the built-in dev server

I'm using Werkzeug's built-in dev server to do local HTTPS testing (debugging an OAuth redirect flow that requires `https://`). Since I'm on Python 3 (also tried 2.7.9), the standard library already ships a perfectly usable `ssl` module, so I'd rather configure the context with that than pull in pyOpenSSL just for local development.

Following the "Loading Contexts by Hand" example in the docs, I wrote the stdlib-equivalent version:

```python
import ssl
from werkzeug.serving import run_simple

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('ssl.cert', 'ssl.key')

run_simple('localhost', 4000, app, ssl_context=ctx)
```

This doesn't work — the server fails to start handling HTTPS connections. As far as I can tell from the docs, `ssl_context` only really supports a pyOpenSSL context object, a `(cert_file, pkey_file)` tuple, or the `'adhoc'` string, so passing an `ssl.SSLContext` isn't a documented option today.

It would be really nice if `run_simple`'s `ssl_context` accepted a stdlib `ssl.SSLContext` directly, given that the stdlib `ssl` module has been good enough for this kind of thing since 2.7.9 / 3.x. Beyond just the convenience, it would also mean I don't need pyOpenSSL installed at all in the common "I have my own cert + key" workflow — I only really need a third-party crypto lib if I want Werkzeug to generate a throwaway certificate for me (`ssl_context='adhoc'` and friends).

The tuple form and `'adhoc'` should of course keep working as before; this is just about adding `ssl.SSLContext` as a first-class option and treating pyOpenSSL as optional when it's not actually needed.
