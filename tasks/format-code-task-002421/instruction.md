我在用 `enum.Flag` 的时候碰到两个怪现象：没设 `boundary` 的 `Flag`，像 `Color(8)` 这种带未知 bit 的值会被静默变成 `Color.0`，一开始我还以为是我定义写错了。另一个是我定义了 `RWX = R | W | X` 这种组合成员，但实际做 `Perm.R | Perm.W | Perm.X` 时显示出来还是 `Perm.R|W|X`，没有命中那个已经命名的组合。

Expected outcomes:
- `enum.Flag` subclasses that do not explicitly set `boundary` should reject values containing bits not represented by the flag definition, instead of silently discarding those bits.
- Explicit `boundary` choices should continue to work according to their documented meaning, including `STRICT`, `CONFORM`, `EJECT`, and `KEEP`.
- `enum.Flag` bitwise operations and value construction should prefer an already named multi-bit member when the resulting value corresponds to that member.
- When a `Flag` result is a valid combination that includes named multi-bit members, its public representation should include the applicable named members rather than expanding only to single-bit members.
- The enum documentation should describe `STRICT` as the default boundary for `Flag`, while `CONFORM` should remain documented as the mode that discards out-of-range bits.

Implementation notes:
- Preserve existing public `enum.Flag` and `enum.IntFlag` APIs and their explicit boundary behavior while correcting the default `Flag` behavior.
- The internal data structures, validation location, and member-resolution strategy are implementation details; choose whatever approach maintains the public behavior above and the existing enum test suite.
