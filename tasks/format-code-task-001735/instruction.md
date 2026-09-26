## Problem Statement

我们有个监控脚本会去读 VPA 的 status.conditions 判断它到底有没有在工作。现在遇到个尴尬的情况：有时候 VPA 的 selector 写错了或者 label 飘了，匹配不到任何 pod，这种 VPA 看上去就一直没有 recommendation，但 status 上啥也看不出来，跟"还在算"完全分不清。能不能让 recommender 在这种没匹配到 pod 的情况下，在 conditions 里明确标一下原因？最好 RecommendationProvided=False 的时候也能带上对应的 reason/message，这样我外部一眼就能看出来是 selector 没选中东西，而不是别的问题。

## Expected outcomes

- 对于 selector 当前匹配不到任何 live pod 的 VPA，recommender 更新后应在该 VPA 的 `.status.conditions` 中暴露一个 `NoPodsMatched` condition，且该 condition 表示匹配不到 pod 的状态为 true。
- 该 `NoPodsMatched` condition 应携带可供外部调用方稳定识别的原因与说明：reason 为 `NoPodsMatched`，message 为 `No live pods match this VPA object`。
- 当 VPA 尚未产生 recommendation 且原因是没有匹配到 live pod 时，`.status.conditions` 中的 `RecommendationProvided` 应为 false，并携带同样的 reason 与 message，以便调用方区分“selector 没选中 pod”和其他暂未推荐的情况。
- 当 VPA 已经产生 recommendation 时，`RecommendationProvided` 仍应表示 recommendation 已提供；没有匹配 pod 的原因不应覆盖“已提供 recommendation”这一状态。
- 对于 selector 当前至少匹配到一个 live pod 的 VPA，recommender 不应把该 VPA 标记为 `NoPodsMatched=True`。

## Implementation notes

- 具体如何判断 pod 与 VPA 的匹配关系、如何在 recommender 的更新流程中传递该状态、以及如何组织内部辅助函数或数据结构，均由实现者根据现有代码结构决定。
- 只要最终写回到 VPA status 的 conditions 满足上述外部可观察行为即可；不要依赖监控端推断内部状态。
