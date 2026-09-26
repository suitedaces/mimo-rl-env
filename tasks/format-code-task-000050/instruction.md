# Add a scoped configuration system for cogs

Red's cogs currently have no consistent way to declare the settings they use or
to read and write those settings at different scopes (the bot as a whole, a
particular guild, a channel, a role, a user, or a specific member of a guild).
We want a small configuration subsystem that gives every cog a single object to
work with.

Add a `Config` class, importable as `from core.config import Config`, with the
behaviour described below.

## Obtaining a config object

`Config.get_conf(cog_name, unique_identifier=0, force_registration=False)`
returns a fresh config object for a cog. `cog_name` is a string; the other two
arguments are keyword options. `force_registration` controls the strict mode
described further down and defaults to `False`.

## Registering defaults

A cog declares the keys it uses, per scope, by registering defaults:

- `register_global(**defaults)`
- `register_guild(**defaults)`
- `register_channel(**defaults)`
- `register_role(**defaults)`
- `register_user(**defaults)`
- `register_member(**defaults)`

Each call records the given keys together with their default values for that
scope. Calling a register method more than once merges the new keys with the
ones already registered for that scope (later calls override earlier defaults
for the same key). Defaults for one scope are independent from every other
scope.

## Reading and writing values

The config object itself represents the **global** scope. To work with another
scope you ask for it by id:

- `config.guild(guild_id)`
- `config.channel(channel_id)`
- `config.role(role_id)`
- `config.user(user_id)`
- `config.member(guild_id, member_id)`

An id may be given either as an integer or as an object that exposes an `id`
attribute (the object's `id` is used). Each of these returns a scoped view of
the configuration.

Reading a value is done by calling the key as a method on the relevant scope.
On the global scope `config.foo()` returns the value of `foo`; on another scope
`config.guild(123).foo()` returns the value of `foo` for guild `123`. If no
value has been stored for that key in that scope, the registered default for the
scope is returned. If the key was never registered (and strict mode is off), the
reader returns `None`.

Writing a value is asynchronous: `await scope.set(key, value)` stores `value`
for `key` in that scope, e.g. `await config.set("foo", 1)` for the global scope
or `await config.guild(123).set("foo", 1)` for a guild. After a value has been
set, reading the same key in the same scope returns the stored value.

`await scope.clear()` removes every stored value for that exact scope, so
subsequent reads fall back to the registered defaults again.

## Scope isolation

Scopes and individual ids are fully isolated. Storing a value for one guild must
not change what another guild, the global scope, or any other scope reports.
Members are identified by the pair `(guild_id, member_id)`, so the same member
id under two different guilds is two distinct scopes.

## Strict mode

When a config object is created with `force_registration=True`, reading or
writing a key that has not been registered for the scope being used raises
`AttributeError`. When `force_registration` is `False` (the default), reading an
unregistered key returns `None` and writing an unregistered key is allowed.
