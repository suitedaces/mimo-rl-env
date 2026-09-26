# Problem Statement

现在跑 ECS task 的时候，我只能在 container 级别设 CPU 和内存，没法直接给整个 task 设一个总的上限，资源规划起来挺别扭的。最好能在 task 定义里直接写个 task 级别的 CPULimit 和 Memory，让整个 task 共享这个配额。另外这功能能不能搞个开关控制下，默认开着就行，但像 Windows 这种支持不了的环境，或者 Docker 版本太老不支持的时候，能自动识别然后禁掉、别硬上报错。

# Expected outcomes

- Task definition resource limits
  - The exported task model should accept and emit a task-level CPU limit through the JSON field `CPULimit`.
  - The exported task model should accept and emit a task-level memory limit through the JSON field `Memory`.
  - When these task-level limit fields are unset, normal JSON serialization should omit them rather than adding zero-valued fields.

- Configuration control
  - The feature should be controlled by `ECS_ENABLE_TASK_CPU_MEM_LIMIT`.
  - If `ECS_ENABLE_TASK_CPU_MEM_LIMIT` is not set, the feature should be enabled by default.
  - If `ECS_ENABLE_TASK_CPU_MEM_LIMIT` is set to a false value, the feature should be disabled.
  - On Windows, the feature should remain disabled even if configuration requests enabling it.

- Capability reporting and automatic disablement
  - When the feature is enabled and the local Docker API support is new enough for task-level CPU and memory limits, `DockerTaskEngine.Capabilities()` should advertise task CPU/memory limit support.
  - When the feature is disabled, `DockerTaskEngine.Capabilities()` should not advertise task CPU/memory limit support.
  - When the feature is enabled but the local Docker API support is too old, `DockerTaskEngine.Capabilities()` should not advertise task CPU/memory limit support and should disable the feature for that agent instance rather than returning an unusable capability.

# Implementation notes

- The concrete internal representation, validation location, and capability-detection plumbing are up to the implementer.
- Preserve existing task, configuration, and capability behavior that is unrelated to task-level CPU/memory limits.
- Keep platform-specific behavior consistent with existing platform configuration patterns in the repository.

## Required output literals (exact-match contract)

When `DockerTaskEngine.Capabilities()` advertises task-level CPU and memory limit support, it MUST include the capability attribute `ecs.capability.task-cpu-mem-limit` exactly. Downstream ECS capability negotiation consumes this attribute string.

The Docker API support threshold for task-level CPU and memory limits is Docker API version `1.22`: versions at or above this support level may advertise the capability when the feature is enabled, while older versions must not and must disable the feature for that agent instance.
