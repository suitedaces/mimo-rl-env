# Problem Statement

我在用 `metpy.calc.lfc()` / `metpy.calc.el()` 算一条基本没有 CIN 的探空时遇到怪现象：从 LCL 往上抬升气块已经比环境温度暖了，后面也只看到一次和环境温度的交点，但这两个函数给我的都是 `nan`。不太确定是不是我这类自由对流廓线的输入哪里不符合 MetPy 的预期。

# Expected outcomes

- 对于无明显对流抑制、气块自 LCL 起已呈正浮力的自由对流廓线，`metpy.calc.lfc(pressure, temperature, dewpt)` 不应把该情形误判为无 LFC 并返回 `nan`；应返回与该廓线物理上对应的自由对流起点，在这类廓线中即 LCL 的压力和温度。
- 对于同类自由对流廓线，`metpy.calc.el(pressure, temperature, dewpt)` 不应因为只有一个可观测到的气块/环境温度交汇层而返回 `nan`；当输入廓线包含可判断的平衡高度时，应返回该平衡高度的压力和温度。
- 对于确实不存在 LFC、确实不存在 EL，或输入廓线不足以判断对应层次的情形，应保持现有无有效层次时返回 `nan` 的行为，不应报告虚假的有效结果。

# Implementation notes

- 具体如何识别交汇层、如何组织中间计算、以及在现有热力学计算流程中的校验位置由实现者决定。
- 保持现有公开 API、单位处理和数值返回风格；调用者应能继续通过 `metpy.calc.lfc()` 和 `metpy.calc.el()` 获得带单位的压力、温度结果。
