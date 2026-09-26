## Problem Statement

我这边用 `tier phases <org>` 查一些没有 schedule 的 Stripe subscription，发现 trial 已经过了、Stripe 状态也不是 `trialing` 了，但返回的 phase 里 trial 还像当前阶段一样；另外有个已经在 Stripe 里 canceled、只有 `canceled_at` 的订阅，phase 列表里也看不到对应取消时间的空功能结束阶段。

## Expected outcomes

- For subscriptions without schedules, elapsed trials should no longer be reported as the current phase once Stripe no longer considers the subscription to be in trial.
- Active trials should continue to be represented as the current trial phase.
- After a trial has elapsed, the returned phases should identify the post-trial subscription phase as current when the subscription is not already ended.
- When Stripe reports that a subscription has actually been canceled, the returned phases should include an ending phase at the reported cancellation time with no features, and the current phase should reflect the ended state.
- Existing scheduled-cancellation behavior for subscriptions that have not yet actually been canceled should continue to work.

## Implementation notes

- Preserve the existing public behavior and output shape of `tier phases <org>` and the equivalent SDK phase lookup except for the corrected phase timing and current/trial flags above.
- The internal data flow, helper structure, and validation location are up to the implementer.
