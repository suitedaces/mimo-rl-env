# Problem Statement

我们 Lambda 用的内存设得比较小（128MB 那种），跑 Node 的函数 OOM 的时候 Datadog 里基本看不到 `aws.lambda.enhanced.out_of_memory` 这个指标，感觉是因为内存太小直接被 kill 了、function 日志里压根没有 OOM 的堆栈，extension 就漏掉了。但其实 AWS 给的 platform.report 日志里 status 是 error、而且 maxMemoryUsed 已经顶到 memorySize 了，这种情况能不能也算成 OOM 给我报出来？另外要注意同一个 requestID 别重复计数，一次 invocation 最多报一次就行。

# Expected outcomes

- Platform report OOM detection: when a Lambda platform report for a request indicates an errored invocation and reports memory usage that reaches or exceeds the configured memory size, the extension emits the same enhanced OOM signal as it does for an OOM found in function logs.
- Existing OOM detection remains intact: function logs that already match the existing out-of-memory detection still emit `aws.lambda.enhanced.out_of_memory` and the associated error enhanced metric.
- Per-request de-duplication: if multiple log records for the same request indicate OOM, including a function log and a platform report for the same request, `aws.lambda.enhanced.out_of_memory` is emitted at most once for that request.
- Request-scoped de-duplication state persistence: the request identity used to avoid duplicate OOM reporting survives the existing execution-context save/restore flow, so restored processing does not count the same request again.
- Non-qualifying platform reports must not be counted as OOM solely because they are report logs.

# Implementation notes

- The exact data structures, helper boundaries, API shape, and validation location are up to the implementer.
- The platform-report path and function-log path should share the same externally visible OOM metric semantics.
- The de-duplication should be based on the request identity, not on log ordering or on a single log source.
