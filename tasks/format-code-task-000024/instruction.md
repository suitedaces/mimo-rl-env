## Problem Statement

我在用 create-market 表单建分类市场（categorical），发现校验有点漏。比如我两个 outcome 填了一模一样的答案，它居然能过；还有我把某个 outcome 留空，它也不一定报错，就这么放过去了。感觉像是分类答案那块的校验没盖全。最好能让重复的、空的答案都老老实实报出来，别让我糊里糊涂就提交了。

## Expected outcomes

- Blank categorical market outcomes are reported with the user-facing error message `Answer cannot be blank`.
- Categorical market outcomes with the same case-sensitive value are reported with the user-facing error message `Category must be unique` for each submitted answer involved in the duplication.
- The categorical-outcome error output lets callers associate each reported error with the submitted answer that caused it, without reordering or losing the submitted outcome positions.
- Missing or empty categorical-outcome input is treated as having no categorical outcome errors.
- The create-market form’s categorical step runs categorical-outcome validation whenever categorical outcomes are present in form state.

## Implementation notes

The exact module organization, helper functions, and placement of validation logic are up to the implementer. Preserve the existing create-market form validation style and public user-facing messages, but avoid relying on any particular internal file layout or refactor path.
