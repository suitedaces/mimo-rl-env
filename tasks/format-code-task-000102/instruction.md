Validate email address format when using automatic IAM authentication
When adding IAM database users to either MySQL or Postgres the user or service account username is formatted in a certain way that differs across database engine types.

This is not necessarily trivial to users when using the connectors, we should try validating and formatting the IAM database usernames within the connectors to remove this burden on users.

**Postgres**: Removes `.gserviceaccount.com` domain suffix if it exists.
**MySQL**: Removes everything after and including the `@` sign. (`test-user@gmail.com` -> `test-user`)

Should already have `databaseVersion` from the API request to https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/connect/get
