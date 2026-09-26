Add bulk "clear" to Browse -> DAG Runs UI
**Description**

Airflow DAG Run UI (Browse -> DAG Runs) is really useful for managing many DAG Runs, creating specific DAG Runs and so on.
It would be great to have an additional option to "With Selected DAG Runs" -> "Clear" to reset all task instances under those DAG Runs.

**Use case / motivation**

When rerunning DAGs especially during development cycles it is tedious to go into the Tree view and clear many DAG Runs manually. It would be great to have some way to do this in bulk / over a range of DAG Runs. 

The DAG Run UI seems like a good place to add this since it is already a kind of administrative area over all the DAG Runs and has "with selected" options like "delete", "mark failed", etc. Discussion welcome :)

**Related Issues**
None
