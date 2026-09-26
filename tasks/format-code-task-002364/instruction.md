# Problem Statement

我用 postgresql_psql 跑一段建表的 SQL，但 manifest 里没写 refreshonly 这个参数，结果 puppet apply 的时候那条命令压根没执行，resource 直接显示成已经是最新状态了。我盯着看了好几次，只有在我给它配了 notify 触发 refresh 的时候才会真正跑。我没加任何 unless 条件，按说普通 apply 就该直接执行才对，搞不懂是不是这个 refreshonly 默认值的问题。

# Expected outcomes

- For `postgresql_psql`, omitting `refreshonly` should behave the same as setting `refreshonly => false`: on a normal non-refresh run, with no `unless` guard preventing execution, the SQL command should be applied rather than being treated as refresh-only.
- For `postgresql_psql`, explicitly setting `refreshonly => true` should continue to defer execution until the resource receives a refresh event; a plain apply without a refresh should not execute the SQL.
- The `refreshonly` parameter should accept only boolean true/false values in the forms supported by the Puppet type, and invalid values should be rejected during resource validation.

# Implementation notes

- Preserve the documented semantics of `postgresql_psql` while fixing the default behavior of `refreshonly`.
- The exact internal representation, validation location, and provider/type coordination are implementation details; choose an approach that makes the public resource behavior correct and consistent.
