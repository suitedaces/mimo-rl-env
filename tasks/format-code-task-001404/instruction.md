## Feature request: a direct way to tell `get_context` which mode I want

Right now `gx.get_context(...)` figures out what kind of `DataContext`
to give me by inspecting a combination of arguments (`project_config`,
`context_root_dir`, `cloud_mode`, `cloud_access_token`, ...) plus
environment variables. That works, but for a lot of my use cases it
feels indirect and a bit fragile.

### What I'm trying to do

In our test suite and in some notebooks I just want a plain in-memory
context — nothing on disk, nothing talking to GX Cloud. The most
intuitive thing to write would be something like "give me an ephemeral
context, please", but `get_context` doesn't really expose that as a
first-class choice. I have to know which combination of flags happens
to produce an `EphemeralDataContext` rather than a `FileDataContext` or
`CloudDataContext`, and that's not obvious from the signature or the
docs.

### Why the current behavior bites us

Because `get_context` falls back to environment variables when args are
ambiguous, I've hit cases where I *think* I'm asking for one kind of
context and silently get back another. Concrete example:

```python
import great_expectations as gx

# On a CI runner where GX_CLOUD_* vars happen to be set in the
# environment (leaked from another job, set globally, whatever)…
ctx = gx.get_context(cloud_mode=False)
# I expected something local / in-memory, but depending on the
# combination of env vars and other defaults, what I get back is
# not always what I wanted, and there is no signal telling me so.
```

The frustrating part isn't just that the wrong type comes back — it's
that there's no feedback. The call just returns *something*, and the
mismatch only surfaces later when some method behaves differently than
I expected, or when isinstance checks in downstream code fail.

### What I'd like

A way to tell `get_context` directly which of the three kinds of
context I want (in-memory / file-backed / cloud), without having to
reason about which combination of existing flags maps to which class.
Something I can write once in a CI script or notebook and trust to do
the same thing regardless of what environment variables happen to be
set on the machine.

And — importantly — if I ask for one kind and for whatever reason the
machinery can't actually give me that kind, I'd much rather get a loud,
explicit error at the `get_context` call site than silently receive a
different `DataContext` subclass.

The existing arg-driven / env-driven behavior should keep working as it
does today for callers that don't opt in to the new explicit choice;
this is purely about giving users a clearer entry point when they know
exactly what they want.

The shape I'd expect at the call site is something like
`gx.get_context(mode=...)`, where the mode value is one of the three
strings `"ephemeral"`, `"file"`, `"cloud"`.
