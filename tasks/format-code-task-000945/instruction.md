# Problem Statement

我用 `load_submission` 连续导入同一个 CGAC、同一个 fiscal year 的 Q1 和 Q2 后，发现 Q2 的 `SubmissionAttributes.previous_submission` 还是空的；序列化出来的 `SubmissionAttributes` 里还有个一直为空的 `frec_code`，我有点怀疑是不是这个空值把上一季度关联搞丢了。

# Expected outcomes

- 上一季度关联
  - 使用 `load_submission` 连续加载同一报告序列中的季度 submission 时，后加载的季度应在 `SubmissionAttributes.previous_submission` 中关联到正确的上一期季度 submission。
  - 无关或缺失的可选字段不应导致同一报告序列中的上一期季度 submission 漏链。
  - 不属于同一报告序列的 submission 不应被错误关联为上一期。

- `SubmissionAttributes` 输出字段
  - `SubmissionAttributes` 不应再把 `frec_code` 作为可用字段暴露。
  - 对 `SubmissionAttributes` 的序列化结果不应包含 `frec_code`。

# Implementation notes

- 具体的数据查询方式、校验位置和内部 helper 组织方式由实现者决定。
- 可以通过现有的加载流程、模型层和序列化层实现上述行为；不要保留会让上一期关联或 `SubmissionAttributes` 输出继续表现为上述问题的公开行为。
