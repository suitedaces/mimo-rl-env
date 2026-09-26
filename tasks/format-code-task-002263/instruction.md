I want `SQLSmith` instances to support a stateful schema-loading method `LoadSchema(records [][5]string, indexes map[string][]string)` so callers can teach the generator which databases, tables, columns, column types, and per-table index names exist before generating SQL.

Each record should be interpreted as `[databaseName, tableName, tableType, columnName, columnType]`. For example, after:

`ss := sqlsmith.New(); ss.LoadSchema([][5]string{{"shop", "users", "BASE TABLE", "id", "INT(11)"}, {"shop", "users", "BASE TABLE", "name", "VARCHAR(255)"}, {"shop", "orders", "VIEW", "created_at", "TIMESTAMP"}}, map[string][]string{"users": {"idx_users_name"}})`

`ss.Databases["shop"]` should exist, `ss.Databases["shop"].Tables["users"]` should have table type `BASE TABLE`, indexes `[]string{"idx_users_name"}`, and columns `id` and `name`; the normalized column data types should be `int` and `varchar`. `ss.Databases["shop"].Tables["orders"]` should also exist with table type `VIEW`, column `created_at`, normalized type `timestamp`, and an empty index list when no index entry is supplied.

The method should group multiple records for the same database/table into a single table, add only missing database/table/column entries, and leave existing entries intact when duplicate rows are passed again. Column type normalization should lowercase the supplied type name and strip numeric size suffixes like `(11)`, `(128)`, or `(255)` so later SQL and data generation can choose values by base type. The call mutates only the receiving `SQLSmith` instance's schema registry and returns no value.
