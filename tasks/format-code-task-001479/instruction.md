# Problem Statement

我现在用 `hass-cli entity list` 查实体时一次出来太多了，想直接按 `entity_id` 用个正则之类的条件筛一下，比如只看某类 sensor。另外 `entity get`、`entity history` 的 table 输出跟 list 不太一致，我来回看很别扭；能不能把这些 entity 表格统一一下，顺便把状态最后变更时间也显示出来？

# Expected outcomes

- `hass-cli entity list` should accept an optional `entityfilter` argument. When provided, the command should treat it as a regular expression and only include entities whose `entity_id` matches it.
- Running `hass-cli entity list` without a filter should continue to list all entities.
- Entity table output should include a `CHANGED` column populated from each entity state’s `last_changed` value.
- Table output for `hass-cli --output table entity list`, `hass-cli --output table entity get <entity>`, and `hass-cli --output table entity history <entity>` should use the same entity-oriented columns: `ENTITY`, `DESCRIPTION`, `STATE`, and `CHANGED`.

# Implementation notes

- The exact internal structure, helper functions, and validation locations are up to the implementer.
- Preserve existing non-table output behavior unless it must naturally include the same entity data.
- The filtering behavior should be observable through the existing CLI command flow rather than requiring callers to use a new internal API.
