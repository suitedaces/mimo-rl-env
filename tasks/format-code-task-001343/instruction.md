# Problem Statement

我在做 model surgery 的时候想按 `Conv_0/bias` 这种路径筛参数，现在 `flatten_dict` 给的是 tuple，后面 `unflatten_dict` 又得自己 split 回去，挺绕的；能不能让这两个 `traverse_util` 工具直接支持用分隔符拼出来的字符串路径？另外文档里的优化器例子还在用 `flax.optim`，我现在项目都按 Optax 写，最好也一起换成 Optax 的写法，不然照着改参数状态时有点对不上。

# Expected outcomes

- `flax.traverse_util.flatten_dict(..., sep='/')` should return a flattened mapping whose path keys are separator-joined strings, such as `Conv_0/bias`, instead of tuple path keys.
- `flax.traverse_util.flatten_dict(...)` without a separator should preserve the existing tuple-key behavior.
- `flax.traverse_util.unflatten_dict(..., sep='/')` should accept flattened mappings keyed by separator-joined strings and reconstruct the nested dictionary structure directly.
- `flax.traverse_util.unflatten_dict(...)` without a separator should preserve the existing tuple-key behavior.
- User-facing model-surgery documentation should show the separator-based traversal workflow instead of asking readers to manually join or split flattened tuple keys.
- User-facing optimizer documentation and examples should no longer present `flax.optim` as the recommended path for current code, and should use Optax-style optimizer setup and state handling, including examples built around `optax` transformations and `tx.init(params)`.

# Implementation notes

- The exact internal data structures, helper functions, validation placement, and documentation wording are up to the implementation.
- Preserve backward compatibility for callers that do not request separator-based paths.
- Keep the traversal behavior general rather than special-casing a single separator or a single example path.
