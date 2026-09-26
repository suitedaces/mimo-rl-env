## Problem Statement

我在用 Knative eventing 的 Broker,想把 spec.config 指向一个别的 namespace 里的 ConfigMap,结果一直报错。但奇怪的是,如果我把 config 里的 namespace 留空,反而能过校验,这逻辑我有点没搞懂。

我的诉求是:能不能在 config 引用跨 namespace 时给个明确的提示,告诉我到底哪儿不对——比如直接说命名空间对不上、parent 是哪个、ref 又指向哪个,而不是让我瞎猜。

理想情况下,最好默认就要求 config 引用的 namespace 跟 Broker 自己的一致,毕竟大多数时候我就是想引用同 namespace 下的配置。

## Expected outcomes

- Broker 的 `spec.config` 应继续表示指向配置对象的引用，并在公开 API 中采用仓库内标准的 Knative 配置引用语义。
- 对 Broker 做校验时，`spec.config` 缺少必要引用字段仍应报告对应字段缺失。
- `spec.config.namespace` 为空时不应仅因为 namespace 未填写而校验失败。
- 默认情况下，如果 Broker 自身 namespace 与 `spec.config.namespace` 都已设置但不一致，校验应清晰指出 config 引用的 namespace 与 Broker namespace 不匹配，并包含双方 namespace 的上下文。
- 如果 Broker 自身 namespace 与 `spec.config.namespace` 一致，校验不应产生 namespace 不匹配错误。

## Implementation notes

- 具体校验入口、上下文传递方式、辅助函数组织和错误聚合位置由实现者决定。
- 实现应保持现有 Broker 其他校验行为不变，并避免对无关 API、生成器或测试工具行为引入额外要求。
