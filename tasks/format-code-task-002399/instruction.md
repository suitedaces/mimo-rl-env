我在用 `pypose.cumprod(..., left=True)` 处理 LieTensor 的时候发现方向有点反：文档看起来是 left 代表左累积，但结果跟我手写 `x0 @ x1 @ ...` 的右累积对上了，`left=False` 反而像左累积。`pypose.cummul` 也有类似现象；另外我试着在 `cummul_` / `cumprod_` 里传 `left`，会直接因为参数不匹配报错。

Expected outcomes:

- Cumulative product direction:
  - `pypose.cumprod(input, dim, left=True)` should perform left cumulative composition along `dim`: each accumulated element should match applying later elements on the left of earlier accumulated elements.
  - `pypose.cumprod(input, dim, left=False)` should perform right cumulative composition along `dim`: each accumulated element should match applying earlier elements before later elements.
- Cumulative multiplication direction:
  - `pypose.cummul(input, dim, left=True)` should use the same left cumulative direction semantics as `cumprod`, but with the multiplication operation used by `cummul`.
  - `pypose.cummul(input, dim, left=False)` should use the corresponding right cumulative direction semantics.
- Custom cumulative operations:
  - `pypose.cumops(input, dim, ops)` and `pypose.cumops_(input, dim, ops)` should produce results consistent with accumulating from the prior prefix value and the current-position value for user-provided non-commutative operations.
- In-place APIs:
  - `pypose.cumprod_(input, dim, left=True/False)` and `pypose.cummul_(input, dim, left=True/False)` should accept `left` and update `input` in place using the same direction semantics as their non-in-place counterparts.
  - `LieTensor.cumprod_(dim, left=True/False)` and `LieTensor.cummul_(dim, left=True/False)` should accept `left` and update the receiver in place using the same direction semantics.
- LieTensor method APIs:
  - `LieTensor.cummul(dim, left=True/False)` should accept `left` and return results consistent with `pypose.cummul(input, dim, left=...)`.
  - Existing `LieTensor.cumprod(dim, left=True/False)` behavior should remain consistent with `pypose.cumprod(input, dim, left=...)`.

Implementation notes:

- Preserve existing public API behavior outside the cumulative operation direction and `left`-parameter support described above.
- The exact internal data flow, helper structure, and validation location are implementation details; the observable behavior should be consistent across functional, in-place, and LieTensor method entry points.
- Tests and user code may rely on non-commutative LieTensor examples to distinguish left and right cumulative directions.
