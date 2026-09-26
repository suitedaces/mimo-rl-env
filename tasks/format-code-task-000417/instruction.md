## DAGs are being deactivated after upgrade even though they are still parsed and present

After upgrading Airflow, several of my DAGs unexpectedly turned **inactive** in the UI. They no longer show up in the active list, can't be triggered, and look like they were removed — but the DAG files are still right where they always were and the DAG processor is still happily parsing them on every loop.

### Setup

In my deployment, not all DAG files live directly under the `dags_folder` configured in `airflow.cfg`. Some of them are loaded from paths outside that directory — this is a legitimate setup for me (multiple sources of DAGs / a custom layout where the scheduler's DAG processor sees DAGs whose `fileloc` is not nested under the main `dags_folder` path). This worked fine on previous versions.

### What I see

After the upgrade:

- The DAGs whose file path is **not** under the configured `dags_folder` get marked stale and deactivated, basically right after the scheduler starts.
- In the scheduler logs I see lines like:

  ```
  DAG <dag_id> is missing and will be deactivated.
  ```

  for every one of these DAGs, even though the file is clearly still there and is being successfully parsed (no import errors, `last_parsed_time` keeps advancing).

- DAGs whose file path **is** under the main `dags_folder` are unaffected — only the "outside" ones get killed.

### What I expected

A DAG should only be considered stale / be deactivated when it has actually disappeared (the file is gone, or it's no longer being parsed within the stale threshold). As long as the DAG processor is still parsing the file successfully, the DAG should stay active — regardless of whether `fileloc` happens to live under the main `dags_folder` path or somewhere else.

The previous behavior (only deactivating DAGs that are genuinely missing / no longer parsed in time) is what I need back. Right now this effectively breaks any setup where DAGs come from more than one root directory.
