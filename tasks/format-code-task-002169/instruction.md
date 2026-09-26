## Problem Statement

我现在想在 GraphQL 里快速拿到某个分支 diff 里到底哪些节点变了，但只能拉完整 diff 再自己折叠，太重了。能不能加个轻量的 diff summary，直接给我变更节点概览，并且可以按时间范围、只看当前 branch 之类的条件缩一下范围？另外有些节点本身没改属性、只是关系变了，也希望摘要里能看出来它算是更新过。

## Expected outcomes

- Diff summary API
  - GraphQL 查询根应提供 `DiffSummary` 字段，用于返回当前分支 diff 中按节点汇总后的变更概览。
  - `DiffSummary` 的每个结果条目应包含 `branch`、`node`、`kind`、`actions` 字段，分别表示变更所在分支、节点 ID、节点 kind 和该节点关联的动作列表。
  - `actions` 应以调用方可直接消费的字符串列表形式返回，并能表达同一节点在 diff 中涉及的一个或多个动作。

- Filtering
  - `DiffSummary` 应接受可选的 `time_from`、`time_to` 和 `branch_only` 参数，用于限定摘要所覆盖的 diff 范围；在 GraphQL schema 中这些参数应按仓库既有 GraphQL 参数命名约定暴露。
  - 未显式传入 `branch_only` 时，应按默认包含完整 diff 范围的方式处理，而不是只返回当前 branch 的变更。

- Relationship-only changes
  - 如果某个节点本身没有直接属性或节点级变更，但参与的 relationship 发生了变化，该节点也应出现在 `DiffSummary` 结果中。
  - 仅因 relationship 变化而出现在摘要中的节点，其 `actions` 应体现为已更新。

## Implementation notes

具体的汇总数据结构、去重方式、过滤参数传递位置以及 GraphQL resolver 的组织方式由实现者决定。实现应保持现有完整 diff 查询能力不被破坏，并通过公开 GraphQL 行为体现新增摘要能力。
