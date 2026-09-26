### Apache Airflow Provider(s)

common-sql

### What happened

Two unrelated annoyances around `DbApiHook` that I hit on the same DAG.

**1. `hook.placeholder` re-queries the metadata DB on every access**

I have a Postgres-backed custom hook subclassing `DbApiHook`, and a task that inserts a lot of rows via `insert_rows`. While poking at why the task is slower than I expected and why I see so much load on my Airflow metadata DB, I noticed the `placeholder` property goes through `get_connection(...)` every single time it's read. Since the insert path reads it per row to build the SQL template, every inserted row triggers a metadata DB roundtrip just to read the connection back. For a task pushing tens of thousands of rows this is very noticeable.

The connection itself isn't changing during a task — reading it once per hook instance should be enough.

**2. Warning about an invalid placeholder in `extra` is unhelpful**

In a different Connection I tried to override the placeholder via the `extra` field, e.g.

```json
{ "placeholder": ":1" }
```

which isn't in the supported set, so it's (correctly) ignored. But the warning I get in the task log looks roughly like:

```
Placeholder defined in Connection 'postgres_conn_id' is not listed in 'DEFAULT_SQL_PLACEHOLDERS' and got ignored. Falling back to the default placeholder '%s'.
```

Two problems with this message:

- `'postgres_conn_id'` here is not my actual connection id — it's the literal name of the attribute on the hook class. So when I went to look up "which of my connections is misconfigured?" I couldn't find one with that id at all and got pretty confused.
- The message never tells me which placeholder value was rejected. If I had several connections / had recently edited extras, I'd want to see that `':1'` was the offending value so I can go fix the right one.

### What you think should happen instead

- Reading `placeholder` on a hook instance shouldn't keep hammering the metadata DB; the connection lookup should only happen once per hook.
- The "invalid placeholder" warning should identify (a) the actual connection id the bad value came from and (b) the bad placeholder value itself, so it's actually actionable.

### Versions of Apache Airflow Providers

apache-airflow-providers-common-sql (current main)

### Deployment

Other

### Anything else

Both are reproducible on any subclass of `DbApiHook` — the slow path just needs a bulk insert, the warning just needs an `extra` with a non-standard `placeholder`.
