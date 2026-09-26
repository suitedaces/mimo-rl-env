## Process topology contains empty-string fields

When I look at the process data Scope reports, I notice that some processes have metadata entries whose values are just empty strings. For example, certain kernel threads or very short-lived processes don't have a cmdline (or other fields) available from `/proc`, but Scope still emits those keys in the node's metadata with `""` as the value.

These empty entries don't carry any information — they just clutter the report and the UI. If a field has no value for a given process, the reporter shouldn't include that key at all (rather than including it with an empty string).

Could the process reporter be updated so that fields without a value are simply omitted from the reported metadata?
