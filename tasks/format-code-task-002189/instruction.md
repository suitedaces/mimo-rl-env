# Configurable identity matching for sign-in

We're laying the groundwork for passwordless / unified sign-in, where a user types a
single "identity" value (an email, a phone number, a username, ...) into one field and
we have to figure out *which* user attribute that value corresponds to before we can
look the user up.

Today the only thing we have is `SECURITY_USER_IDENTITY_ATTRIBUTES`, a flat list of the
attributes an identity may match. That's not enough: different attributes need different
recognition logic (an email looks nothing like a phone number), and the order in which we
try them matters.

Please add a configurable, ordered identity-matching mechanism.

## What to add

**Mapper helpers.** Provide two reusable matcher functions, importable from the top-level
`flask_security` package as `uia_email_mapper` and `uia_phone_mapper`:

- `uia_email_mapper`: given a candidate string, returns that string unchanged when it is a
  syntactically valid email address, and `None` otherwise.
- `uia_phone_mapper`: given a candidate string, returns that string unchanged when it looks
  like a phone number (e.g. `555-555-5555`, `(555) 555-5555`, `+1-555-555-5555`,
  `5555555555`), and `None` otherwise.

Each matcher takes a single string argument.

**A new configuration value** `SECURITY_USER_IDENTITY_MAPPINGS` that defines, *in order*, how a
submitted identity is matched to a user attribute. It is a list of single-entry dicts, each
pairing an attribute name with a matcher callable, e.g.

```python
[
    {"email": uia_email_mapper},
    {"us_phone_number": uia_phone_mapper},
]
```

Its default must recognize email addresses out of the box (mapping the `email` attribute to
`uia_email_mapper`). The configured callables must remain real callables once the extension is
initialized.

**A resolution helper** `get_identity_lookup`, importable from the top-level `flask_security`
package, that takes a submitted identity string (and optionally an explicit app as a second
argument) and returns the attribute/value pair to use when looking up the user. Concretely it
returns a dict of the form `{attribute: value}` — suitable for passing straight to a datastore
`find_user(**result)` call — or `None` when the identity matches nothing.

Resolution rules:

- Evaluate the configured mappings **in their configured order**.
- Only consider a mapping whose attribute is **also enabled** in
  `SECURITY_USER_IDENTITY_ATTRIBUTES`; mappings for non-enabled attributes are skipped entirely,
  even if their matcher would have matched.
- For the first eligible mapping whose matcher returns a non-`None` value, return
  `{attribute: <that returned value>}`. The value is exactly what the matcher returned (no extra
  normalization on top).
- If no eligible mapping matches, return `None`.
