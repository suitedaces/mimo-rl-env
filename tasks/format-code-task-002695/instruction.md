# Problem Statement

I hit a confusing issue with a DefraDB view schema where two view result types both declare relation fields pointing at each other: the schema processing accepts it, but queries involving those relations later behave oddly, and there’s no error pointing to the specific field/type that caused it.

# Expected outcomes

- View schemas must reject relation definitions between view result types when the relation is declared on both participating view schemas instead of only one side.
- Schema processing for such an invalid view schema must fail immediately, before the schema is accepted for later querying.
- The failure must be reported as a schema-processing error using DefraDB’s existing structured error conventions.
- The error text must be `relations in views must only be defined on one schema`.
- The error must identify the offending relation field and the target view type using the structured metadata keys `Field` and `Type`.

# Implementation notes

- The specific validation location, helper shape, and data structures are up to the implementer.
- The fix should preserve valid one-sided view relations and existing non-view relation validation behavior.
- The implementation should report the invalid schema through the existing schema-processing error flow rather than allowing the schema to be accepted and fail later during query execution.
