### STORAGES fixer clobbers inherited storages when settings are split across modules

I have a typical split settings layout:

```
example/
    settings/
        base.py
        production.py
```

`base.py` defines a custom `DEFAULT_FILE_STORAGE` (and also a `STATICFILES_STORAGE`). `production.py` inherits from it via a star-import and then overrides just one of them:

```python
# example/settings/production.py
from example.settings.base import *

DEFAULT_FILE_STORAGE = "example.storages.S3Storage"
```

When I run django-upgrade with `--target-version 4.2` over both files, `base.py` gets rewritten nicely into a combined `STORAGES = {...}` dict with both `"default"` and `"staticfiles"` keys — great.

But `production.py` gets rewritten to:

```python
from example.settings.base import *

STORAGES = {
    "default": {
        "BACKEND": "example.storages.S3Storage",
    },
}
```

That's a regression in behavior. Before the rewrite, `production.py` was inheriting `STATICFILES_STORAGE` (and anything else storage-related) from `base.py` via the star-import and only overriding the default file storage. After the rewrite, `production.py` defines a fresh `STORAGES` dict with only `"default"` in it, which fully replaces the inherited dict — so the `"staticfiles"` entry from `base.py` is silently dropped at runtime.

It would be nice if the fixer recognized that the module is pulling settings in via `from ...settings... import *` and produced something that extends the inherited dict instead of replacing it, so the override semantics are preserved.
