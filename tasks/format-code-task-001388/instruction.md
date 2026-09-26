AzureMonitor: configuration editor should be disabled for readonly datasource
**What would you like to be added**:

When opening configuration editor for provisioned read-only Azure Monitor datasource, the controls are still editable.
`DataSourceJsonData` has `readOnly` property which needs to be respected.

Also, because all controls are editable, it's possible to save the read-only datasource by clicking on **Load Subscriptions**.
