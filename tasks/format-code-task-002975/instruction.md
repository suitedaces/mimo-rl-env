# Problem Statement

我在写 Vyper 合约的时候发现 `self.__default__()` 这种直接调用 fallback 的写法居然能编译过，但这看起来不像是正常能调用的函数入口，容易让人误以为真的会走默认路径。能不能在编译时直接报错提醒一下，最好顺便告诉我这种情况应该用 `raw_call`？

# Expected outcomes

- 任何直接调用 fallback/default 函数入口 `__default__` 的 Vyper 源码都不应再通过编译。
- 这类编译失败应表现为调用违规类错误，例如公开异常 `CallViolation`，而不是被静默接受或作为普通可调用函数处理。
- 报错信息应清楚表达 `__default__` 不能被直接调用，并提示如果要触发默认路径应使用 `raw_call`。

# Implementation notes

- 具体在哪个语义检查阶段、通过何种内部数据结构识别 fallback/default 函数，以及错误对象如何组装，由实现者根据现有编译器架构决定。
- 保持与现有 Vyper 编译入口、异常体系和测试风格兼容；不要为了该行为引入新的用户可见调用语法或配置开关。
