## `quilt3.admin.sso_config.set(None)` errors out instead of removing SSO config

According to the docs, `quilt3.admin.sso_config.set` takes `Optional[str]`, so I assumed I could pass `None` to clear out the SSO configuration on our stack (mirroring how the catalog UI lets admins remove it).

```python
from quilt3.admin import sso_config

# this works and returns the current config
sso_config.get()

# this is supposed to remove the SSO config
sso_config.set(None)
```

The `get()` call works fine and returns whatever is currently configured. But `set(None)` doesn't return cleanly — it blows up inside the admin client while trying to build the result, even though the mutation on the server side appears to have actually cleared the config (subsequent `get()` calls return `None`).

Passing a non-empty config string to `set(...)` still works as expected and returns the new `SSOConfig`. It's specifically the "remove" path (passing `None`) that's broken from the Python API.

Could `sso_config.set(None)` be made to work as a proper way to remove the SSO configuration, and return something sensible (e.g. `None`) in that case? It would also be nice to have the type signature and docstring reflect that removal is a supported use of this function.
