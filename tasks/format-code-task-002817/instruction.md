# Problem Statement

我在 YAML 参数文件里经常要写一些算出来的值，比如某个相位想写成 `2*np.pi*0.3`，或者扫描一组数想用 `2**np.arange(6,10)` 这种生成，但现在 tenpy 加载 YAML 时这些都只能当字符串读进来，没法求值，每次只能自己手动算好再填一堆数字进去，挺烦的。能不能让我在 YAML 里直接写 Python 表达式、加载的时候就帮我算出来？最好 np、scipy 这些在表达式里能直接用，命令行跑 simulation 传的 `*.yml` 也能这么写就好了。

# Expected outcomes

- YAML parameter loading supports an explicit opt-in `!py_eval` tag for Python expression evaluation, so a tagged scalar such as an expression involving `np.pi` is returned as the computed Python value rather than as an unevaluated string.
- The public YAML loader makes `np` available for tagged expressions by default, and callers can make additional names available for expressions when needed.
- YAML files passed to the simulation command-line entry point support the same tagged expression evaluation behavior, with common TeNPy-related names such as `np`, `scipy`, and `tenpy` available to tagged expressions.
- Tagged YAML expressions can produce non-scalar Python values, including lists and NumPy arrays, and those values are preserved in the loaded configuration.
- TeNPy exposes this loader through a public function `tenpy.load_yaml_with_py_eval(...)`, with the same functionality also available from the tools parameters module.
- `Config.from_yaml(...)` loads YAML files using the expression-aware behavior, so configuration objects created from YAML can contain evaluated values.
- User-facing command-line help or documentation for YAML parameter files mentions the availability and purpose of the expression-evaluation tag.

# Implementation notes

The exact loader structure, validation placement, and internal data flow are up to the implementer. The feature should remain opt-in at the YAML value level, avoid changing the meaning of ordinary untagged YAML values, and preserve existing YAML-loading behavior outside the tagged-expression cases.
