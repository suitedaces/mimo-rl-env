### postgres_user.present / postgres_group.present report bogus changes under `test=True`

I'm using `postgres_user.present` (and `postgres_group.present`) to manage a few roles on a PostgreSQL server. When I run a real apply, salt correctly reports the role as already present and does nothing:

```yaml
frank:
  postgres_user.present:
    - login: True
    - createdb: False
```

```
$ salt 'db1' state.sls pg_users
db1:
----------
          ID: frank
    Function: postgres_user.present
      Result: True
     Comment: User frank is already present
     Changes:
```

But if I run the exact same state with `test=True` to do a dry-run, it tells me there's a pending change even though nothing has actually changed on the server:

```
$ salt 'db1' state.sls pg_users test=True
db1:
----------
          ID: frank
    Function: postgres_user.present
      Result: None
     Comment: User frank is set to be updated
     Changes:
```

The role exists, every attribute (`login`, `createdb`, password, ...) already matches what the state declares, and a real run is a no-op — but the test run claims an update is going to happen. That makes `test=True` useless for these states: I can't trust it to tell me what would actually change.

I'd expect `test=True` to mirror the real behavior:

- if the role is already present and all attributes match → "already present", no pending change
- if something would actually be created or updated → report it as pending, and ideally show *what* would change so I can review the diff before applying

Same problem applies to `postgres_group.present`.
