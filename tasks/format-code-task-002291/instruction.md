## Problem Statement

When I set up an MSSQL connection in Falcon, I can fill in the usual host/user/password stuff, but I don’t see any way to increase the connection or query timeout. Some of our SQL Server connections are slow to respond and hit the default timeout, so it would be great if the connection form let me set those timeout values and made the fields a bit clearer about what they mean.

## Expected outcomes

- MSSQL connection configuration exposes editable timeout fields for `connectTimeout` and `requestTimeout` alongside the usual connection settings.
- Timeout values entered for an MSSQL connection are preserved in the connection configuration and passed through when Falcon creates or uses that connection.
- Connection forms show clearer user-facing field information, such as friendly names, helpful hints, and optional explanatory text, so users can understand what each configurable value means.
- Field rendering uses appropriate controls for the kind of value being edited, such as numeric or password-style inputs where applicable, while existing file/path picking behavior continues to work.

## Implementation notes

- The exact data structure used to describe connection fields, and where validation or normalization happens, is up to the implementation.
- The UI and backend changes should remain compatible with existing connection settings and should not require users to configure timeouts for databases that do not support them.
- Existing connection behavior should continue to work unless a user explicitly supplies additional MSSQL timeout values.
