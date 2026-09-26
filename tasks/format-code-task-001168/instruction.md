MLflow's table artifact API currently always appends when the same artifact path is logged again. That is convenient for incremental evaluation results, but callers also need deterministic ways to replace a stale table or refuse to touch an existing one. Please add an optional `mode` parameter to both the fluent `mlflow.log_table` API and `MlflowClient.log_table`. It must accept exactly `"append"`, `"overwrite"`, and `"error_if_exists"`, with `"append"` as the default so existing callers keep their current behavior.

The modes should have these persisted behaviors:

- `append`: create the table when the artifact does not exist. When it does exist, append the incoming rows after the stored rows. Appending is allowed when the incoming table has the same set of columns even if their order differs; align the incoming data to the stored column order before writing. If any stored column is missing or any new column is present, reject the write instead of silently introducing null-filled schema drift.
- `overwrite`: create the table when absent; otherwise replace all stored rows and the old schema with the incoming table.
- `error_if_exists`: create the table when absent; otherwise raise without changing it.

An unsupported mode, an append with missing columns, or an append with extra columns must raise `MlflowException` with the `INVALID_PARAMETER_VALUE` error code. These validation failures must be non-mutating: the previously persisted artifact contents and its `mlflow.loggedArtifacts` tag stay unchanged, and an invalid mode on a fresh path must not create either an artifact or a table tag.

Keep the existing data compatibility: dictionaries and pandas DataFrames remain accepted for every mode, nested run-relative artifact paths continue to work, and successful writes register the existing `{"path": ..., "type": "table"}` metadata. Repeated appends and overwrites of the same path must leave exactly one such metadata entry rather than duplicating it.
