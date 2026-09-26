## Scheduled queries: no way to pass task arguments

I'm setting up a scheduled query in this repo and the corresponding Airflow task on the telemetry-airflow side needs a couple of extra command-line arguments to run correctly (similar to what's described in mozilla/telemetry-airflow#1013).

I tried adding the arguments under the `scheduling` block in the query's `metadata.yaml`, regenerated the DAG, and the generated Airflow DAG file doesn't carry them through to the task at all — the task definition looks exactly the same as before. As far as I can tell there's just no supported way today to declare per-task arguments from the query's scheduling metadata.

It would be great if the scheduling config let me list out the arguments I want passed to a task, and the generated DAG actually forwarded them to the task so they're available at execution time. Tasks that don't need any arguments should keep generating the same output they do today.
