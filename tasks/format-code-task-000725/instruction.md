## Problem Statement

我在用 ALL 的 SAC 跑连续控制时发现，只把环境 action space 从 `[-1, 1]` 线性放大到比如 `[-2, 2]`，`SoftDeterministicPolicy` 返回的 `log_prob`、entropy 和 policy loss 就会明显跟着尺度变，训练表现也飘得很厉害。另外我开了 `clip_grad` 后，有次梯度范数已经是 NaN/Inf，`step()` 还是继续往下跑了；我这边环境用的是 torch 1.9，但包依赖看起来还卡在 1.8。

## Expected outcomes

- `SoftDeterministicPolicy` 在连续动作空间边界不是 `[-1, 1]` 时，返回的 `log_prob` 应与缩放后的动作分布一致；只线性放大同一任务的动作范围时，`log_prob` 只应体现动作尺度带来的常数偏移，不应出现逐维概率量级被错误放大的现象。
- 基于该 `log_prob` 的 entropy 与 SAC policy loss 不应因为动作空间做等价线性缩放而产生额外的异常尺度变化。
- `Approximation.step()` 在启用非零 `clip_grad` 时，如果待裁剪的梯度范数为 NaN 或 Inf，应抛出 `RuntimeError` 并阻止优化步骤静默继续。
- 包元数据版本应更新为 `0.7.2`，文档配置中的 release 也应更新为 `0.7.2`。
- 安装依赖应面向 torch 1.9，声明为 `torch~=1.9.0`；项目 CI 中固定安装的 CPU 版 torch 也应更新到 `torch==1.9.0+cpu`。

## Implementation notes

具体校正位置、辅助函数组织方式、内部命名和测试覆盖方式由实现者决定；只要公开行为、错误处理语义、版本元数据与依赖声明满足上述结果即可。
