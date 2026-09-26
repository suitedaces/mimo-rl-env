## Problem Statement

When I set `export DYNACONF_THING=True` and then read `settings.THING`, I get the string `"True"` back instead of an actual boolean. Same thing happens with `False`. But if I use lowercase `true`/`false` it correctly comes through as a real bool. Just trying to flag a boolean config value through an env var and it's tripping me up.

## Expected outcomes

- Environment variables whose bare value is `True` should be read by Dynaconf settings as the Python boolean `True`, not as the string `"True"`.
- Environment variables whose bare value is `False` should be read by Dynaconf settings as the Python boolean `False`, not as the string `"False"`.
- Existing behavior for lowercase bare `true` and `false` environment variable values should continue to produce Python booleans.
- The change should apply to bare environment-variable values only; string values embedded inside TOML-style environment data structures should remain strings.
- TOML settings files should continue to follow TOML’s own type rules: quoted `"True"` / `"False"` values remain strings, while TOML booleans remain booleans.
- Users who explicitly request a string value from an environment variable, such as through Dynaconf’s string casting syntax or by supplying a quoted string value, should still receive the original string.

## Implementation notes

- Keep the fix focused on externally visible configuration-loading behavior rather than on any specific helper, module layout, or parsing hook.
- The exact place where environment-variable values are normalized or parsed is up to the implementation, as long as all supported environment-variable loading paths exhibit the expected behavior.
- Do not change TOML file parsing semantics or TOML data-structure semantics while fixing bare environment-variable boolean values.
