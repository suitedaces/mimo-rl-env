# Problem Statement

I'm using Platformatic with a table that has a `json` column, and the generated GraphQL schema shows that field as `String`; the OpenAPI schema also lists it as a string. When I query it, the value is treated like a string even though I'm storing a JSON object there, so I'm not sure if I've modeled the column wrong or if the generator is losing the JSON type.

# Expected outcomes

- GraphQL generation:
  - A database column declared with SQL type `json` should not be exposed as a GraphQL `String`.
  - The generated GraphQL API should expose that column as a JSON object-capable scalar, so querying the field can return structured JSON object values rather than stringifying them.

- REST/OpenAPI and JSON Schema generation:
  - A database column declared with SQL type `json` should not be described as a string property.
  - The generated schema for that field should describe an object value that permits arbitrary properties.
  - Existing nullable handling for nullable columns should continue to apply to `json` columns.

# Implementation notes

- The specific implementation approach, dependency choices, and location of the type mapping logic are up to the implementer.
- Preserve existing behavior for non-`json` SQL column types.
