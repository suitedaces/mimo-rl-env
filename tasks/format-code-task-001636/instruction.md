## Problem Statement

我有个实体里带了 many-to-many 关系，跑 jhipster 之后生成的 liquibase fake-data CSV 里居然把那个 join 列也塞进去了，导入的时候直接报错，因为 m2m 明明是走 join table 的，单表 csv 里根本不该出现这一列啊。能不能让生成的实体 csv 自动把这种 collection 关系跳掉？

## Expected outcomes

- Liquibase fake-data CSV generation should only emit relationship columns that are actually represented as columns on that entity’s own table.
- Collection-style relationships, including many-to-many relationships whose data is represented outside the entity row, should not appear in that entity CSV’s header or data rows.
- Required singular relationships that are stored as columns on the entity table should continue to appear in the entity fake-data CSV as before.
- Generated CSV files should remain structurally valid: each data row should match the emitted header columns.

## Implementation notes

- Keep the fix focused on externally observable generation behavior; the specific internal organization, helper structure, and filtering location are up to the implementation.
- Do not remove or regress existing fake-data handling for normal scalar fields, content-type columns, or required relationships that are actually stored on the entity table.
- Avoid adding entity-table CSV columns for relationship data that belongs in join-table or other non-entity-row artifacts.
