# Problem Statement

I'm running TiDB with TiFlash and trying to get queries like `SELECT a FROM t WHERE t.a > 1 OR t.a IN (SELECT a FROM t)` (and the `NOT IN` variant) to run in MPP mode, but EXPLAIN keeps showing a root-level join and I get a warning saying MPP is blocked because `left outer semi join` / `anti left outer semi join` isn't supported. Would be great if these semi-join shapes could just go through TiFlash MPP hash join like the regular joins do, including the cartesian case when I've already turned on `tidb_opt_broadcast_cartesian_join`.

Also, separately — I tried disabling some join types by inserting into `mysql.expr_pushdown_blacklist`, but it doesn't seem to have any effect on the MPP hash join path; the plan still pushes down. Ideally the blacklist would actually gate this too, with a clear warning telling me it was blocked by the blacklist so I know where to look.

# Expected outcomes

- TiFlash MPP planning should allow `left outer semi join` queries produced by `IN`-style predicates to use a TiFlash-side MPP `HashJoin` plan instead of falling back to a TiDB root-level join only because that join type is unsupported.
- TiFlash MPP planning should allow `anti left outer semi join` queries produced by `NOT IN`-style predicates to use a TiFlash-side MPP `HashJoin` plan instead of falling back to a TiDB root-level join only because that join type is unsupported.
- When MPP mode is otherwise enabled and cartesian broadcast joins are allowed through `tidb_opt_broadcast_cartesian_join`, cartesian forms of the same left-outer-semi and anti-left-outer-semi join shapes should also be eligible for TiFlash MPP hash join planning.
- Disabling a join type through `mysql.expr_pushdown_blacklist` should prevent the corresponding TiFlash MPP hash join from being selected, including for the newly supported semi-join shapes.
- When a TiFlash MPP hash join is blocked by `mysql.expr_pushdown_blacklist`, the warning should clearly identify that the join type was blocked by the blacklist and point users to `mysql.expr_pushdown_blacklist`.
- Join types that still are not supported by TiFlash MPP hash join should continue to fall back with the existing “not supported now” style warning; the newly supported left-outer-semi and anti-left-outer-semi shapes should no longer produce that unsupported-join warning.

# Implementation notes

- Choose any implementation that makes the externally observable EXPLAIN plans, warnings, and blacklist behavior match the expected outcomes.
- The exact internal structure, helper functions, and validation locations are up to the implementer, as long as the externally observable EXPLAIN plans, warnings, and blacklist behavior match the expected outcomes.
- Preserve existing MPP behavior for already supported join types unless the blacklist explicitly disables them.
