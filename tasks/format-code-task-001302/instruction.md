## Problem Statement

我这边用 `database.NewPaginator` 分页一个带 `Preload` 关联的 GORM 查询时，列表数据本身能查出来，但分页的 total/page 会不对，有时候还会报错。能不能让这种带 `Preload` 的分页也正常算总数？

## Expected Outcomes

- 使用 `database.NewPaginator` 对已配置 GORM `Preload` 的查询分页时，分页器应能按原查询条件正确计算总记录数与最大页数。
- 带 `Preload` 的分页查询不应因为关联预加载而在分页统计阶段失败。
- 修复不应破坏实际列表查询：原查询请求预加载的关联数据仍应随分页结果正常加载。

## Implementation Notes

请保持现有公开 API 与调用方式兼容，避免要求调用者为带关联预加载的分页场景额外改写查询。
